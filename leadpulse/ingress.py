"""
Meta Webhook Handler for LeadPulse AI.

Provides FastAPI endpoints for Meta (WhatsApp Cloud API & Instant Form leads):
- GET  /webhook/whatsapp   -> Webhook verification (hub.challenge)
- POST /webhook/whatsapp   -> Incoming WhatsApp messages (HMAC signature verification,
                              tenant lookup, async qualification task, <50ms return)
- POST /webhook/meta-leads -> Meta Instant Form lead capture (Graph API lookup,
                              lead creation, outbound template trigger)
"""

import asyncio
import hashlib
import hmac
import json
import logging
from typing import Any, Optional
from uuid import UUID

from fastapi import APIRouter, Header, Query, Request, Response
from fastapi.responses import PlainTextResponse
import httpx
from sqlalchemy import select

from leadpulse.config import settings
from leadpulse.database import (
    Lead,
    LeadSource,
    LeadStatus,
    Project,
    Tenant,
    async_session_factory,
)
from leadpulse.dispatcher import handle_qualification_flow, send_whatsapp_template
from leadpulse.session import get_or_create_lead

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhook", tags=["webhook"])


# ---------------------------------------------------------------------------
# Helper: Verify Meta HMAC-SHA256 signature
# ---------------------------------------------------------------------------

def verify_meta_signature(raw_body: bytes, signature_header: Optional[str]) -> bool:
    """
    Verify the X-Hub-Signature-256 header against META_APP_SECRET.
    Returns True if valid or if no secret is configured (dev mode).
    """
    secret = settings.META_APP_SECRET
    if not secret:
        logger.warning("META_APP_SECRET is not configured — skipping HMAC verification")
        return True

    if not signature_header:
        logger.warning("Missing X-Hub-Signature-256 header")
        return False

    prefix = "sha256="
    if not signature_header.startswith(prefix):
        logger.warning("Invalid signature header format: %s", signature_header)
        return False

    expected_sig = signature_header[len(prefix):]
    computed_sig = hmac.new(
        key=secret.encode("utf-8"),
        msg=raw_body,
        digestmod=hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(computed_sig, expected_sig)


# ---------------------------------------------------------------------------
# GET /webhook/whatsapp — Webhook Verification
# ---------------------------------------------------------------------------

@router.get("/whatsapp")
async def verify_whatsapp_webhook(
    mode: Optional[str] = Query(None, alias="hub.mode"),
    challenge: Optional[str] = Query(None, alias="hub.challenge"),
    token: Optional[str] = Query(None, alias="hub.verify_token"),
):
    """
    Meta webhook verification endpoint.
    Meta sends hub.mode, hub.challenge, and hub.verify_token to verify ownership.
    Must return hub.challenge with HTTP 200 if verify_token matches.
    """
    logger.info("Webhook verification request: mode=%s, token=%s", mode, token)

    if mode == "subscribe" and token == settings.META_VERIFY_TOKEN:
        logger.info("Webhook verification successful")
        return PlainTextResponse(content=challenge or "", status_code=200)

    logger.warning("Webhook verification failed: token mismatch or mode not subscribe")
    return Response(content="Verification token mismatch", status_code=403)


# ---------------------------------------------------------------------------
# POST /webhook/whatsapp — Inbound WhatsApp Messages
# ---------------------------------------------------------------------------

@router.post("/whatsapp")
async def handle_whatsapp_webhook(
    request: Request,
    x_hub_signature_256: Optional[str] = Header(None, alias="X-Hub-Signature-256"),
):
    """
    Receives incoming WhatsApp Cloud API events:
    1. Verify X-Hub-Signature-256 HMAC
    2. Extract phone number, message text, and display name
    3. Look up owning tenant by whatsapp_phone_number_id
    4. Spawn background qualification task (asyncio.create_task)
    5. Return HTTP 200 immediately (<50ms)
    """
    raw_body = await request.body()

    # a. Verify HMAC signature
    if not verify_meta_signature(raw_body, x_hub_signature_256):
        logger.error("HMAC signature verification failed for incoming WhatsApp webhook")
        return Response(content="Invalid signature", status_code=403)

    # Parse JSON payload
    try:
        payload = json.loads(raw_body.decode("utf-8"))
    except json.JSONDecodeError:
        logger.error("Invalid JSON payload received in WhatsApp webhook")
        return Response(content="Invalid JSON", status_code=400)

    # b. Parse webhook payload
    # Check if entry list exists
    entries = payload.get("entry", [])
    if not entries:
        return {"status": "ok", "message": "No entries"}

    for entry in entries:
        changes = entry.get("changes", [])
        for change in changes:
            value = change.get("value", {})
            metadata = value.get("metadata", {})
            phone_number_id = metadata.get("phone_number_id")

            # Check if this is an incoming message (vs. status updates like sent/delivered/read)
            messages = value.get("messages", [])
            if not messages:
                # Status update or notification — acknowledge immediately
                continue

            msg = messages[0]
            wa_id = msg.get("from")  # Sender's WhatsApp ID / phone number
            msg_type = msg.get("type", "text")

            # Extract message text based on type
            message_text = ""
            if msg_type == "text":
                message_text = msg.get("text", {}).get("body", "")
            elif msg_type == "interactive":
                interactive = msg.get("interactive", {})
                itype = interactive.get("type")
                if itype == "button_reply":
                    message_text = interactive.get("button_reply", {}).get("title", "")
                elif itype == "list_reply":
                    message_text = interactive.get("list_reply", {}).get("title", "")
            elif msg_type == "button":
                message_text = msg.get("button", {}).get("text", "")
            else:
                # Other types (media, location, etc.)
                message_text = f"[{msg_type} message received]"

            # Extract display name if available in contacts
            contacts = value.get("contacts", [])
            display_name = None
            if contacts:
                display_name = contacts[0].get("profile", {}).get("name")

            if not phone_number_id or not wa_id or not message_text:
                continue

            # c & e. Spawn background worker to handle tenant lookup and qualification
            asyncio.create_task(
                _process_incoming_message(
                    phone_number_id=phone_number_id,
                    phone_number=wa_id,
                    message_text=message_text,
                    display_name=display_name,
                )
            )

    # f. Return HTTP 200 immediately (within 50ms)
    return {"status": "ok"}


async def _process_incoming_message(
    phone_number_id: str,
    phone_number: str,
    message_text: str,
    display_name: Optional[str] = None,
) -> None:
    """
    Background worker for WhatsApp qualification flow.
    Operates in its own DB session so the request lifecycle is never blocked.
    """
    logger.info(
        "Processing WhatsApp message from %s (phone_number_id=%s)",
        phone_number,
        phone_number_id,
    )
    try:
        async with async_session_factory() as db:
            # c. Look up tenant by whatsapp_phone_number_id
            stmt_tenant = (
                select(Tenant)
                .where(Tenant.whatsapp_phone_number_id == phone_number_id)
                .where(Tenant.is_active.is_(True))
            )
            result = await db.execute(stmt_tenant)
            tenant = result.scalar_one_or_none()

            # d. If no tenant found, return/log and ignore
            if not tenant:
                logger.warning(
                    "No active tenant found for whatsapp_phone_number_id %s — ignoring message",
                    phone_number_id,
                )
                return

            # Find active project for this tenant
            stmt_project = (
                select(Project)
                .where(Project.tenant_id == tenant.id)
                .where(Project.is_active.is_(True))
                .order_by(Project.created_at.desc())
            )
            res_project = await db.execute(stmt_project)
            project = res_project.scalars().first()

            if not project:
                logger.warning(
                    "Tenant %s (%s) has no active project — ignoring message",
                    tenant.id,
                    tenant.company_name,
                )
                return

            # Get or create lead
            lead = await get_or_create_lead(
                db=db,
                tenant_id=tenant.id,
                project_id=project.id,
                phone_number=phone_number,
                name=display_name,
            )

            # Delegate to qualification flow orchestrator
            await handle_qualification_flow(
                db=db,
                tenant=tenant,
                project=project,
                lead=lead,
                user_message=message_text,
            )

    except Exception as exc:
        logger.exception(
            "Background qualification failed for phone %s: %s",
            phone_number,
            exc,
        )


# ---------------------------------------------------------------------------
# POST /webhook/meta-leads — Meta Instant Form Leads
# ---------------------------------------------------------------------------

@router.post("/meta-leads")
async def handle_meta_leads_webhook(
    request: Request,
    x_hub_signature_256: Optional[str] = Header(None, alias="X-Hub-Signature-256"),
):
    """
    Receives Meta Instant Form lead notifications:
    1. Verify HMAC signature
    2. Extract leadgen_id from payload
    3. Spawn background task to fetch lead details from Graph API and initiate WhatsApp
    4. Return HTTP 200 immediately
    """
    raw_body = await request.body()

    if not verify_meta_signature(raw_body, x_hub_signature_256):
        logger.error("HMAC signature verification failed for meta-leads webhook")
        return Response(content="Invalid signature", status_code=403)

    try:
        payload = json.loads(raw_body.decode("utf-8"))
    except json.JSONDecodeError:
        logger.error("Invalid JSON payload in meta-leads webhook")
        return Response(content="Invalid JSON", status_code=400)

    # Parse leadgen_id(s) from payload
    leadgen_items = []
    entries = payload.get("entry", [])
    for entry in entries:
        changes = entry.get("changes", [])
        for change in changes:
            val = change.get("value", {})
            leadgen_id = val.get("leadgen_id")
            form_id = val.get("form_id")
            page_id = val.get("page_id")
            if leadgen_id:
                leadgen_items.append({
                    "leadgen_id": str(leadgen_id),
                    "form_id": str(form_id) if form_id else None,
                    "page_id": str(page_id) if page_id else None,
                })

    if not leadgen_items:
        # Check direct payload structure if sent differently
        direct_leadgen = payload.get("leadgen_id")
        if direct_leadgen:
            leadgen_items.append({"leadgen_id": str(direct_leadgen), "form_id": None, "page_id": None})

    for item in leadgen_items:
        asyncio.create_task(_process_meta_leadgen(item["leadgen_id"], item.get("form_id"), item.get("page_id")))

    return {"status": "ok", "leads_queued": len(leadgen_items)}


async def _process_meta_leadgen(
    leadgen_id: str,
    form_id: Optional[str] = None,
    page_id: Optional[str] = None,
) -> None:
    """
    Fetches lead details from Meta Graph API using leadgen_id, creates lead record,
    and sends outbound WhatsApp template message.
    """
    logger.info("Processing Meta Instant Form leadgen_id: %s", leadgen_id)

    try:
        async with async_session_factory() as db:
            # Find tenant with active WhatsApp token
            # Look up active tenants
            stmt_tenant = (
                select(Tenant)
                .where(Tenant.is_active.is_(True))
                .where(Tenant.whatsapp_access_token.isnot(None))
            )
            res = await db.execute(stmt_tenant)
            tenants = res.scalars().all()

            if not tenants:
                logger.warning("No active tenant found to process leadgen_id %s", leadgen_id)
                return

            # If multiple tenants, find the one with matching ad account or use first active
            tenant = tenants[0]
            access_token = tenant.whatsapp_access_token
            phone_number_id = tenant.whatsapp_phone_number_id

            # Find active project
            stmt_project = (
                select(Project)
                .where(Project.tenant_id == tenant.id)
                .where(Project.is_active.is_(True))
                .order_by(Project.created_at.desc())
            )
            res_project = await db.execute(stmt_project)
            project = res_project.scalars().first()

            if not project:
                logger.warning("No active project for tenant %s to handle instant form lead", tenant.id)
                return

            # b. Fetch lead details from Meta Graph API
            url = f"https://graph.facebook.com/v20.0/{leadgen_id}"
            params = {"access_token": access_token}

            name: Optional[str] = None
            phone: Optional[str] = None
            email: Optional[str] = None

            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.get(url, params=params)
                if resp.status_code == 200:
                    lead_info = resp.json()
                    field_data = lead_info.get("field_data", [])

                    # c. Extract name, phone, email from field_data
                    for field in field_data:
                        fname = field.get("name", "").lower()
                        fvals = field.get("values", [])
                        val = fvals[0] if fvals else None
                        if not val:
                            continue

                        if "name" in fname:
                            name = val
                        elif "phone" in fname:
                            phone = val
                        elif "email" in fname:
                            email = val
                else:
                    logger.error(
                        "Graph API error %d fetching leadgen_id %s: %s",
                        resp.status_code,
                        leadgen_id,
                        resp.text[:500],
                    )
                    return

            if not phone:
                logger.warning("No phone number found in leadgen_id %s — cannot initiate WhatsApp", leadgen_id)
                return

            # Normalize phone number (strip spaces/plus/dashes)
            clean_phone = "".join(ch for ch in phone if ch.isdigit())

            # d. Create lead in DB (source: instant_form)
            # Check existing
            stmt_lead = (
                select(Lead)
                .where(Lead.tenant_id == tenant.id)
                .where(Lead.phone_number == clean_phone)
            )
            res_lead = await db.execute(stmt_lead)
            existing_lead = res_lead.scalar_one_or_none()

            lead_data_extra = {"email": email, "leadgen_id": leadgen_id, "form_id": form_id}
            if existing_lead:
                lead = existing_lead
                if name and not lead.name:
                    lead.name = name
                lead.source = LeadSource.instant_form
                lead.qualification_data = {**(lead.qualification_data or {}), **lead_data_extra}
            else:
                lead = Lead(
                    tenant_id=tenant.id,
                    project_id=project.id,
                    phone_number=clean_phone,
                    name=name,
                    status=LeadStatus.new,
                    source=LeadSource.instant_form,
                    qualification_data=lead_data_extra,
                    lead_score=0,
                )
                db.add(lead)

            await db.commit()
            await db.refresh(lead)

            logger.info(
                "Created/updated Instant Form lead %s (%s, %s)",
                lead.id,
                lead.name,
                clean_phone,
            )

            # Trigger outbound WhatsApp template message
            if phone_number_id and access_token:
                template_name = "lead_qualification_intro"
                rules = project.qualification_rules or {}
                if "template_name" in rules:
                    template_name = rules["template_name"]

                await send_whatsapp_template(
                    phone_number_id=phone_number_id,
                    access_token=access_token,
                    to_number=clean_phone,
                    template_name=template_name,
                    language=rules.get("language", "en"),
                )

    except Exception as exc:
        logger.exception("Error processing meta leadgen_id %s: %s", leadgen_id, exc)

"""
Outbound Message Dispatcher for LeadPulse AI.

Handles sending WhatsApp messages (text + templates) and Telegram alerts.
Contains the main qualification orchestrator that ties together
session, agent, and dispatch layers.
"""

import logging
from typing import Any, Optional
from uuid import UUID

import httpx

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# WhatsApp Cloud API — Text Message
# ---------------------------------------------------------------------------

async def send_whatsapp_message(
    phone_number_id: str,
    access_token: str,
    to_number: str,
    text: str,
) -> bool:
    """
    Send a text message via WhatsApp Cloud API.

    POST https://graph.facebook.com/v20.0/{phone_number_id}/messages

    Returns True on success, False on failure.
    """
    url = f"https://graph.facebook.com/v20.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_number,
        "type": "text",
        "text": {"preview_url": False, "body": text},
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
            if resp.status_code == 200:
                logger.info("WhatsApp message sent to %s", to_number)
                return True
            else:
                logger.error(
                    "WhatsApp API error %d for %s: %s",
                    resp.status_code,
                    to_number,
                    resp.text[:500],
                )
                return False
    except httpx.HTTPError as exc:
        logger.error("WhatsApp HTTP error sending to %s: %s", to_number, exc)
        return False
    except Exception as exc:
        logger.exception("Unexpected error sending WhatsApp to %s: %s", to_number, exc)
        return False


# ---------------------------------------------------------------------------
# WhatsApp Cloud API — Template Message
# ---------------------------------------------------------------------------

async def send_whatsapp_template(
    phone_number_id: str,
    access_token: str,
    to_number: str,
    template_name: str,
    language: str = "en",
) -> bool:
    """
    Send a pre-approved template message via WhatsApp Cloud API.
    Used for business-initiated conversations (e.g., following up on
    instant form leads outside the 24h messaging window).

    Returns True on success, False on failure.
    """
    url = f"https://graph.facebook.com/v20.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": language},
        },
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
            if resp.status_code == 200:
                logger.info(
                    "WhatsApp template '%s' sent to %s",
                    template_name,
                    to_number,
                )
                return True
            else:
                logger.error(
                    "WhatsApp template API error %d for %s: %s",
                    resp.status_code,
                    to_number,
                    resp.text[:500],
                )
                return False
    except httpx.HTTPError as exc:
        logger.error(
            "WhatsApp HTTP error sending template to %s: %s", to_number, exc
        )
        return False
    except Exception as exc:
        logger.exception(
            "Unexpected error sending WhatsApp template to %s: %s", to_number, exc
        )
        return False


# ---------------------------------------------------------------------------
# Telegram Alert
# ---------------------------------------------------------------------------

async def send_telegram_alert(
    bot_token: str,
    chat_id: str,
    lead_data: dict[str, Any],
) -> bool:
    """
    Send a rich HTML-formatted lead alert to a Telegram chat/group.

    lead_data expected keys:
        name, phone, status, lead_score, qualification_data,
        appointment_time (optional), project_name, company_name

    Returns True on success, False on failure.
    """
    name = lead_data.get("name", "Unknown")
    phone = lead_data.get("phone", "N/A")
    status = lead_data.get("status", "qualified")
    score = lead_data.get("lead_score", 0)
    project = lead_data.get("project_name", "")
    company = lead_data.get("company_name", "")
    qual_data = lead_data.get("qualification_data", {})
    appointment = lead_data.get("appointment_time")

    # Build qualification summary
    qual_lines = []
    for key, value in qual_data.items():
        qual_lines.append(f"  • <b>{key}</b>: {value}")
    qual_summary = "\n".join(qual_lines) if qual_lines else "  No data collected"

    # Status emoji
    status_emoji = {
        "qualified": "✅",
        "appointment_booked": "📅",
    }.get(status, "🔔")

    message = (
        f"{status_emoji} <b>New Qualified Lead!</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"👤 <b>Name:</b> {name}\n"
        f"📱 <b>Phone:</b> {phone}\n"
        f"📊 <b>Score:</b> {score}/100\n"
        f"🏢 <b>Project:</b> {project}\n"
        f"🏷️ <b>Company:</b> {company}\n"
    )

    if appointment:
        message += f"📅 <b>Appointment:</b> {appointment}\n"

    message += (
        f"\n📋 <b>Qualification Details:</b>\n"
        f"{qual_summary}\n"
        f"━━━━━━━━━━━━━━━━━━"
    )

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code == 200:
                logger.info("Telegram alert sent for lead %s to chat %s", name, chat_id)
                return True
            else:
                logger.error(
                    "Telegram API error %d: %s",
                    resp.status_code,
                    resp.text[:500],
                )
                return False
    except httpx.HTTPError as exc:
        logger.error("Telegram HTTP error: %s", exc)
        return False
    except Exception as exc:
        logger.exception("Unexpected error sending Telegram alert: %s", exc)
        return False


# ---------------------------------------------------------------------------
# Main Orchestrator — called by ingress.py as a background task
# ---------------------------------------------------------------------------

async def handle_qualification_flow(
    db,
    tenant,
    project,
    lead,
    user_message: str,
) -> None:
    """
    End-to-end qualification flow for a single inbound WhatsApp message.

    1. Retrieve conversation history
    2. Run Claude qualification agent
    3. Save inbound + outbound messages
    4. Send WhatsApp reply
    5. Handle terminal actions (QUALIFY / DISQUALIFY / BOOK_APPOINTMENT)

    This function NEVER raises — all errors are caught and logged so
    the webhook background task cannot crash.
    """
    from leadpulse.agent import qualify_lead
    from leadpulse.session import (
        get_conversation_history,
        save_message,
        update_lead_status,
    )

    try:
        # 1. Get conversation history
        history = await get_conversation_history(db, lead.id, limit=10)

        # 2. Run Claude qualification
        result = await qualify_lead(tenant, project, lead, user_message, history)

        reply_text = result["reply_text"]
        action = result["action"]
        extracted_data = result["extracted_data"]
        lead_score = result["lead_score"]
        reasoning = result["reasoning"]

        # 3. Save inbound message (the user's message)
        await save_message(
            db=db,
            lead_id=lead.id,
            tenant_id=tenant.id,
            direction="inbound",
            content=user_message,
        )

        # 4. Save outbound message (Claude's reply) with reasoning
        await save_message(
            db=db,
            lead_id=lead.id,
            tenant_id=tenant.id,
            direction="outbound",
            content=reply_text,
            claude_reasoning={
                "action": action,
                "lead_score": lead_score,
                "extracted_data": extracted_data,
                "reasoning": reasoning,
            },
        )

        # 5. Send WhatsApp reply
        await send_whatsapp_message(
            phone_number_id=tenant.whatsapp_phone_number_id,
            access_token=tenant.whatsapp_access_token,
            to_number=lead.phone_number,
            text=reply_text,
        )

        # 6. Handle terminal actions
        if action == "QUALIFY":
            await update_lead_status(
                db=db,
                lead_id=lead.id,
                status="qualified",
                qualification_data=extracted_data,
                lead_score=lead_score,
            )
            # Send Telegram alert to sales team
            await _send_sales_alert(tenant, project, lead, extracted_data, lead_score)

        elif action == "BOOK_APPOINTMENT":
            await update_lead_status(
                db=db,
                lead_id=lead.id,
                status="appointment_booked",
                qualification_data=extracted_data,
                lead_score=lead_score,
            )
            # Send Telegram alert with appointment info
            await _send_sales_alert(
                tenant,
                project,
                lead,
                extracted_data,
                lead_score,
                appointment_time=extracted_data.get("appointment_time"),
            )

        elif action == "DISQUALIFY":
            await update_lead_status(
                db=db,
                lead_id=lead.id,
                status="disqualified",
                disqualification_reason=reasoning,
                lead_score=lead_score,
            )

        else:
            # CONTINUE — update to in_conversation if still new
            new_status = "in_conversation" if getattr(lead, "status", None) == "new" else getattr(lead, "status", "in_conversation")
            await update_lead_status(
                db=db,
                lead_id=lead.id,
                status=new_status,
                qualification_data=extracted_data,
                lead_score=lead_score,
            )

        logger.info(
            "Qualification flow complete for lead %s: action=%s score=%d",
            lead.id,
            action,
            lead_score,
        )

    except Exception as exc:
        logger.exception(
            "Qualification flow failed for lead %s (tenant %s): %s",
            lead.id,
            tenant.id,
            exc,
        )


async def _send_sales_alert(
    tenant,
    project,
    lead,
    extracted_data: dict,
    lead_score: int,
    appointment_time: Optional[str] = None,
) -> None:
    """
    Send a Telegram alert to the tenant's sales team.
    Uses the global TELEGRAM_BOT_TOKEN from config.
    """
    from leadpulse.config import settings

    bot_token = settings.TELEGRAM_BOT_TOKEN

    if not bot_token:
        logger.warning("No Telegram bot token configured — skipping alert")
        return

    # Check tenant attribute, project rules, or project attribute for telegram chat_id
    chat_id = getattr(tenant, "telegram_chat_id", None)
    if not chat_id and project and hasattr(project, "qualification_rules") and project.qualification_rules:
        chat_id = project.qualification_rules.get("telegram_chat_id")
    if not chat_id and project:
        chat_id = getattr(project, "telegram_chat_id", None)

    if not chat_id:
        logger.warning(
            "No Telegram chat_id found for tenant %s or project %s — skipping alert",
            tenant.id,
            getattr(project, "id", None),
        )
        return

    lead_data = {
        "name": lead.name or "Unknown",
        "phone": lead.phone_number,
        "status": lead.status,
        "lead_score": lead_score,
        "qualification_data": extracted_data,
        "project_name": project.name if project else "",
        "company_name": tenant.company_name if tenant else "",
        "appointment_time": appointment_time,
    }

    await send_telegram_alert(bot_token, str(chat_id), lead_data)

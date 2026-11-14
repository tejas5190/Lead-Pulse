"""
Conversation State Manager for LeadPulse AI.

Manages lead lifecycle, conversation history retrieval, and message persistence.
All database operations are scoped by tenant_id for multi-tenant isolation.
"""

import logging
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def get_or_create_lead(
    db: AsyncSession,
    tenant_id: UUID,
    project_id: UUID,
    phone_number: str,
    name: Optional[str] = None,
) :
    """
    Retrieve an existing lead by phone number within a tenant,
    or create a new one if none exists.
    Returns the Lead ORM object.
    """
    from leadpulse.database import Lead, LeadSource, LeadStatus

    stmt = (
        select(Lead)
        .where(Lead.tenant_id == tenant_id)
        .where(Lead.phone_number == phone_number)
    )
    result = await db.execute(stmt)
    lead = result.scalar_one_or_none()

    if lead is not None:
        # Update name if we now have one and didn't before
        if name and not lead.name:
            lead.name = name
            await db.commit()
            await db.refresh(lead)
        logger.debug("Found existing lead %s for phone %s", lead.id, phone_number)
        return lead

    lead = Lead(
        tenant_id=tenant_id,
        project_id=project_id,
        phone_number=phone_number,
        name=name,
        status=LeadStatus.new,
        lead_score=0,
        source=LeadSource.ctwa,
    )
    db.add(lead)
    await db.commit()
    await db.refresh(lead)
    logger.info(
        "Created new lead %s for tenant %s, phone %s",
        lead.id,
        tenant_id,
        phone_number,
    )
    return lead


async def get_conversation_history(
    db: AsyncSession,
    lead_id: UUID,
    limit: int = 10,
) -> list[dict]:
    """
    Fetch the most recent messages for a lead and format them
    as a list of {role, content} dicts suitable for Claude's
    messages parameter.

    inbound  -> role: "user"
    outbound -> role: "assistant"
    """
    from leadpulse.database import Message

    stmt = (
        select(Message)
        .where(Message.lead_id == lead_id)
        .order_by(Message.timestamp.desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    messages = result.scalars().all()

    # Reverse so oldest first (chronological order)
    messages = list(reversed(messages))

    history: list[dict] = []
    for msg in messages:
        role = "user" if msg.direction == "inbound" else "assistant"
        history.append({"role": role, "content": msg.content})

    logger.debug("Retrieved %d messages for lead %s", len(history), lead_id)
    return history


async def update_lead_status(
    db: AsyncSession,
    lead_id: UUID,
    status: str,
    qualification_data: Optional[dict] = None,
    disqualification_reason: Optional[str] = None,
    lead_score: Optional[int] = None,
) -> None:
    """
    Update a lead's status and optionally set qualification data,
    disqualification reason, or lead score.
    """
    from leadpulse.database import Lead, LeadStatus

    status_enum = LeadStatus(status) if isinstance(status, str) else status
    values: dict = {"status": status_enum}

    if qualification_data is not None:
        values["qualification_data"] = qualification_data

    if disqualification_reason is not None:
        values["disqualification_reason"] = disqualification_reason

    if lead_score is not None:
        values["lead_score"] = lead_score

    if str(status) in ("qualified", "appointment_booked"):
        values["qualified_at"] = datetime.now(timezone.utc)

    stmt = update(Lead).where(Lead.id == lead_id).values(**values)
    await db.execute(stmt)
    await db.commit()
    logger.info("Updated lead %s status to %s (score=%s)", lead_id, status, lead_score)


async def save_message(
    db: AsyncSession,
    lead_id: UUID,
    tenant_id: UUID,
    direction: str,
    content: str,
    claude_reasoning: Optional[dict] = None,
) -> None:
    """
    Persist a message (inbound or outbound) to the messages table.

    Args:
        direction: "inbound" or "outbound"
        claude_reasoning: optional JSON with Claude's internal reasoning
    """
    from leadpulse.database import Message, MessageDirection

    dir_enum = MessageDirection(direction) if isinstance(direction, str) else direction
    message = Message(
        lead_id=lead_id,
        tenant_id=tenant_id,
        direction=dir_enum,
        content=content,
        claude_reasoning=claude_reasoning,
    )
    db.add(message)
    await db.commit()
    logger.debug(
        "Saved %s message for lead %s (tenant %s)",
        direction,
        lead_id,
        tenant_id,
    )

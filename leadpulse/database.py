"""LeadPulse AI — SQLAlchemy 2.0 async ORM models and session management."""

from __future__ import annotations

import enum
import uuid
from datetime import date, datetime
from typing import AsyncGenerator

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    Uuid as UUID,
    func,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from .config import settings

# ── Enums ─────────────────────────────────────────────────────────────


class PlanTier(str, enum.Enum):
    free_trial = "free_trial"
    starter = "starter"
    professional = "professional"
    agency = "agency"


class LeadStatus(str, enum.Enum):
    new = "new"
    in_conversation = "in_conversation"
    qualified = "qualified"
    disqualified = "disqualified"
    appointment_booked = "appointment_booked"


class LeadSource(str, enum.Enum):
    ctwa = "ctwa"
    instant_form = "instant_form"
    instagram_dm = "instagram_dm"
    manual = "manual"


class MessageDirection(str, enum.Enum):
    inbound = "inbound"
    outbound = "outbound"


# ── Base ──────────────────────────────────────────────────────────────


class Base(DeclarativeBase):
    pass


# ── Models ────────────────────────────────────────────────────────────


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    industry: Mapped[str] = mapped_column(String(128), nullable=False)
    owner_email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)

    # WhatsApp / Meta
    whatsapp_phone_number_id: Mapped[str | None] = mapped_column(String(64))
    whatsapp_access_token: Mapped[str | None] = mapped_column(Text)  # encrypted at app layer
    meta_ad_account_id: Mapped[str | None] = mapped_column(String(64))

    # AI
    claude_api_key: Mapped[str | None] = mapped_column(Text)  # encrypted at app layer

    # Billing
    plan: Mapped[PlanTier] = mapped_column(
        Enum(PlanTier, name="plan_tier"), default=PlanTier.free_trial
    )
    trial_leads_remaining: Mapped[int] = mapped_column(Integer, default=10)

    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    projects: Mapped[list["Project"]] = relationship(
        back_populates="tenant", cascade="all, delete-orphan"
    )
    leads: Mapped[list["Lead"]] = relationship(
        back_populates="tenant", cascade="all, delete-orphan"
    )
    messages: Mapped[list["Message"]] = relationship(
        back_populates="tenant", cascade="all, delete-orphan"
    )
    metrics: Mapped[list["MetricsCache"]] = relationship(
        back_populates="tenant", cascade="all, delete-orphan"
    )
    ad_campaigns: Mapped[list["AdCampaign"]] = relationship(
        back_populates="tenant", cascade="all, delete-orphan"
    )


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Flexible qualification config — schema-free JSON:
    # {
    #   "greeting": "Hi {{name}}, thanks for your interest!",
    #   "ai_personality": "friendly, professional",
    #   "language": "en",
    #   "questions": [
    #       {"key": "budget", "ask": "What is your budget range?", "type": "text",
    #        "pass_criteria": {"min_value": 50000}},
    #       {"key": "timeline", "ask": "When are you looking to proceed?", "type": "choice",
    #        "options": ["Immediately", "1-3 months", "3-6 months", "Just exploring"],
    #        "pass_criteria": {"accepted": ["Immediately", "1-3 months"]}},
    #   ],
    #   "pass_threshold": 70,
    #   "disqualify_message": "Thanks for chatting! We'll keep you posted.",
    #   "qualified_message": "Great news — you qualify! A team member will reach out shortly."
    # }
    qualification_rules: Mapped[dict | None] = mapped_column(JSON, default=dict)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    tenant: Mapped["Tenant"] = relationship(back_populates="projects")
    leads: Mapped[list["Lead"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    metrics: Mapped[list["MetricsCache"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str | None] = mapped_column(String(255))

    status: Mapped[LeadStatus] = mapped_column(
        Enum(LeadStatus, name="lead_status"), default=LeadStatus.new
    )
    qualification_data: Mapped[dict | None] = mapped_column(JSON, default=dict)
    disqualification_reason: Mapped[str | None] = mapped_column(Text)
    lead_score: Mapped[int] = mapped_column(Integer, default=0)  # 0-100

    source: Mapped[LeadSource] = mapped_column(
        Enum(LeadSource, name="lead_source"), default=LeadSource.ctwa
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    qualified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Relationships
    tenant: Mapped["Tenant"] = relationship(back_populates="leads")
    project: Mapped["Project"] = relationship(back_populates="leads")
    messages: Mapped[list["Message"]] = relationship(
        back_populates="lead", cascade="all, delete-orphan"
    )


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    lead_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("leads.id", ondelete="CASCADE"), nullable=False
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False
    )
    direction: Mapped[MessageDirection] = mapped_column(
        Enum(MessageDirection, name="message_direction"), nullable=False
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    claude_reasoning: Mapped[dict | None] = mapped_column(JSON)

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    lead: Mapped["Lead"] = relationship(back_populates="messages")
    tenant: Mapped["Tenant"] = relationship(back_populates="messages")


class MetricsCache(Base):
    __tablename__ = "metrics_cache"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    date: Mapped[date] = mapped_column(Date, nullable=False)

    impressions: Mapped[int] = mapped_column(Integer, default=0)
    clicks: Mapped[int] = mapped_column(Integer, default=0)
    leads_count: Mapped[int] = mapped_column(Integer, default=0)
    spend_inr: Mapped[float] = mapped_column(Float, default=0.0)
    cpl_inr: Mapped[float] = mapped_column(Float, default=0.0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    tenant: Mapped["Tenant"] = relationship(back_populates="metrics")
    project: Mapped["Project"] = relationship(back_populates="metrics")


class AdCampaign(Base):
    __tablename__ = "ad_campaigns"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    objective: Mapped[str] = mapped_column(String(64), default="OUTCOME_LEADS")
    platform: Mapped[str] = mapped_column(String(64), default="Meta (Instagram & Facebook)")
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE")
    daily_budget: Mapped[float] = mapped_column(Float, default=500.0)
    target_cpl: Mapped[float] = mapped_column(Float, default=250.0)
    currency: Mapped[str] = mapped_column(String(10), default="INR")
    auto_pilot: Mapped[bool] = mapped_column(Boolean, default=True)

    targeting: Mapped[dict | None] = mapped_column(JSON, default=dict)
    creative: Mapped[dict | None] = mapped_column(JSON, default=dict)

    impressions: Mapped[int] = mapped_column(Integer, default=0)
    clicks: Mapped[int] = mapped_column(Integer, default=0)
    spend: Mapped[float] = mapped_column(Float, default=0.0)
    leads: Mapped[int] = mapped_column(Integer, default=0)

    optimization_logs: Mapped[list | None] = mapped_column(JSON, default=list)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    tenant: Mapped["Tenant"] = relationship(back_populates="ad_campaigns")


# ── Engine & Session ──────────────────────────────────────────────────

is_sqlite = settings.DATABASE_URL.startswith("sqlite")
engine_kwargs: dict = {"echo": False}
if not is_sqlite:
    engine_kwargs["pool_size"] = 5
    engine_kwargs["max_overflow"] = 10

engine = create_async_engine(
    settings.DATABASE_URL,
    **engine_kwargs,
)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields an async database session."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

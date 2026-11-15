"""
LeadPulse AI — Pydantic v2 request/response schemas.
"""

from __future__ import annotations

import math
import uuid
from datetime import date, datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


# ────────────────────────────────────────────────────────
#  Enums (mirrors database enums)
# ────────────────────────────────────────────────────────

class PlanTier(str, Enum):
    free_trial = "free_trial"
    starter = "starter"
    professional = "professional"
    agency = "agency"


# Alias for backwards compatibility
PlanType = PlanTier


class LeadStatus(str, Enum):
    new = "new"
    in_conversation = "in_conversation"
    qualified = "qualified"
    disqualified = "disqualified"
    appointment_booked = "appointment_booked"


class LeadSource(str, Enum):
    ctwa = "ctwa"
    instant_form = "instant_form"
    instagram_dm = "instagram_dm"
    manual = "manual"


class MessageDirection(str, Enum):
    inbound = "inbound"
    outbound = "outbound"


# ────────────────────────────────────────────────────────
#  Auth schemas
# ────────────────────────────────────────────────────────

class TenantCreate(BaseModel):
    company_name: str = Field(..., min_length=1, max_length=255)
    industry: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class TenantLogin(BaseModel):
    email: EmailStr
    password: str


class TenantResponse(BaseModel):
    id: uuid.UUID
    company_name: str
    industry: str
    owner_email: str
    plan: PlanTier
    trial_leads_remaining: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ────────────────────────────────────────────────────────
#  Qualification rules (flexible, dynamic)
# ────────────────────────────────────────────────────────

class QualificationRule(BaseModel):
    question: str = Field(..., min_length=1, description="The question to ask the lead")
    pass_criteria: str = Field(..., min_length=1, description="What constitutes a passing answer")
    is_required: bool = Field(default=True, description="Whether this question must be answered")

    model_config = {"extra": "allow"}


class QualificationRules(BaseModel):
    questions: list[QualificationRule] = Field(default_factory=list)
    greeting_message: str = Field(
        default="Hello! Thanks for reaching out. I'd love to help you. Let me ask a few quick questions.",
    )
    ai_personality: str = Field(
        default="friendly and professional",
        description="Tone/style the AI agent should adopt",
    )
    language: str = Field(
        default="en",
        description="Primary language for the conversation (ISO 639-1)",
    )

    model_config = {"extra": "allow"}


# ────────────────────────────────────────────────────────
#  Project schemas
# ────────────────────────────────────────────────────────

class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    qualification_rules: QualificationRules = Field(default_factory=QualificationRules)


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    qualification_rules: QualificationRules | None = None
    is_active: bool | None = None

    @model_validator(mode="after")
    def at_least_one_field(self) -> "ProjectUpdate":
        if self.name is None and self.qualification_rules is None and self.is_active is None:
            raise ValueError("At least one field must be provided for update")
        return self


class ProjectResponse(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    name: str
    qualification_rules: dict[str, Any]
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ────────────────────────────────────────────────────────
#  Lead schemas
# ────────────────────────────────────────────────────────

class LeadResponse(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    phone_number: str
    name: str | None = None
    status: LeadStatus
    lead_score: int
    source: LeadSource
    qualification_data: dict[str, Any] | None = None
    disqualification_reason: str | None = None
    created_at: datetime
    qualified_at: datetime | None = None

    model_config = {"from_attributes": True}


class LeadDetailResponse(LeadResponse):
    pass


class MessageResponse(BaseModel):
    direction: MessageDirection
    content: str
    timestamp: datetime

    model_config = {"from_attributes": True}


class LeadTranscriptResponse(BaseModel):
    lead_id: uuid.UUID
    lead_name: str | None = None
    phone_number: str
    messages: list[MessageResponse]


# ────────────────────────────────────────────────────────
#  Metrics schemas
# ────────────────────────────────────────────────────────

class LeadsByDay(BaseModel):
    date: date
    total: int
    qualified: int
    disqualified: int


class MetricsResponse(BaseModel):
    total_leads: int
    qualified: int
    disqualified: int
    qualification_rate: float = Field(
        ..., description="Percentage 0-100"
    )
    avg_lead_score: float
    leads_by_day: list[LeadsByDay]


class MetricsSummaryResponse(BaseModel):
    today_leads: int
    this_week_qualified: int
    total_active_leads: int
    conversion_rate: float = Field(
        ..., description="Qualified / total leads percentage"
    )


# ────────────────────────────────────────────────────────
#  Settings schemas
# ────────────────────────────────────────────────────────

class SettingsResponse(BaseModel):
    company_name: str
    industry: str
    owner_email: str
    plan: PlanTier
    trial_leads_remaining: int
    whatsapp_phone_number_id: str | None = None
    meta_ad_account_id: str | None = None
    telegram_chat_id: str | None = None
    has_claude_api_key: bool = False
    has_whatsapp_access_token: bool = False

    model_config = {"from_attributes": True}


class SettingsUpdate(BaseModel):
    company_name: str | None = Field(default=None, max_length=255)
    whatsapp_phone_number_id: str | None = None
    meta_ad_account_id: str | None = None
    telegram_chat_id: str | None = None

    @model_validator(mode="after")
    def at_least_one_field(self) -> "SettingsUpdate":
        values = [
            self.company_name,
            self.whatsapp_phone_number_id,
            self.meta_ad_account_id,
            self.telegram_chat_id,
        ]
        if all(v is None for v in values):
            raise ValueError("At least one field must be provided for update")
        return self


class ApiKeysUpdate(BaseModel):
    claude_api_key: str | None = Field(default=None, min_length=1)
    whatsapp_access_token: str | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def at_least_one_key(self) -> "ApiKeysUpdate":
        if self.claude_api_key is None and self.whatsapp_access_token is None:
            raise ValueError("At least one API key must be provided")
        return self


# ────────────────────────────────────────────────────────
#  Paginated wrapper
# ────────────────────────────────────────────────────────

class PaginatedLeadsResponse(BaseModel):
    items: list[LeadResponse]
    total: int
    page: int
    limit: int
    pages: int


# ────────────────────────────────────────────────────────
#  Creative Studio Schemas
# ────────────────────────────────────────────────────────

class SmartParseRequest(BaseModel):
    prompt: str = Field(min_length=3, description="Natural language business or campaign description")


class SmartParseResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    topic: str
    company_name: Optional[str] = None
    product_name: str
    price_point: Optional[str] = None
    location: Optional[str] = None
    target_audience: Optional[str] = None
    key_benefit: Optional[str] = None
    industry: Optional[str] = "food"
    tone: Optional[str] = "high_energy"
    suggested_cta: Optional[str] = None
    engine: Optional[str] = None


class CreativeCopyRequest(BaseModel):
    product_name: str = Field(min_length=2)
    company_name: Optional[str] = None
    topic: Optional[str] = None
    industry: str = Field(default="universal")
    price_point: str = Field(default="Competitive Pricing")
    location: str = Field(default="Your City")
    key_benefit: str = Field(default="Guaranteed Quality & Fast Delivery")
    target_audience: str = Field(default="Target Audience")
    duration: Optional[int] = Field(default=15)
    quality: Optional[str] = Field(default="1080p")
    tone: Optional[str] = Field(default="high_energy")


class CreativeCopyResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    product_name: str
    company_name: Optional[str] = None
    topic: Optional[str] = None
    industry: str
    primary_texts: list[str]
    headlines: list[str]
    descriptions: list[str]
    call_to_action: str
    video_script: dict[str, str]
    screenplay: Optional[list[dict[str, Any]]] = None
    duration: Optional[int] = 15
    quality: Optional[str] = "1080p"
    tone: Optional[str] = "high_energy"
    full_narration: str
    thinking_process: Optional[str] = None
    engine: Optional[str] = None


class CreativeBannerRequest(BaseModel):
    product_name: str = Field(min_length=2)
    headline: str = Field(min_length=3)
    price_tag: str = Field(default="Starting ₹85L")
    location: str = Field(default="Prime Location")
    key_points: list[str] = Field(default_factory=lambda: ["Direct Developer Offer", "Instant WhatsApp Brochure", "Zero Brokerage"])
    aspect_ratio: str = Field(default="1:1")  # "1:1" or "9:16"


class CreativeBannerResponse(BaseModel):
    banner_url: str
    aspect_ratio: str


class CreativeVideoRequest(BaseModel):
    product_name: str = Field(min_length=2)
    price_point: str = Field(default="Starting ₹85L")
    location: str = Field(default="Prime Location")
    key_benefit: str = Field(default="Zero Brokerage · Luxury Amenities")
    script: dict[str, str]
    voice: str = Field(default="en-IN-NeerjaNeural")


class CreativeVideoResponse(BaseModel):
    video_url: str
    format: str = "9:16"


# ────────────────────────────────────────────────────────
#  Agency Marketing & Social Concierge Schemas
# ────────────────────────────────────────────────────────

class StrategyRequest(BaseModel):
    business_name: str = Field(min_length=2)
    industry: str = Field(default="dental")
    location: str = Field(default="Indiranagar, Bangalore")
    target_audience: str = Field(default="Local residents seeking clear aligners")
    key_offer: str = Field(default="From ₹2,499/mo | Free 3D Scan")


class StrategyResponse(BaseModel):
    business_name: str
    industry: str
    location: str
    phases_overview: list[dict[str, str]]
    days: list[dict[str, Any]]


class PageSetupRequest(BaseModel):
    business_name: str = Field(min_length=2)
    industry: str = Field(default="dental")
    location: str = Field(default="Indiranagar, Bangalore")
    phone_number: str = Field(default="+919876543210")
    key_offer: str = Field(default="From ₹2,499/mo | Free 3D Scan")


class PageSetupResponse(BaseModel):
    business_name: str
    industry: str
    location: str
    instagram: dict[str, Any]
    facebook: dict[str, Any]
    non_tech_checklist: list[dict[str, Any]]


# ── Meta Ads Manager Schemas ──────────────────────────────────────────

class AdCampaignCreateRequest(BaseModel):
    name: str = Field(min_length=2)
    objective: str = Field(default="OUTCOME_LEADS")
    daily_budget: float = Field(default=500.0, ge=100.0)
    target_cpl: float = Field(default=250.0, ge=10.0)
    currency: str = Field(default="INR")
    targeting: Optional[dict[str, Any]] = None
    creative: Optional[dict[str, Any]] = None
    auto_pilot: bool = Field(default=True)


class AdCampaignUpdateRequest(BaseModel):
    status: Optional[str] = None
    daily_budget: Optional[float] = None
    target_cpl: Optional[float] = None
    auto_pilot: Optional[bool] = None


class AdCampaignResponse(BaseModel):
    id: uuid.UUID | str
    name: str
    objective: str
    platform: str
    status: str
    daily_budget: float
    target_cpl: float
    currency: str
    auto_pilot: bool
    targeting: Optional[dict[str, Any]] = None
    creative: Optional[dict[str, Any]] = None
    impressions: int = 0
    clicks: int = 0
    spend: float = 0.0
    leads: int = 0
    ctr: float = 0.0
    cpl: float = 0.0
    optimization_logs: list[dict[str, Any]] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

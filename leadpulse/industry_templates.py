"""
LeadPulse AI — Pre-built industry qualification templates.

Each template is a starting point that tenants can customise after creation.
"""

from __future__ import annotations

from typing import Any


def _template(
    *,
    industry: str,
    greeting: str,
    personality: str,
    language: str,
    questions: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build a template dict in the same shape as QualificationRules."""
    return {
        "industry": industry,
        "qualification_rules": {
            "greeting_message": greeting,
            "ai_personality": personality,
            "language": language,
            "questions": questions,
        },
    }


INDUSTRY_TEMPLATES: dict[str, dict[str, Any]] = {
    # ── Real Estate ──────────────────────────────────────
    "real_estate": _template(
        industry="Real Estate",
        greeting=(
            "Hi! 🏠 Thanks for your interest in our property listings. "
            "I'd love to help you find the perfect home. May I ask a few quick questions?"
        ),
        personality="warm, knowledgeable real-estate advisor",
        language="en",
        questions=[
            {
                "question": "What is your approximate budget range for this property?",
                "pass_criteria": "Budget is ≥ ₹30,00,000 (or project-specific minimum)",
                "is_required": True,
            },
            {
                "question": "When are you looking to move in or take possession?",
                "pass_criteria": "Timeline is within 12 months",
                "is_required": True,
            },
            {
                "question": "Would you like to book a site visit this week?",
                "pass_criteria": "Lead agrees to visit or asks for available dates",
                "is_required": False,
            },
        ],
    ),

    # ── Dental Clinic ────────────────────────────────────
    "dental_clinic": _template(
        industry="Dental Clinic",
        greeting=(
            "Hello! 😊 Thank you for reaching out to our clinic. "
            "Let me help you with the right treatment. A few quick questions first—"
        ),
        personality="caring, reassuring healthcare professional",
        language="en",
        questions=[
            {
                "question": "Which dental procedure are you interested in? (e.g., braces, implants, whitening, general check-up)",
                "pass_criteria": "Lead specifies a valid procedure or concern",
                "is_required": True,
            },
            {
                "question": "Are you located near our clinic or able to visit for an appointment?",
                "pass_criteria": "Lead confirms they can visit the clinic location",
                "is_required": True,
            },
            {
                "question": "Would you like to book a consultation appointment?",
                "pass_criteria": "Lead agrees to book or asks for available slots",
                "is_required": False,
            },
        ],
    ),

    # ── Gym / Fitness ────────────────────────────────────
    "gym_fitness": _template(
        industry="Gym & Fitness",
        greeting=(
            "Hey! 💪 Thanks for showing interest in our fitness programs. "
            "Let me find the best plan for you. Quick questions—"
        ),
        personality="energetic, motivational fitness coach",
        language="en",
        questions=[
            {
                "question": "Are you looking for a gym membership or personal training sessions?",
                "pass_criteria": "Lead indicates clear interest in membership or PT",
                "is_required": True,
            },
            {
                "question": "Is our location convenient for you? Can you visit regularly?",
                "pass_criteria": "Lead is within a reasonable distance or confirms they can commute",
                "is_required": True,
            },
            {
                "question": "Would you like to book a free trial session?",
                "pass_criteria": "Lead agrees to a trial or asks for details",
                "is_required": False,
            },
        ],
    ),

    # ── Coaching / Education ─────────────────────────────
    "coaching_education": _template(
        industry="Coaching & Education",
        greeting=(
            "Hi there! 📚 Thank you for your interest in our programs. "
            "Let me understand your goals so I can guide you to the right course."
        ),
        personality="knowledgeable, encouraging academic counselor",
        language="en",
        questions=[
            {
                "question": "Which exam or course are you preparing for?",
                "pass_criteria": "Lead names a specific exam, course, or subject area",
                "is_required": True,
            },
            {
                "question": "Are you comfortable with the course fee range? (We can discuss payment plans too.)",
                "pass_criteria": "Lead does not express inability to pay or asks about payment options",
                "is_required": True,
            },
            {
                "question": "Would you like to book a free counseling session with our faculty?",
                "pass_criteria": "Lead agrees to counseling or asks for schedule",
                "is_required": False,
            },
        ],
    ),

    # ── Interior Design ──────────────────────────────────
    "interior_design": _template(
        industry="Interior Design",
        greeting=(
            "Hello! ✨ Thanks for considering us for your interior design needs. "
            "I'd love to learn more about your project."
        ),
        personality="creative, detail-oriented design consultant",
        language="en",
        questions=[
            {
                "question": "What type of project is this? (e.g., full home, single room, office, commercial space)",
                "pass_criteria": "Lead describes a specific project type",
                "is_required": True,
            },
            {
                "question": "What is your approximate budget for this project?",
                "pass_criteria": "Budget is ≥ ₹2,00,000 (or project-specific minimum)",
                "is_required": True,
            },
            {
                "question": "Can we schedule a visit to take measurements and discuss your vision?",
                "pass_criteria": "Lead agrees to schedule or asks for availability",
                "is_required": False,
            },
        ],
    ),

    # ── Hair & Skin Clinic ───────────────────────────────
    "hair_skin_clinic": _template(
        industry="Hair & Skin Clinic",
        greeting=(
            "Hi! 💆 Thank you for reaching out to our clinic. "
            "Let me help you find the best treatment. A couple of questions—"
        ),
        personality="empathetic, professional dermatology consultant",
        language="en",
        questions=[
            {
                "question": "Which treatment are you interested in? (e.g., hair transplant, PRP, laser, skin treatment)",
                "pass_criteria": "Lead specifies a treatment or concern area",
                "is_required": True,
            },
            {
                "question": "Are you located in our city, or can you travel for the procedure?",
                "pass_criteria": "Lead confirms they can visit for treatment",
                "is_required": True,
            },
            {
                "question": "Would you like to book a consultation with our specialist?",
                "pass_criteria": "Lead agrees to consultation or asks for available slots",
                "is_required": False,
            },
        ],
    ),

    # ── Custom (blank template) ──────────────────────────
    "custom": _template(
        industry="Custom",
        greeting="Hello! Thanks for reaching out. I'd love to help you. Let me ask a few quick questions.",
        personality="friendly and professional",
        language="en",
        questions=[
            {
                "question": "Your first qualification question here",
                "pass_criteria": "Describe what a passing answer looks like",
                "is_required": True,
            },
            {
                "question": "Your second qualification question here",
                "pass_criteria": "Describe what a passing answer looks like",
                "is_required": True,
            },
            {
                "question": "Your third qualification question here (optional)",
                "pass_criteria": "Describe what a passing answer looks like",
                "is_required": False,
            },
        ],
    ),
}


def get_template(industry_key: str) -> dict[str, Any] | None:
    """Return a deep copy of the template for the given industry, or None."""
    import copy

    tpl = INDUSTRY_TEMPLATES.get(industry_key)
    return copy.deepcopy(tpl) if tpl else None


def list_industries() -> list[dict[str, str]]:
    """Return a lightweight list of available industry keys and display names."""
    return [
        {"key": key, "name": tpl["industry"]}
        for key, tpl in INDUSTRY_TEMPLATES.items()
    ]

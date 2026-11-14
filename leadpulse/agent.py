"""
Claude Qualification Agent for LeadPulse AI.

Dynamically builds an industry-agnostic system prompt from the project's
qualification_rules JSON and uses Claude 3.5 Haiku to qualify leads through
natural WhatsApp conversations.
"""

import json
import logging
from typing import Any, Optional

try:
    import anthropic
except ImportError:
    anthropic = None

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# System prompt template — fully dynamic, never hardcoded to any industry
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT_TEMPLATE = """\
You are a friendly, professional AI assistant for {company_name}. \
Your role is to have a natural WhatsApp conversation with a potential customer \
who responded to an advertisement.

{personality_block}

LANGUAGE: Respond in {language}. Match the customer's language style when possible.

GREETING (use only for the FIRST message in a conversation):
{greeting}

---

YOUR QUALIFICATION TASK:

You must determine whether this lead is genuinely interested and qualified \
by asking the following questions naturally during the conversation. \
Do NOT ask them all at once — weave them into a natural dialogue.

QUALIFICATION QUESTIONS:
{questions_block}

---

RULES:
1. Be conversational, warm, and helpful — never robotic.
2. Ask ONE question at a time. Wait for the answer before moving on.
3. If the customer goes off-topic, gently steer back.
4. If the customer is rude or clearly uninterested, politely end the conversation.
5. NEVER reveal that you are an AI unless directly asked.
6. NEVER invent information about the product/service — only use what is provided.

---

Based on the conversation so far, respond with a JSON object (and ONLY a JSON object, no markdown fencing) with these fields:
{{
  "reply_text": "Your WhatsApp reply to the customer (string)",
  "extracted_data": {{<key-value pairs of information gathered so far>}},
  "action": "CONTINUE | QUALIFY | DISQUALIFY | BOOK_APPOINTMENT",
  "lead_score": <integer 0-100>,
  "reasoning": "Brief internal note on why you chose this action"
}}

ACTION GUIDE:
- CONTINUE: You still have unanswered qualification questions.
- QUALIFY: All qualification criteria are met and the lead looks genuine.
- DISQUALIFY: The lead clearly fails one or more pass/fail criteria, or is not interested.
- BOOK_APPOINTMENT: The customer explicitly wants to book/schedule an appointment or visit.

Respond ONLY with the JSON object.\
"""


def _build_system_prompt(tenant, project) -> str:
    """
    Construct the system prompt from the project's qualification_rules JSON.

    Expected qualification_rules structure:
    {
        "greeting": "Hi! Thanks for your interest in ...",
        "personality": "Friendly and consultative",
        "language": "en",
        "questions": [
            {
                "id": "q1",
                "text": "What is your budget range?",
                "pass_criteria": "Budget >= 85 lakhs",
                "fail_criteria": "Budget below 50 lakhs",
                "required": true
            },
            ...
        ]
    }
    """
    rules: dict = project.qualification_rules or {}

    greeting = rules.get("greeting", "Hello! Thanks for reaching out to us.")
    personality = rules.get("personality", "Friendly and professional")
    language = rules.get("language", "en")
    questions = rules.get("questions", [])

    # Build personality block
    personality_block = f"PERSONALITY: {personality}"

    # Build questions block
    if questions:
        lines = []
        for i, q in enumerate(questions, 1):
            line = f"Q{i}: {q.get('text', '')}"
            if q.get("pass_criteria"):
                line += f"\n   ✅ Pass: {q['pass_criteria']}"
            if q.get("fail_criteria"):
                line += f"\n   ❌ Fail: {q['fail_criteria']}"
            if q.get("required", True):
                line += "\n   (Required)"
            lines.append(line)
        questions_block = "\n\n".join(lines)
    else:
        questions_block = (
            "No specific questions configured. "
            "Have a friendly conversation and gauge interest."
        )

    company_name = getattr(tenant, "company_name", "our company")

    return _SYSTEM_PROMPT_TEMPLATE.format(
        company_name=company_name,
        personality_block=personality_block,
        language=language,
        greeting=greeting,
        questions_block=questions_block,
    )


def _parse_claude_response(raw_text: str) -> dict[str, Any]:
    """
    Parse Claude's JSON response, handling common quirks like
    markdown code fences.
    """
    text = raw_text.strip()

    # Strip markdown fences if Claude adds them despite instructions
    if text.startswith("```"):
        # Remove opening fence (```json or ```)
        first_newline = text.index("\n")
        text = text[first_newline + 1 :]
        # Remove closing fence
        if text.endswith("```"):
            text = text[:-3].strip()

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        logger.error("Failed to parse Claude response as JSON: %s", text[:500])
        # Return a safe fallback so the conversation doesn't break
        parsed = {
            "reply_text": "I'm sorry, could you repeat that? I want to make sure I understand correctly.",
            "extracted_data": {},
            "action": "CONTINUE",
            "lead_score": 0,
            "reasoning": "JSON parse failure — asking user to repeat",
        }

    # Validate required fields with safe defaults
    parsed.setdefault("reply_text", "Thank you for your message! Let me get back to you shortly.")
    parsed.setdefault("extracted_data", {})
    parsed.setdefault("action", "CONTINUE")
    parsed.setdefault("lead_score", 0)
    parsed.setdefault("reasoning", "")

    # Clamp lead_score
    try:
        parsed["lead_score"] = max(0, min(100, int(parsed["lead_score"])))
    except (ValueError, TypeError):
        parsed["lead_score"] = 0

    # Validate action
    valid_actions = {"CONTINUE", "QUALIFY", "DISQUALIFY", "BOOK_APPOINTMENT"}
    if parsed["action"] not in valid_actions:
        logger.warning("Invalid action '%s', defaulting to CONTINUE", parsed["action"])
        parsed["action"] = "CONTINUE"

    return parsed


async def qualify_lead(
    tenant,
    project,
    lead,
    user_message: str,
    conversation_history: list[dict],
) -> dict[str, Any]:
    """
    Run a qualification step via Claude 3.5 Haiku.

    Args:
        tenant: Tenant ORM object (needs claude_api_key, company_name)
        project: Project ORM object (needs qualification_rules JSON)
        lead: Lead ORM object
        user_message: The latest inbound message from the customer
        conversation_history: List of {role, content} dicts (prior messages)

    Returns:
        Parsed dict with keys: reply_text, extracted_data, action, lead_score, reasoning
    """
    system_prompt = _build_system_prompt(tenant, project)

    # Build messages list for Claude
    messages: list[dict] = []

    # Add conversation history
    for msg in conversation_history:
        messages.append({"role": msg["role"], "content": msg["content"]})

    # Add the new user message
    messages.append({"role": "user", "content": user_message})

    # Deduplicate consecutive same-role messages (Claude requires alternating roles)
    deduped: list[dict] = []
    for msg in messages:
        if deduped and deduped[-1]["role"] == msg["role"]:
            deduped[-1]["content"] += "\n" + msg["content"]
        else:
            deduped.append(msg)

    # Ensure conversation starts with a user message
    if deduped and deduped[0]["role"] != "user":
        deduped.insert(0, {"role": "user", "content": "(conversation start)"})

    # Use the tenant's own API key or fallback to system default
    from leadpulse.config import settings

    api_key = getattr(tenant, "claude_api_key", None) or settings.CLAUDE_API_KEY
    if not api_key:
        logger.error("Neither tenant %s nor system has a Claude API key configured", getattr(tenant, "id", "unknown"))
        return {
            "reply_text": "Thank you for your message! Our team will get back to you shortly.",
            "extracted_data": {},
            "action": "CONTINUE",
            "lead_score": 0,
            "reasoning": "No Claude API key — returning fallback",
        }

    if anthropic is None:
        logger.error("Anthropic SDK is not installed — returning fallback")
        return {
            "reply_text": "Thank you for your message! Our team will get back to you shortly.",
            "extracted_data": {},
            "action": "CONTINUE",
            "lead_score": 0,
            "reasoning": "Anthropic SDK not installed",
        }

    try:
        client = anthropic.AsyncAnthropic(api_key=api_key)

        response = await client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=1024,
            system=system_prompt,
            messages=deduped,
        )

        raw_text = response.content[0].text
        logger.debug("Claude raw response for lead %s: %s", lead.id, raw_text[:300])

        parsed = _parse_claude_response(raw_text)
        logger.info(
            "Lead %s qualification step: action=%s score=%d",
            lead.id,
            parsed["action"],
            parsed["lead_score"],
        )
        return parsed

    except anthropic.APIError as exc:
        logger.error(
            "Anthropic API error for tenant %s, lead %s: %s",
            tenant.id,
            lead.id,
            exc,
        )
        return {
            "reply_text": "Thank you for your patience! Our team will follow up with you shortly.",
            "extracted_data": {},
            "action": "CONTINUE",
            "lead_score": 0,
            "reasoning": f"Anthropic API error: {exc}",
        }
    except Exception as exc:
        logger.exception(
            "Unexpected error during qualification for lead %s: %s",
            lead.id,
            exc,
        )
        return {
            "reply_text": "Thanks for your message! Someone from our team will reach out soon.",
            "extracted_data": {},
            "action": "CONTINUE",
            "lead_score": 0,
            "reasoning": f"Unexpected error: {exc}",
        }

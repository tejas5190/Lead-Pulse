"""
LeadPulse AI — Thinking Master Engine (OmniRoute Multi-Model Engine)
Provides live on-the-fly deep strategic thinking, smart prompt intake,
audience psychology analysis, bespoke ad copywriting, and Google Veo cinematic screenplay generation.
All operations run through OmniRoute using resilient provider models with zero hardcoded fallbacks.
"""
from __future__ import annotations
import json
import logging
import re
from typing import Dict, Any, List
import httpx
import json_repair

logger = logging.getLogger(__name__)

OMNIROUTE_URL = "http://127.0.0.1:20128/v1/chat/completions"
OMNIROUTE_KEY = "sk-296ab32e22eef604-04b072-4cdd0bd1"

# Priority list: fast, highly reliable multimodal/reasoning models via OmniRoute
CANDIDATE_MODELS: List[str] = [
    "antigravity/gemini-3-flash",
    "antigravity/gemini-3.1-flash-lite",
    "antigravity/claude-sonnet-4-6",
    "kr/deepseek-3.2"
]


def _extract_json(text: str) -> Dict[str, Any]:
    """Robustly extract and parse JSON from LLM response text."""
    text = text.strip()
    # Strip markdown code fence if present
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        text = text.strip()
    m = re.search(r"\{[\s\S]*\}", text)
    candidate = m.group(0) if m else text
    try:
        return json.loads(candidate)
    except Exception:
        try:
            return json_repair.loads(candidate)
        except Exception as e:
            logger.error("JSON parse failure on: %s", candidate[:500])
            raise ValueError(f"Failed to parse model JSON output: {e}") from e


async def _call_omniroute_with_fallback(messages: List[Dict[str, str]], temperature: float = 0.5, max_tokens: int = 3500) -> tuple[Dict[str, Any], str]:
    """Execute LLM call across candidate models on OmniRoute, automatically recovering from cooldowns/429s."""
    headers = {
        "Authorization": f"Bearer {OMNIROUTE_KEY}",
        "Content-Type": "application/json"
    }

    last_error = None
    for model in CANDIDATE_MODELS:
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        try:
            async with httpx.AsyncClient(timeout=45.0) as client:
                res = await client.post(OMNIROUTE_URL, json=payload, headers=headers)
                if res.status_code == 200:
                    resp_json = res.json()
                    content_text = resp_json["choices"][0]["message"]["content"]
                    parsed = _extract_json(content_text)
                    return parsed, model
                elif res.status_code == 429:
                    logger.warning("Model %s cooling down (429), switching to next model...", model)
                    last_error = f"{model} returned 429 cooling down"
                    continue
                else:
                    logger.warning("Model %s returned status %s: %s", model, res.status_code, res.text[:200])
                    last_error = f"{model} returned {res.status_code}: {res.text[:200]}"
                    continue
        except Exception as exc:
            logger.warning("Exception calling %s: %s", model, exc)
            last_error = str(exc)
            continue

    raise RuntimeError(f"All OmniRoute candidate models failed. Last error: {last_error}")


async def smart_parse_requirement(prompt: str) -> Dict[str, Any]:
    """Parse a natural language business prompt into structured campaign fields via OmniRoute."""
    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty")

    system_prompt = (
        "You are an elite marketing intake strategist and commercial creative director. "
        "Given a user's natural language business idea or ad campaign concept, extract or intelligently infer "
        "the precise campaign setup. If details like brand name, location, or price are missing, suggest creative, "
        "highly plausible, context-aware values tailored directly to that specific concept.\n\n"
        "Return ONLY a valid JSON object with NO extra text and NO markdown code fences:\n"
        "{\n"
        '  "topic": "Concise campaign theme (e.g. Artisanal Gelato & Sorbet Summer Launch)",\n'
        '  "company_name": "Inferred or creative brand name (e.g. Velvet Scoop Gelateria)",\n'
        '  "product_name": "Hero product or service offering",\n'
        '  "price_point": "Compelling offer or price (e.g. Scoops from ₹129 / Buy 2 Get 1 Free)",\n'
        '  "location": "Target neighborhood / city (e.g. Bandra West, Mumbai)",\n'
        '  "target_audience": "Specific customer persona with psychological desires",\n'
        '  "key_benefit": "Top 3 USPs separated by commas (e.g. 100% Real Fruit, Zero Preservatives, Belgian Waffle Cones)",\n'
        '  "industry": "food, retail, clinic, fitness, real_estate, ecommerce, services, or tech",\n'
        '  "tone": "high_energy, luxury, friendly, or problem_solution",\n'
        '  "suggested_cta": "Action-specific CTA with emoji (e.g. 🍨 Order on WhatsApp ➔)"\n'
        "}"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Business Requirement Prompt:\n{prompt.strip()}"}
    ]

    parsed, used_model = await _call_omniroute_with_fallback(messages, temperature=0.3, max_tokens=1500)
    parsed["engine"] = f"OmniRoute ({used_model})"
    return parsed


async def think_and_generate_campaign(
    topic: str,
    company_name: str,
    product_name: str,
    price_point: str,
    location: str,
    key_benefit: str,
    target_audience: str,
    duration: int = 15,
    quality: str = "1080p",
    tone: str = "high_energy",
) -> Dict[str, Any]:
    """Call OmniRoute to reason deeply and generate a 100% bespoke ad suite and screenplay."""

    brand = company_name.strip() or product_name.strip() or "Brand"
    prod = product_name.strip() or topic.strip() or "Offering"
    loc = location.strip() or "Your City"
    price = price_point.strip() or "Special Launch Offer"
    ben = key_benefit.strip() or "Verified Quality & Unbeatable Value"
    aud = target_audience.strip() or "Customers seeking top quality"

    system_prompt = f"""You are the LeadPulse AI Thinking Master — an elite creative director, ad copy strategist, and commercial filmmaker.
When given a business requirement, you think deeply and reason through:
1. Brand positioning & target persona psychology in {loc}.
2. Core customer friction / pain point and the emotional hook to stop the scroll on Instagram Reels and Meta Ads.
3. Why ordinary options fail and how {brand}'s {prod} solves it.
4. Google Veo 2 / Sora cinematography: lighting, lens choice, camera movement, and kinetic typography.
5. The exact high-converting Call To Action (e.g. 'Order on WhatsApp', 'Claim Offer', 'Book Now').

Generate a 100% bespoke advertising campaign tailored specifically to this business.
Return ONLY a valid JSON object with NO extra prose or markdown code fence:
{{
  "thinking_process": "3-5 sentences of your live strategic thinking, audience psychology, hook rationale, and visual metaphor",
  "brand_tagline": "short catchy brand punchline",
  "headlines": ["Headline 1 with emoji", "Headline 2", "Headline 3"],
  "primary_text": "2-sentence high-converting ad copy",
  "primary_texts": ["Angle 1 (Desire & Aspiration)", "Angle 2 (Logic & Value)", "Angle 3 (Urgency & Scarcity)"],
  "descriptions": ["Description variant 1", "Description variant 2", "Description variant 3"],
  "dynamic_cta": "Action-specific CTA with emoji and arrow (e.g. 🛒 Order on WhatsApp ➔)",
  "video_script": {{
    "hook": "Attention-grabbing hook for scroll-stopping impact (0-3s)",
    "problem": "Customer pain point / tension building (3-7s)",
    "solution": "Hero product demo with clear benefits (7-11s)",
    "cta": "Urgent call to action with scarcity (11-15s)"
  }},
  "screenplay": [
    {{
      "scene_number": 1,
      "scene_title": "The Visual Hook",
      "timestamp": "00:00 - 00:03",
      "lens_lighting": "35mm Anamorphic · High-Key Rim Light",
      "camera_motion": "Rapid Snap Zoom + Center Track",
      "veo_prompt": "Cinematic prompt describing the visual action, lighting, and camera motion specifically for this product",
      "voiceover": "Narration text for scene 1",
      "on_screen_text": "Bold text overlay for scene 1"
    }},
    {{
      "scene_number": 2,
      "scene_title": "The Customer Problem",
      "timestamp": "00:03 - 00:07",
      "lens_lighting": "50mm Prime · Dramatic Chiaroscuro Side Light",
      "camera_motion": "Slow Push-In to subject tension",
      "veo_prompt": "Cinematic prompt showing the frustration or compromise before finding the solution",
      "voiceover": "Narration text for scene 2",
      "on_screen_text": "Bold text overlay for scene 2"
    }},
    {{
      "scene_number": 3,
      "scene_title": "The Hero Product Revelation",
      "timestamp": "00:07 - 00:11",
      "lens_lighting": "85mm Macro · Warm Golden Hour Glow",
      "camera_motion": "Dynamic 360 Arc around the product in use",
      "veo_prompt": "Cinematic prompt capturing exquisite detail, vibrant texture, and high satisfaction",
      "voiceover": "Narration text for scene 3",
      "on_screen_text": "Bold text overlay for scene 3"
    }},
    {{
      "scene_number": 4,
      "scene_title": "Urgent Scarcity & Call to Action",
      "timestamp": "00:11 - 00:15",
      "lens_lighting": "24mm Wide · Neon / High-Energy Backlight",
      "camera_motion": "Fast Dolly Out to end card badge",
      "veo_prompt": "Cinematic end frame showing the final product with offer badge and dynamic text",
      "voiceover": "Narration text for scene 4",
      "on_screen_text": "Bold text overlay for scene 4"
    }}
  ],
  "full_narration": "Seamless 15-second voiceover script for Edge-TTS neural speech synthesis",
  "aspect_ratio": "9:16",
  "target_audience": "{aud}",
  "location": "{loc}"
}}"""

    user_message = f"""Requirement Details:
Company / Brand: {brand}
Topic / Concept: {topic}
Product Offering: {prod}
Price / Offer: {price}
Target City / Region: {loc}
Key Selling Points / USPs: {ben}
Target Audience: {aud}
Duration: {duration}s
Quality: {quality}
Tone: {tone}"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    parsed, used_model = await _call_omniroute_with_fallback(messages, temperature=0.7, max_tokens=4000)
    parsed["engine"] = f"OmniRoute Thinking Master ({used_model})"
    return parsed

"""
LeadPulse AI — Thinking Master Engine (OmniRoute / kr/deepseek-3.2)
Provides live on-the-fly deep strategic thinking, smart prompt intake,
audience psychology analysis, bespoke ad copywriting, and Google Veo cinematic screenplay generation.
All operations run through OmniRoute using kr/deepseek-3.2 with zero hardcoded fallbacks.
"""
from __future__ import annotations
import json
import logging
import re
from typing import Dict, Any
import httpx

logger = logging.getLogger(__name__)

OMNIROUTE_URL = "http://127.0.0.1:20128/v1/chat/completions"
OMNIROUTE_KEY = "sk-296ab32e22eef604-04b072-4cdd0bd1"
MODEL_NAME = "kr/deepseek-3.2"


def _extract_json(text: str) -> Dict[str, Any]:
    """Robustly extract and parse JSON from LLM response text."""
    text = text.strip()
    # Strip markdown code fence if present
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        text = text.strip()
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if m:
        return json.loads(m.group(0))
    return json.loads(text)


async def smart_parse_requirement(prompt: str) -> Dict[str, Any]:
    """Parse a natural language business prompt into structured campaign fields via DeepSeek-3.2."""
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

    headers = {
        "Authorization": f"Bearer {OMNIROUTE_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Business Requirement Prompt:\n{prompt.strip()}"}
        ],
        "temperature": 0.3,
        "max_tokens": 1000
    }

    async with httpx.AsyncClient(timeout=35.0) as client:
        res = await client.post(OMNIROUTE_URL, json=payload, headers=headers)
        if res.status_code != 200:
            raise RuntimeError(f"OmniRoute error ({res.status_code}): {res.text}")
        
        resp_json = res.json()
        raw_text = resp_json["choices"][0]["message"]["content"]
        parsed = _extract_json(raw_text)
        parsed["engine"] = f"OmniRoute ({MODEL_NAME})"
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
    """Call OmniRoute (kr/deepseek-3.2) to reason deeply and generate a 100% bespoke ad suite and screenplay."""

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
    "hook": "Attention-grabbing hook (0-4s)",
    "problem": "Customer pain point / tension (4-8s)",
    "solution": "Hero product reveal with price/offer (8-12s)",
    "cta": "Urgent call to action (12-15s)"
  }},
  "screenplay": [
    {{
      "scene_number": 1,
      "scene_title": "The Visual Hook",
      "timestamp": "00:00 - 00:04",
      "lens_lighting": "35mm Anamorphic · High-Key Rim Light",
      "camera_motion": "Rapid Snap Zoom + Center Track",
      "veo_prompt": "Cinematic prompt describing the visual action, lighting, and camera motion specifically for this product",
      "voiceover": "Narration text for scene 1",
      "on_screen_text": "Bold text overlay for scene 1"
    }},
    {{
      "scene_number": 2,
      "scene_title": "The Tension & Problem",
      "timestamp": "00:04 - 00:08",
      "lens_lighting": "50mm Macro · Low-Key Directional Light",
      "camera_motion": "Whip Pan Left to Right",
      "veo_prompt": "Cinematic prompt describing tension/comparison for this product",
      "voiceover": "Narration text for scene 2",
      "on_screen_text": "Bold text overlay for scene 2"
    }},
    {{
      "scene_number": 3,
      "scene_title": "The Hero Product Reveal",
      "timestamp": "00:08 - 00:12",
      "lens_lighting": "85mm Portrait f/1.4 · Golden Hour Warmth",
      "camera_motion": "Smooth 360-Degree Orbital Gimbal",
      "veo_prompt": "Hero reveal of product with glowing presentation specifically for this product",
      "voiceover": "Narration text for scene 3",
      "on_screen_text": "Bold text overlay for scene 3"
    }},
    {{
      "scene_number": 4,
      "scene_title": "The Urgent Call-To-Action",
      "timestamp": "00:12 - 00:15",
      "lens_lighting": "24mm Wide Angle · Vibrant Modern Glow",
      "camera_motion": "Slow Forward Dolly Push",
      "veo_prompt": "High-energy end card with smartphone mockup and glowing WhatsApp CTA button",
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

    headers = {
        "Authorization": f"Bearer {OMNIROUTE_KEY}",
        "Content-Type": "application/json"
    }

    req_body = {
        "model": MODEL_NAME,
        "max_tokens": 2000,
        "temperature": 0.7,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    }

    async with httpx.AsyncClient(timeout=45.0) as client:
        res = await client.post(OMNIROUTE_URL, json=req_body, headers=headers)
        if res.status_code != 200:
            raise RuntimeError(f"OmniRoute generation failed ({res.status_code}): {res.text}")

        resp_json = res.json()
        content_text = resp_json["choices"][0]["message"]["content"]
        parsed = _extract_json(content_text)
        parsed["engine"] = f"OmniRoute Thinking Master ({MODEL_NAME})"
        return parsed

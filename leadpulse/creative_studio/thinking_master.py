"""
LeadPulse AI — Thinking Master Engine (Omni-tm / OmniRoute)
Provides live on-the-fly deep strategic thinking, audience psychology analysis,
bespoke ad copywriting, and Google Veo cinematic screenplay generation.
"""
from __future__ import annotations
import json
import logging
import re
from typing import Dict, Any
import httpx

logger = logging.getLogger(__name__)

OMNIROUTE_URL = "http://localhost:20128/v1/messages"
OMNIROUTE_KEY = "sk-296ab32e22eef604-04b072-4cdd0bd1"
MODEL_NAME = "Omni-tm"


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
    """Call the Omni-tm Thinking Master to reason through and generate a bespoke campaign."""

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

Generate a bespoke advertising campaign tailored specifically to this business.
Return ONLY a valid JSON object with NO extra prose or markdown code fence:
{{
  "thinking_process": "3-5 sentences of your live strategic thinking, audience psychology, hook rationale, and visual metaphor",
  "brand_tagline": "short catchy brand punchline",
  "headlines": ["Headline 1 with emoji", "Headline 2", "Headline 3"],
  "primary_text": "2-sentence high-converting ad copy",
  "dynamic_cta": "Action-specific CTA with emoji and arrow (e.g. 🛒 Order Now on WhatsApp ➔)",
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
      "veo_prompt": "Cinematic prompt describing the visual action, lighting, and camera motion",
      "voiceover": "Narration text for scene 1",
      "on_screen_text": "Bold text overlay for scene 1"
    }},
    {{
      "scene_number": 2,
      "scene_title": "The Tension & Problem",
      "timestamp": "00:04 - 00:08",
      "lens_lighting": "50mm Macro · Low-Key Directional Light",
      "camera_motion": "Whip Pan Left to Right",
      "veo_prompt": "Cinematic prompt describing tension/comparison",
      "voiceover": "Narration text for scene 2",
      "on_screen_text": "Bold text overlay for scene 2"
    }},
    {{
      "scene_number": 3,
      "scene_title": "The Hero Product Reveal",
      "timestamp": "00:08 - 00:12",
      "lens_lighting": "85mm Portrait f/1.4 · Golden Hour Warmth",
      "camera_motion": "Smooth 360-Degree Orbital Gimbal",
      "veo_prompt": "Hero reveal of product with glowing badges and pristine presentation",
      "voiceover": "Narration text for scene 3",
      "on_screen_text": "Bold text overlay for scene 3"
    }},
    {{
      "scene_number": 4,
      "scene_title": "The Urgent Call-To-Action",
      "timestamp": "00:12 - 00:15",
      "lens_lighting": "24mm Wide Angle · Neon Cyber Glow",
      "camera_motion": "Slow Forward Dolly Push",
      "veo_prompt": "High-energy end card with smartphone mockup and glowing WhatsApp CTA button",
      "voiceover": "Narration text for scene 4",
      "on_screen_text": "Bold text overlay for scene 4"
    }}
  ],
  "full_narration": "Seamless 15-second voiceover script for Edge-TTS neural speech synthesis",
  "aspect_ratio": "1:1",
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
        "x-api-key": OMNIROUTE_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    req_body = {
        "model": MODEL_NAME,
        "max_tokens": 1500,
        "temperature": 0.7,
        "messages": [
            {"role": "user", "content": f"{system_prompt}\n\n{user_message}"}
        ]
    }

    try:
        async with httpx.AsyncClient(timeout=25.0) as client:
            res = await client.post(OMNIROUTE_URL, json=req_body, headers=headers)
            if res.status_code == 200:
                resp_json = res.json()
                content_text = resp_json.get("content", [{}])[0].get("text", "")
                m = re.search(r"\{.*\}", content_text, re.DOTALL)
                if m:
                    parsed = json.loads(m.group(0))
                    parsed["engine"] = "Thinking Master (Omni-tm)"
                    return parsed
    except Exception as e:
        logger.warning(f"Thinking Master OmniRoute call failed, using dynamic generator: {e}")

    # Resilient dynamic fallback tailored specifically to the input
    from .copywriter import generate_ad_copy
    fallback_data = generate_ad_copy(
        product_name=prod,
        company_name=brand,
        topic=topic,
        price_point=price,
        location=loc,
        key_benefit=ben,
        target_audience=aud,
        duration=duration,
        quality=quality,
        tone=tone,
    )
    fallback_data["thinking_process"] = (
        f"Analyzed {brand}'s positioning for {prod} in {loc}. "
        f"Focused the strategy on {ben} with an immediate {price} offer. "
        f"Designed dynamic video reel hooks to drive maximum click-through rates directly to WhatsApp."
    )
    fallback_data["engine"] = "LeadPulse Dynamic Generative Engine"
    return fallback_data

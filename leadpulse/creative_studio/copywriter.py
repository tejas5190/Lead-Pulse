"""
LeadPulse AI — Creative Studio Copywriter Engine
Generates dynamic high-converting Meta Ad primary text, headlines, descriptions,
and multi-scene Google Veo / Sora screenplays for any business topic.
"""
from __future__ import annotations
from typing import Dict, Any, List


def generate_ad_copy(
    product_name: str,
    company_name: str = "",
    topic: str = "",
    industry: str = "universal",
    price_point: str = "Competitive Pricing",
    location: str = "Your City",
    key_benefit: str = "Premium Quality & Fast Delivery",
    target_audience: str = "Discerning customers",
    duration: int = 15,
    quality: str = "1080p",
    tone: str = "high_energy",
    claude_api_key: str = None
) -> Dict[str, Any]:
    """Generate dynamic high-CTR Meta Ad copy variants & Google Veo screenplays on demand."""
    
    brand = company_name.strip() if company_name else product_name
    prod = product_name.strip() if product_name else "Exclusive Collection"
    subject = topic.strip() if topic else prod
    loc = location.strip() if location else "your area"
    price = price_point.strip() if price_point else "Introductory Offer"
    ben = key_benefit.strip() if key_benefit else "Guaranteed Results & Uncompromised Quality"
    aud = target_audience.strip() if target_audience else "customers looking for the best"

    # Tone adjustments
    if tone == "luxury":
        h_prefix = ["The Art of", "Unrivaled Elegance:", "Redefining Luxury:"]
        v_mood = "Cinematic slow-motion 4K macro shot, dramatic chiaroscuro lighting, shallow depth of field (f/1.4, 85mm anamorphic), deep obsidian and warm metallic gold tones."
        cta_verb = "Request Private VIP Invitation"
    elif tone == "problem_solution":
        h_prefix = ["Why Settle When", "The Problem With Ordinary", "Finally, A Better Way:"]
        v_mood = "Sharp dynamic transition, high-contrast editorial lighting, 35mm crisp commercial lens, candid documentary realism shifting to glowing polished finish."
        cta_verb = "See The Transformation on WhatsApp"
    elif tone == "friendly":
        h_prefix = ["Meet", "Your New Favorite", "Why Everyone in " + loc + " Loves"]
        v_mood = "Warm natural daylight, handheld tracking shot, cheerful organic atmosphere, vibrant natural color grading."
        cta_verb = "Say Hi on WhatsApp"
    else:  # high_energy (default)
        h_prefix = ["Stop Wasting Money On", "Transform Your Results With", "Limited Launch Offer:"]
        v_mood = "Fast dynamic zoom-in, electric neon rim lighting, high-speed 60fps slow-motion capture, energetic motion blur with crisp product isolation."
        cta_verb = "Claim Launch Offer on WhatsApp"

    # 1. Dynamic CTR Headlines
    headlines = [
        f"{h_prefix[0]} {prod} | {price}",
        f"{h_prefix[1]} {subject} @ {loc}",
        f"Get {ben.split(',')[0]} With {brand} Today"
    ]

    # 2. Dynamic Primary Texts (Angle 1: Desire, Angle 2: Logic/ROI, Angle 3: Urgency)
    primary_texts = [
        # Angle 1: Desire & Aspiration
        f"✨ Experience the difference with {prod} by {brand}.\n\n"
        f"Designed specifically for {aud}, this is your opportunity to upgrade without compromise.\n\n"
        f"💎 {price}\n"
        f"📍 Available in {loc}\n"
        f"⭐ {ben}\n\n"
        f"👉 Tap WhatsApp below to get the exclusive brochure and introductory pricing directly on your phone.",

        # Angle 2: Rational / Comparison / ROI
        f"💡 Why settle for ordinary {subject} when you can get direct access to {brand}?\n\n"
        f"✔️ Transparent Pricing: {price}\n"
        f"✔️ Proven Benefits: {ben}\n"
        f"✔️ 100% Satisfaction & Verified Quality\n\n"
        f"Join hundreds of satisfied clients in {loc}. Tap below to speak directly with our team on WhatsApp in 30 seconds.",

        # Angle 3: Scarcity & Urgent Launch Window
        f"⏳ LIMITED OPPORTUNITY: Exclusive launch packages for {prod} are now live for {loc}.\n\n"
        f"🔒 Lock in special pricing at {price} before rates adjust.\n"
        f"⚡ {ben}\n\n"
        f"Click WhatsApp below right now to secure your spot before this week's allocation fills up."
    ]

    descriptions = [
        f"{brand} Official · Instant WhatsApp Response",
        f"Verified Quality · {price} · {loc}",
        f"Limited Allocation This Week · Inquire Now"
    ]

    # 3. Google Veo 2 / Sora Screenplay Generator
    screenplay: List[Dict[str, Any]] = []

    if duration <= 15:
        # 15-Second Blitz Reel (4 scenes)
        screenplay = [
            {
                "scene_number": 1,
                "timecode": "00:00 - 00:03",
                "scene_title": "The Visual Hook",
                "veo_prompt": f"{v_mood} Camera pulls back rapidly revealing {subject} centered in frame with glowing atmospheric mist. Text pops with kinetic energy.",
                "camera_movement": "Rapid Snap-Zoom + Center Track",
                "on_screen_text": f"Tired of Average {subject}?",
                "voiceover": f"Still searching for the best {subject} in {loc}?",
                "sound_fx": "Deep sub-bass riser with crisp whoosh transition"
            },
            {
                "scene_number": 2,
                "timecode": "00:03 - 00:07",
                "scene_title": "The Agitation",
                "veo_prompt": f"Gritty high-speed macro details of common industry frustrations, rapid shutter flicker, transitioning abruptly into sleek polished glass.",
                "camera_movement": "Whip Pan Left to Right",
                "on_screen_text": "Most options cut corners.",
                "voiceover": f"Most alternatives overcharge and underdeliver on quality.",
                "sound_fx": "Vinyl scratch transition into energetic rhythmic beat"
            },
            {
                "scene_number": 3,
                "timecode": "00:07 - 00:12",
                "scene_title": "The Solution & Hero Showcase",
                "veo_prompt": f"Hero 360-degree orbit shot around {prod}. Pristine highlights glint across edges. Floating modern holographic badge reveals '{price}'.",
                "camera_movement": "Smooth 360-Degree Drone Orbit",
                "on_screen_text": f"{prod} · {price}",
                "voiceover": f"Meet {prod} from {brand}. Starting at just {price}, with {ben}.",
                "sound_fx": "Lush uplifting synth drop with crisp sparkle chime"
            },
            {
                "scene_number": 4,
                "timecode": "00:12 - 00:15",
                "scene_title": "The Urgent CTA",
                "veo_prompt": f"Vibrant WhatsApp green glow pulses around a sleek 3D smartphone mockup. Floating countdown timer and glowing direct message button.",
                "camera_movement": "Gentle Forward Push to Screen",
                "on_screen_text": "👉 Tap WhatsApp to Claim Offer",
                "voiceover": f"Tap WhatsApp below right now to claim your exclusive launch voucher!",
                "sound_fx": "Satisfying iPhone message pop chime"
            }
        ]
    elif duration <= 30:
        # 30-Second Standard Meta Ad (6 scenes)
        screenplay = [
            {
                "scene_number": 1,
                "timecode": "00:00 - 00:04",
                "scene_title": "The Pattern Interrupt",
                "veo_prompt": f"{v_mood} An unexpected extreme close-up of {subject}. Subtle smoke and dramatic rim lighting create instant curiosity.",
                "camera_movement": "Slow Cinematic Dolly-In",
                "on_screen_text": f"This changes everything about {subject}.",
                "voiceover": f"If you live in {loc} and care about quality, you need to see this.",
                "sound_fx": "Subtle cinematic heartbeat with ambient drone"
            },
            {
                "scene_number": 2,
                "timecode": "00:04 - 00:09",
                "scene_title": "The Unspoken Problem",
                "veo_prompt": f"Split screen or fast montage showing the hassle, hidden fees, and frustration people experience with ordinary {subject}.",
                "camera_movement": "Fast Editorial Cuts with Glitch Accent",
                "on_screen_text": "Why is it so hard to find true quality?",
                "voiceover": f"Why is it so frustrating to find {subject} that actually delivers what is promised?",
                "sound_fx": "Tension build with muted percussive ticks"
            },
            {
                "scene_number": 3,
                "timecode": "00:09 - 00:15",
                "scene_title": "The Breakthrough Revelation",
                "veo_prompt": f"A breathtaking reveal of {prod} in pristine studio lighting. The brand logo of {brand} shines subtly.",
                "camera_movement": "Hero Pedestal Rise from Low Angle",
                "on_screen_text": f"Introducing {brand}",
                "voiceover": f"That's why {brand} created {prod}. Engineered from the ground up for {aud}.",
                "sound_fx": "Full orchestral swell into driving commercial rhythm"
            },
            {
                "scene_number": 4,
                "timecode": "00:15 - 00:20",
                "scene_title": "Core Craftsmanship & Benefits",
                "veo_prompt": f"Dynamic macro sequence highlighting: {ben}. 4K crisp textures and smooth fluid motion graphics overlaying key specifications.",
                "camera_movement": "Fluid Macro Tracking Pan",
                "on_screen_text": f"✔ {ben}",
                "voiceover": f"You get unmatched craftsmanship: {ben}, backed by our 100% satisfaction guarantee.",
                "sound_fx": "Clean rhythmic bassline with subtle high-hat accents"
            },
            {
                "scene_number": 5,
                "timecode": "00:20 - 00:25",
                "scene_title": "The Unbeatable Offer",
                "veo_prompt": f"Glowing neon card displays the launch package. A bold price pill flashes '{price}' with zero hidden surprises.",
                "camera_movement": "Slow Lateral Track Right",
                "on_screen_text": f"Starting from {price}",
                "voiceover": f"And for a limited time, packages start at just {price} with zero middleman markups.",
                "sound_fx": "Positive chime riser with upbeat chord progression"
            },
            {
                "scene_number": 6,
                "timecode": "00:25 - 00:30",
                "scene_title": "The Final Call To Action",
                "veo_prompt": f"High-contrast end card with WhatsApp logo, direct chat prompt, and limited availability ticker: 'Only in {loc}'.",
                "camera_movement": "Slow Static Hold with Subtle Pulse",
                "on_screen_text": "💬 Tap WhatsApp Below · Instant Response",
                "voiceover": f"Tap the WhatsApp button below now to lock in your introductory rate before spots fill up!",
                "sound_fx": "Resonant final bass impact with double message notification"
            }
        ]
    else:
        # 60-Second Long-Form Explainer (8 scenes)
        screenplay = [
            {
                "scene_number": 1,
                "timecode": "00:00 - 00:06",
                "scene_title": "Cinematic Teaser",
                "veo_prompt": f"{v_mood} Atmospheric wide shot transitioning into intense macro focus on {subject}. Golden hour atmosphere in {loc}.",
                "camera_movement": "Crane Down + Slow Push Forward",
                "on_screen_text": f"The New Standard in {subject}",
                "voiceover": f"For years, {aud} have been forced to accept compromise when it comes to {subject}.",
                "sound_fx": "Atmospheric cinematic pad with distant city drone"
            },
            {
                "scene_number": 2,
                "timecode": "00:06 - 00:14",
                "scene_title": "The Conflict & Reality Check",
                "veo_prompt": f"Realistic documentary-style footage illustrating common pitfalls: high costs, delays, poor materials, and broken promises.",
                "camera_movement": "Handheld Tracking Shot with Natural Motion",
                "on_screen_text": "Broken Promises & Inflated Costs",
                "voiceover": f"Most providers cut corners on materials, hide extra fees, and disappear when you need support.",
                "sound_fx": "Subtle dissonant strings building suspense"
            },
            {
                "scene_number": 3,
                "timecode": "00:14 - 00:22",
                "scene_title": f"The Vision Behind {brand}",
                "veo_prompt": f"Behind-the-scenes master craftsmanship: hands precision-assembling, measuring, and testing {prod} to absolute perfection.",
                "camera_movement": "Smooth Slider Pan across Worktable",
                "on_screen_text": f"Crafted Without Compromise",
                "voiceover": f"At {brand}, we decided to change that. We set out to create {prod} with one uncompromising goal: perfection.",
                "sound_fx": "Deep acoustic piano chords enter with warm cello"
            },
            {
                "scene_number": 4,
                "timecode": "00:22 - 00:30",
                "scene_title": "The Key Differentiator",
                "veo_prompt": f"Crystal-clear 4K demonstration showcasing: {ben}. Micro-animations explain why it outperforms traditional alternatives.",
                "camera_movement": "Architectural 3D Pan with Motion Callouts",
                "on_screen_text": f"The Breakthrough: {ben}",
                "voiceover": f"Here is what sets us apart: {ben}. Every detail is engineered for lasting reliability.",
                "sound_fx": "Uplifting rhythmic pulse begins driving momentum"
            },
            {
                "scene_number": 5,
                "timecode": "00:30 - 00:38",
                "scene_title": "Customer Transformation",
                "veo_prompt": f"Genuine happy clients in {loc} experiencing the real results. Radiant smiles, modern environments, five-star review badges.",
                "camera_movement": "Slow Orbit around Satisfied Customer",
                "on_screen_text": "⭐⭐⭐⭐⭐ Rated 4.9/5 by Clients",
                "voiceover": f"That is why our clients consistently rate us 4.9 stars and recommend us to their friends and colleagues.",
                "sound_fx": "Bright percussive energy with melodic synth accents"
            },
            {
                "scene_number": 6,
                "timecode": "00:38 - 00:46",
                "scene_title": "Risk-Free Guarantee",
                "veo_prompt": f"3D security shield and verified guarantee seal stamp onto a pristine glass certificate.",
                "camera_movement": "Center Lock with Radial Light Rays",
                "on_screen_text": "100% Satisfaction & Warranty",
                "voiceover": f"Plus, your decision is protected with our complete guarantee and transparent pricing.",
                "sound_fx": "Confident metallic click with warm bass sweep"
            },
            {
                "scene_number": 7,
                "timecode": "00:46 - 00:54",
                "scene_title": "The Exclusive Launch Offer",
                "veo_prompt": f"Exclusive VIP invite envelope opens, unveiling introductory rate '{price}' with limited edition perks.",
                "camera_movement": "Elegant Macro Tilt Down",
                "on_screen_text": f"Packages from {price}",
                "voiceover": f"For our upcoming launch batch in {loc}, packages start from just {price} with zero middleman markup.",
                "sound_fx": "Celebratory musical swell reaching climax"
            },
            {
                "scene_number": 8,
                "timecode": "00:54 - 00:60",
                "scene_title": "The Direct WhatsApp Call to Action",
                "veo_prompt": f"High-impact final screen with clickable WhatsApp interface, QR code, and countdown timer: 'Offer Expires Soon'.",
                "camera_movement": "Direct Push to Center Action Button",
                "on_screen_text": "👉 Tap WhatsApp to Book Your Consultation",
                "voiceover": f"Click the WhatsApp button right below this video to speak with our specialists and claim your package today!",
                "sound_fx": "Signature WhatsApp send chime with lingering warm chord"
            }
        ]

    # Full narration text for voice synthesis
    full_narration = " ".join(scene["voiceover"] for scene in screenplay)

    # Simplified video_script object for backward compatibility
    video_script = {
        "hook": screenplay[0]["voiceover"],
        "problem": screenplay[1]["voiceover"],
        "solution": screenplay[2]["voiceover"] if len(screenplay) > 2 else screenplay[-1]["voiceover"],
        "cta": screenplay[-1]["voiceover"]
    }

    return {
        "product_name": prod,
        "company_name": brand,
        "topic": subject,
        "industry": industry,
        "primary_texts": primary_texts,
        "headlines": headlines,
        "descriptions": descriptions,
        "call_to_action": cta_verb,
        "video_script": video_script,
        "screenplay": screenplay,
        "duration": duration,
        "quality": quality,
        "tone": tone,
        "full_narration": full_narration
    }

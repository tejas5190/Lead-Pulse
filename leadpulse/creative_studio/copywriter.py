"""
LeadPulse AI — Creative Studio Copywriter Engine
Generates high-converting Meta Ad primary text, headlines, descriptions,
and short video scripts for any business vertical.
"""
from typing import Dict, Any, List
import json


DEFAULT_TEMPLATES = {
    "real_estate": {
        "primary_texts": [
            "🏡 Tired of endless traffic and congested apartments? Step into {product_name} — luxury living designed for families who want more space, fresh air, and peace of mind.\n\n✨ Premium {price_point}\n📍 Prime Location: {location}\n🌿 {key_benefit}\n\n👉 Click 'WhatsApp' below to receive the complete floor plan & price breakdown directly on your phone.",
            "💰 Why pay rent or middleman commissions when you can own luxury directly from the developer? {product_name} is now open for private VIP viewings.\n\n✔️ {price_point}\n✔️ Direct Developer Pricing (Zero Brokerage)\n✔️ {key_benefit}\n\nTap below to chat with our property advisory team on WhatsApp.",
            "⏳ URGENT: Only a few prime units remain in Phase 1 of {product_name}. Prices are set to revise by 8% next month.\n\n🔒 Lock in pre-launch pricing at {price_point}.\n📍 {location}\n\nBook your private sample flat visit this weekend before slots fill up."
        ],
        "headlines": [
            "Luxury 3BHK Homes from {price_point} | Zero Brokerage",
            "Exclusive Sample Flat Open This Saturday @ {location}",
            "Save Up To ₹5 Lakhs on Pre-Launch Bookings Today"
        ],
        "descriptions": [
            "Direct Developer Offer · Instant WhatsApp Brochure",
            "RERA Approved · 80% Green Open Spaces",
            "Limited Phase 1 Inventory · Book Your VIP Slot"
        ],
        "video_script": {
            "hook": "Still looking for your dream home in {location} without paying crazy broker fees?",
            "problem": "Most apartments give you small rooms and noisy neighborhoods.",
            "solution": "Introducing {product_name}. Spacious luxury layouts starting at just {price_point}. {key_benefit}.",
            "cta": "Tap the WhatsApp button below now to get the instant brochure and book your VIP site visit!"
        }
    },
    "dental": {
        "primary_texts": [
            "✨ Stop hiding your smile! Experience pain-free dental care and laser teeth alignment with {product_name}.\n\n💎 {price_point}\n📍 {location}\n🩺 {key_benefit}\n\nTap below to claim your complimentary dental scan & consultation on WhatsApp.",
            "🦷 Missing teeth or crooked smile? Transform your confidence in just 2 sittings at {product_name}.\n\n✔️ Packages from {price_point}\n✔️ 0% EMI Available\n\nClick below to book your appointment on WhatsApp in 30 seconds.",
            "⏳ Limited Weekend Slots: Book your 3D digital dental scan at {product_name} before appointments fill up.\n\n🔒 Starting at {price_point} with 0% interest monthly payment options.\n📍 {location}\n\nTap WhatsApp to claim your special introductory voucher today."
        ],
        "headlines": [
            "Transform Your Smile From {price_point} | Free Consultation",
            "Pain-Free Dental Implants & Aligners @ {location}",
            "Book Your 3D Dental Scan on WhatsApp Today"
        ],
        "descriptions": [
            "Top Rated Dental Specialists · 0% EMI",
            "Pain-Free Technology · 10,000+ Happy Smiles",
            "Limited Slots This Week · Book Now"
        ],
        "video_script": {
            "hook": "Want a perfect, confident smile without the pain or high hospital bills?",
            "problem": "Traditional braces take years and cost a fortune.",
            "solution": "At {product_name}, our modern clear aligners and painless dental care start at just {price_point}. {key_benefit}.",
            "cta": "Click the WhatsApp button below right now to claim your free consultation!"
        }
    },
    "fitness": {
        "primary_texts": [
            "🔥 Ready to get in the best shape of your life? Join {product_name} and get a custom workout + nutrition plan tailored to your body type.\n\n⚡ Membership starting at {price_point}\n📍 {location}\n🏋️ {key_benefit}\n\nTap WhatsApp to claim your Free 3-Day Trial Pass today!",
            "💪 Don't wait until next year to fix your health. Work with certified personal trainers at {product_name}.\n\n✔️ Only {price_point}\n✔️ Guaranteed Results in 90 Days\n\nClaim your trial pass on WhatsApp now.",
            "⚡ Flash Launch Offer: The first 25 sign-ups this month get free body composition analysis and zero admission fee at {product_name}.\n\n📍 {location} | Starting at {price_point}\n\nClick below to lock in your discounted membership on WhatsApp."
        ],
        "headlines": [
            "Get In Peak Shape from {price_point} | Free 3-Day Pass",
            "Elite Personal Training & Nutrition @ {location}",
            "Join {product_name} Today · Zero Registration Fee"
        ],
        "descriptions": [
            "Certified Trainers · State-of-the-art Equipment",
            "Custom Diet & Workout Plans Included",
            "Claim Your Free Session on WhatsApp"
        ],
        "video_script": {
            "hook": "Tired of starting fitness programs and quitting after two weeks?",
            "problem": "Generic workouts don't work without personal guidance.",
            "solution": "Join {product_name}. Our certified coaches give you 1-on-1 guidance starting at {price_point}. {key_benefit}.",
            "cta": "Click the WhatsApp button below to get your free 3-day pass today!"
        }
    },
    "universal": {
        "primary_texts": [
            "🚀 Elevate your results with {product_name}. Designed for customers who value premium quality, reliability, and guaranteed performance.\n\n💎 {price_point}\n📍 {location}\n⭐ {key_benefit}\n\nTap WhatsApp to chat with our team directly and claim exclusive promotional pricing.",
            "🎯 Why settle for less when you can get the best in class with {product_name}?\n\n✔️ Starting at {price_point}\n✔️ {key_benefit}\n\nClick the button below to connect with our specialists on WhatsApp.",
            "⏳ Limited Opportunity: Take advantage of our exclusive seasonal pricing for {product_name}.\n\n⭐ {price_point}\n📍 {location}\n\nTap WhatsApp below to speak with an advisor and claim your special rate."
        ],
        "headlines": [
            "Special Launch Offer Starting at {price_point}",
            "Premium Quality & Guaranteed Results @ {location}",
            "Chat With Us on WhatsApp for Instant Booking"
        ],
        "descriptions": [
            "Direct Provider Offer · Instant Response",
            "Limited Time Promotion · Zero Risk",
            "100% Satisfaction Guaranteed"
        ],
        "video_script": {
            "hook": "Looking for the highest quality {product_name} without overpaying?",
            "problem": "Most options in the market are overpriced or deliver poor results.",
            "solution": "We deliver premium quality starting from {price_point}. {key_benefit}.",
            "cta": "Tap the WhatsApp button below now for instant details and VIP support!"
        }
    }
}


def generate_ad_copy(
    product_name: str,
    industry: str = "real_estate",
    price_point: str = "Competitive Pricing",
    location: str = "Your City",
    key_benefit: str = "Top Quality & Fast Delivery",
    target_audience: str = "Prospective buyers",
    claude_api_key: str = None
) -> Dict[str, Any]:
    """Generate high-CTR Meta Ad copy variants & video scripts."""
    tmpl = DEFAULT_TEMPLATES.get(industry) or DEFAULT_TEMPLATES.get("universal")
    
    # Format templates with parameters
    primary_texts = [
        t.format(
            product_name=product_name,
            price_point=price_point,
            location=location,
            key_benefit=key_benefit,
            target_audience=target_audience
        )
        for t in tmpl["primary_texts"]
    ]
    
    headlines = [
        h.format(
            product_name=product_name,
            price_point=price_point,
            location=location
        )
        for h in tmpl["headlines"]
    ]
    
    descriptions = [
        d.format(
            product_name=product_name,
            price_point=price_point,
            location=location
        )
        for d in tmpl["descriptions"]
    ]
    
    vs = tmpl["video_script"]
    script_obj = {
        "hook": vs["hook"].format(product_name=product_name, location=location, price_point=price_point),
        "problem": vs["problem"].format(product_name=product_name, location=location, price_point=price_point),
        "solution": vs["solution"].format(product_name=product_name, location=location, price_point=price_point, key_benefit=key_benefit),
        "cta": vs["cta"].format(product_name=product_name, location=location, price_point=price_point),
    }
    
    # Full narration text for TTS
    full_narration = f"{script_obj['hook']} {script_obj['problem']} {script_obj['solution']} {script_obj['cta']}"
    
    return {
        "product_name": product_name,
        "industry": industry,
        "primary_texts": primary_texts,
        "headlines": headlines,
        "descriptions": descriptions,
        "call_to_action": "Send WhatsApp Message",
        "video_script": script_obj,
        "full_narration": full_narration
    }

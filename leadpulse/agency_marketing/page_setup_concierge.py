"""
LeadPulse AI — Done-For-You Business Page Setup Concierge
Generates complete SEO-optimized profiles, bios, WhatsApp deep-links,
and 5-minute setup guides for non-tech business owners.
"""
from typing import Dict, Any
import urllib.parse


def generate_business_page_setup(
    business_name: str,
    industry: str,
    location: str,
    phone_number: str,
    key_offer: str
) -> Dict[str, Any]:
    """Generate complete social page setup kit for non-tech clients."""
    clean_phone = phone_number.replace("+", "").replace(" ", "").replace("-", "")
    
    # Pre-filled WhatsApp message for lead tracking
    wa_msg = f"Hi! Saw your Instagram page. I would like to know more about {key_offer}."
    encoded_msg = urllib.parse.quote(wa_msg)
    wa_direct_link = f"https://wa.me/{clean_phone}?text={encoded_msg}"

    if industry == "dental":
        ig_name = f"{business_name} | Clear Aligners & Dental"
        ig_category = "Dentist & Dental Clinic"
        ig_bio = (
            f"✨ Painless Laser Dentistry & Invisible Aligners\n"
            f"📍 {location}\n"
            f"⭐ 10,000+ Happy Confident Smiles\n"
            f"🎁 Special: {key_offer}\n"
            f"👇 Tap below to book your appointment in 30 seconds"
        )
        fb_about = (
            f"Welcome to {business_name}, {location}'s premier center for advanced painless dentistry, "
            f"clear aligners, and cosmetic smile makeovers. We combine 3D digital scanning with gentle "
            f"laser technology for zero-pain dental care. Enjoy 0% EMI payment options and a complimentary "
            f"initial consultation. Message us directly on WhatsApp for instant booking."
        )
        highlights = ["Smile Tours", "Results / B&A", "Our Doctors", "Clear Aligners", "Pricing & EMI"]
    elif industry == "real_estate":
        ig_name = f"{business_name} | Luxury Homes & Villas"
        ig_category = "Real Estate Developer"
        ig_bio = (
            f"🏡 Premium Residential & Commercial Properties\n"
            f"📍 {location}\n"
            f"🔑 Direct Developer Bookings · Zero Brokerage\n"
            f"🌟 {key_offer}\n"
            f"👇 Click below for instant floor plans & VIP pricing"
        )
        fb_about = (
            f"{business_name} is a leading luxury real estate brand in {location}. We craft high-end "
            f"living spaces with 80% green open areas, smart home automation, and world-class clubhouses. "
            f"Connect directly with our property advisory desk on WhatsApp for brochure downloads and "
            f"private sample flat viewings."
        )
        highlights = ["Sample Flat", "Floor Plans", "Amenities", "Location Map", "VIP Offers"]
    elif industry == "fitness":
        ig_name = f"{business_name} | Fitness & Transformation"
        ig_category = "Gym / Fitness Center"
        ig_bio = (
            f"🔥 Science-backed Body Transformations\n"
            f"📍 {location}\n"
            f"🏋️ Personal Training · Nutrition Plans · Elite Gym\n"
            f"⚡ {key_offer}\n"
            f"👇 Claim your Free 3-Day Pass on WhatsApp"
        )
        fb_about = (
            f"Transform your strength and physique at {business_name}, {location}. Equipped with world-class "
            f"strength machinery, certified trainers, and personalized nutrition coaching. Claim your free "
            f"guest trial pass via WhatsApp today."
        )
        highlights = ["Transformations", "Gym Tour", "Workouts", "Trainers", "Diet Plans"]
    else:
        ig_name = f"{business_name} | Official"
        ig_category = "Local Business / Service"
        ig_bio = (
            f"⭐ Premium Quality Products & Trusted Service\n"
            f"📍 {location}\n"
            f"💎 100% Customer Satisfaction Guaranteed\n"
            f"🎁 {key_offer}\n"
            f"👇 Tap to chat with our team on WhatsApp"
        )
        fb_about = (
            f"{business_name} provides industry-leading products and customer service in {location}. "
            f"Dedicated to quality, speed, and customer satisfaction. Chat with our customer support "
            f"team directly on WhatsApp."
        )
        highlights = ["About Us", "Top Products", "Reviews", "Offers", "Contact Us"]

    checklist = [
        {"step": 1, "title": "Switch Instagram to Professional Account", "detail": "Open Instagram App → Settings → Account Type → Switch to Professional Account (Choose Category: '" + ig_category + "')."},
        {"step": 2, "title": "Paste the High-Converting Bio", "detail": "Tap 'Edit Profile' → Paste the generated bio and set the Website link to your direct WhatsApp booking URL."},
        {"step": 3, "title": "Connect WhatsApp Business Button", "detail": "Under 'Public Business Information' → Contact Options → Add your WhatsApp number so clients see a direct 'WhatsApp' button on your profile."},
        {"step": 4, "title": "Setup Facebook Page & Link Accounts", "detail": "Create Page on facebook.com/pages/create with the provided About text, then link your Instagram account under Page Settings → Linked Accounts."},
        {"step": 5, "title": "Turn on Auto-Reply Greeting", "detail": "In Meta Business Suite app → Inbox → Automated Responses → Turn on 'Instant Reply' with your LeadPulse AI WhatsApp link."}
    ]

    return {
        "business_name": business_name,
        "industry": industry,
        "location": location,
        "instagram": {
            "name_field": ig_name,
            "category": ig_category,
            "bio": ig_bio,
            "website_link": wa_direct_link,
            "recommended_highlights": highlights
        },
        "facebook": {
            "page_name": business_name,
            "category": ig_category,
            "about": fb_about,
            "call_to_action_button": "Send WhatsApp Message",
            "whatsapp_link": wa_direct_link
        },
        "non_tech_checklist": checklist
    }

"""
LeadPulse AI — 30-Day Audience Building & Launch Strategy Planner
Generates a complete day-by-day organic & paid marketing roadmap
across 4 distinct psychological marketing phases.
"""
from typing import Dict, Any, List


def generate_30_day_strategy(
    business_name: str,
    industry: str,
    location: str,
    target_audience: str,
    key_offer: str
) -> Dict[str, Any]:
    """Generate structured 30-day marketing calendar with ready-to-post creatives & briefs."""
    
    phases = [
        {"name": "Phase 1: Authority & Awareness", "days": "Days 1–7", "goal": "Build local credibility, introduce the expert/brand, and highlight the core customer problem."},
        {"name": "Phase 2: Social Proof & Objection Handling", "days": "Days 8–14", "goal": "Showcase transformations, debunk common myths, and dismantle hesitation on price and pain."},
        {"name": "Phase 3: Pre-Launch Hype & Engagement", "days": "Days 15–21", "goal": "Tease the exclusive launch offer, build a VIP waitlist, and run interactive polls to prime buyers."},
        {"name": "Phase 4: Paid Meta Ad Blitz & Conversion", "days": "Days 22–30", "goal": "Activate Click-To-WhatsApp Meta Ads, retarget engaged followers, and convert high-ticket clients."}
    ]

    days_data = []

    # Dynamic templates based on industry
    if industry == "dental":
        daily_blueprints = [
            # Week 1
            (1, "Phase 1", "Reel (9:16)", "Meet Your New Smile Doctor in {location}", "Behind-the-scenes clinic tour and meet the doctor who prioritizes zero pain.", "Photorealistic video: Camera tracks through modern dental lounge with warm ambient lighting", "Save this post", "7:30 PM"),
            (2, "Phase 1", "Carousel (1080x1350)", "3 Signs You Might Need Clear Aligners", "Notice teeth crowding or jaw pain? Here are 3 subtle signs most people ignore.", "Canva Flyer: 3 aesthetic split cards showing dental alignment before/after drawings", "Share with someone who hides their smile", "1:00 PM"),
            (3, "Phase 1", "Single Post (1:1)", "Why Traditional Braces Are Being Replaced", "Wires vs. Invisible Aligners: A complete breakdown of comfort, diet, and lifestyle.", "High-res photo: Close up of a clear aligner resting on clean dental surface", "Drop a 👍 if you prefer invisible", "6:00 PM"),
            (4, "Phase 1", "Story Series + Poll", "Does Laser Dentistry Actually Hurt?", "We asked 50 patients about pain levels. Here is what they honestly said.", "Video clip: Doctor holding painless laser pen explaining zero-bleeding tech", "Vote in our pain poll", "12:30 PM"),
            (5, "Phase 1", "Reel (9:16)", "The 60-Second 3D Scan Experience", "Watch how a full digital 3D replica of your mouth is captured in just 60 seconds.", "Cinematic video: 3D intraoral scanner gliding smoothly over patient's teeth", "Book your free scan via link in bio", "8:00 PM"),
            (6, "Phase 1", "Carousel", "What Happens to Your Teeth While You Sleep?", "Night grinding and enamel erosion — how to protect your smile effortlessly.", "Infographic carousel: Clean clinical typography with modern diagrams", "Save for later", "11:30 AM"),
            (7, "Phase 1", "Story Q&A", "Sunday Smile Clinic AMA", "Answering your top questions about yellow teeth, bad breath, and aligners.", "Casual doctor selfie story with question sticker", "Ask your question below", "4:00 PM"),
            
            # Week 2: Social Proof
            (8, "Phase 2", "Carousel", "From Insecure to Unstoppable: Rahul's 6-Month Journey", "See how Rahul transformed his smile without metal wires before his wedding.", "Side-by-side high-res before/after smile photography with patient quote", "Comment 'SMILE' for treatment details", "7:30 PM"),
            (9, "Phase 2", "Reel (9:16)", "Is Laser Teeth Whitening Safe for Enamel?", "Debunking the #1 myth about teeth sensitivity and enamel damage.", "Macro video: Sparkling dental clean process with gentle laser pulse", "Share with coffee lovers", "1:30 PM"),
            (10, "Phase 2", "Single Post", "Transparent Pricing: No Hidden Clinic Surcharges", "Why we publish our costs openly. Packages starting from {key_offer}.", "Modern Canva aesthetic price breakdown card with 0% EMI badge", "Tap link in bio to check pricing", "6:30 PM"),
            (11, "Phase 2", "Reel (9:16)", "A Day in the Life of a Cosmetic Dentist", "Pristine sterilization, patient smile designs, and customized treatment plans.", "Fast-paced aesthetic reel with trending upbeat audio", "Follow for daily dental tips", "8:00 PM"),
            (12, "Phase 2", "Carousel", "5 Foods That Silently Stain Your Teeth", "Coffee, red wine, and soy sauce: how to enjoy them without ruining your white smile.", "Aesthetic lifestyle flat lay of morning coffee with dental tips", "Tag a coffee addict", "12:00 PM"),
            (13, "Phase 2", "Story Testimonial", "Video Review from Priya in {location}", "Hear why she was terrified of dentists until she visited {business_name}.", "Short vertical video of real patient smiling and sharing her review", "Tap to book your visit", "5:30 PM"),
            (14, "Phase 2", "Carousel", "Metal Braces vs Clear Aligners: The Cost Math", "Think aligners are twice as expensive? Think again. Real cost comparison.", "Canva comparison matrix with checkmarks and pricing breakdown", "Check your eligibility in bio", "7:00 PM"),

            # Week 3: Pre-Launch Hype
            (15, "Phase 3", "Reel (9:16)", "Something Big Is Coming to {location} Next Week", "We are opening 25 exclusive VIP consultation slots with free 3D scans.", "Cinematic teaser video: Slow motion reveal of brand new aligner suite", "Comment 'VIP' to get early invite", "7:30 PM"),
            (16, "Phase 3", "Story Poll", "Would You Rather: Whiter Teeth or Straighter Teeth?", "Help us tailor our upcoming festive smile package to what you want most.", "Interactive 2-option Instagram story poll sticker", "Cast your vote", "1:00 PM"),
            (17, "Phase 3", "Carousel", "Behind the Technology: Why Digital Scanning Matters", "No messy putty trays. No gagging. Why 100% digital dentistry is the future.", "Close up photo of high-tech digital touchscreen 3D smile model", "Save this post", "6:00 PM"),
            (18, "Phase 3", "Single Post", "Only 10 Early-Bird Slots Left on the Waitlist", "The response to our VIP Smile Launch has been overwhelming.", "Clean aesthetic graphic: 'VIP Waitlist Closing Soon' with golden badge", "DM us 'WAITLIST' to claim", "8:00 PM"),
            (19, "Phase 3", "Reel (9:16)", "Common Aligner Mistakes You Must Avoid", "Drinking hot drinks with trays on? Here are 3 mistakes that ruin treatment.", "Doctor speaking directly to camera with animated kinetic captions", "Share with someone wearing braces", "12:30 PM"),
            (20, "Phase 3", "Carousel", "Meet the Lead Specialist at {business_name}", "15+ years of clinical excellence, thousands of successful smile rehabilitations.", "High-end corporate studio portrait of the doctor in pristine coat", "Book a private consult in bio", "7:00 PM"),
            (21, "Phase 3", "Story Countdown", "24 Hours Left Until Official Public Launch!", "Tomorrow morning we unlock our {key_offer} for the first 30 bookings.", "Instagram countdown sticker set to 9:00 AM tomorrow", "Turn on countdown reminder", "6:00 PM"),

            # Week 4: Paid Meta Ad Blitz & Direct WhatsApp Conversion
            (22, "Phase 4", "Meta Ad Reel (9:16)", "💥 LAUNCH DAY: Claim Your Free 3D Dental Scan in {location}", "The wait is over! Experience pain-free aligners and laser care starting at {key_offer}.", "High-energy 9:16 commercial with direct WhatsApp green CTA pill", "Tap 'Send WhatsApp Message' below", "9:00 AM"),
            (23, "Phase 4", "Meta Feed Ad (1:1)", "Exclusive {location} Smile Makeover Offer", "Lock in 0% EMI and free initial 3D scan this week only. Limited appointments.", "Professional Canva flyer with doctor portrait and price sticker", "Click WhatsApp to book now", "2:00 PM"),
            (24, "Phase 4", "Story Proof", "14 Bookings in the First 48 Hours!", "Thank you {location}! Showing live appointment calendar filling up.", "Screenshot of busy appointment diary with patient names blurred", "Grab one of the remaining 6 slots", "6:30 PM"),
            (25, "Phase 4", "Reel (9:16)", "Why Our WhatsApp AI Responds in 5 Seconds", "No waiting on hold. Chat, pick your slot, and get directions instantly.", "Screen recording of WhatsApp conversation smoothly booking Saturday visit", "Message us on WhatsApp", "8:00 PM"),
            (26, "Phase 4", "Carousel", "The 4 Steps to Your New Smile", "From WhatsApp booking to customized 3D aligners: how simple it really is.", "Step-by-step visual roadmap with clean numbered icons", "Start step 1 on WhatsApp", "1:00 PM"),
            (27, "Phase 4", "Meta Ad Retargeting", "Still Thinking About Aligners? Here is 0% EMI", "Don't postpone confidence. Pay in easy installments with zero interest.", "Clear financial infographic showing monthly breakdown of ₹2,499/mo", "Chat with our team on WhatsApp", "5:00 PM"),
            (28, "Phase 4", "Story Urgency", "Last 3 Saturday Slots Remaining", "Private sample flat / clinic consultations closing for the weekend.", "Story photo of clinic reception with urgent text overlay", "Swipe up to claim final slot", "11:00 AM"),
            (29, "Phase 4", "Reel (9:16)", "What Our Patients Wish They Knew Earlier", "The #1 regret our aligner patients share: 'I wish I had done this 3 years ago.'", "Montage of happy smiling patients holding their aligner cases", "Start your journey today", "7:30 PM"),
            (30, "Phase 4", "Single Post", "Month 1 Campaign Wrap-Up & What's Next", "Celebrating 50+ new smile transformations launched this month in {location}!", "Warm team photo of clinic staff celebrating milestone", "Join the family on WhatsApp", "8:30 PM")
        ]
    else:
        # Generic Real Estate / Universal Blueprint
        daily_blueprints = [
            (i, f"Phase {(i-1)//7 + 1}", "Reel (9:16)" if i % 2 == 1 else "Carousel",
             f"{business_name} Milestone Day {i}",
             f"Highlighting key features of {key_offer} in {location} for {target_audience}.",
             "Cinematic 4K shot highlighting product quality and location advantage",
             "Tap WhatsApp to connect", "7:30 PM")
            for i in range(1, 31)
        ]

    for item in daily_blueprints:
        day_num, phase_name, fmt, headline, caption, visual_brief, cta, best_time = item
        days_data.append({
            "day": day_num,
            "phase": phase_name,
            "format": fmt,
            "headline": headline.format(business_name=business_name, location=location, key_offer=key_offer),
            "caption": caption.format(business_name=business_name, location=location, key_offer=key_offer, target_audience=target_audience),
            "visual_brief": visual_brief.format(business_name=business_name, location=location, key_offer=key_offer),
            "call_to_action": cta,
            "best_time": best_time
        })

    return {
        "business_name": business_name,
        "industry": industry,
        "location": location,
        "phases_overview": phases,
        "days": days_data
    }

"""
LeadPulse AI — Programmatic 9:16 Video Ad Producer
Combines AI voiceover (VoiceStudio Neural Engine via Edge-TTS) with programmatic motion slides
and FFmpeg to generate professional 9:16 Instagram Reels / WhatsApp video ads with smooth transitions.
"""
import os
import uuid
import asyncio
import subprocess
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from .banner_designer import get_font, create_gradient, fetch_stock_photo
from .copywriter import get_dynamic_cta



async def generate_voiceover(
    text: str,
    output_path: str,
    voice: str = "en-US-JennyNeural",
    rate: str = "+0%"
):
    """Generate professional UGC audio MP3 using neural voice synthesis with SSML pauses.

    Inspired by debpalash/VoiceStudio for high-quality neural voice cloning and
    cliprise/awesome-ai-ugc-video-prompts for authentic UGC pacing and delivery.

    Args:
        text: Full narration script
        output_path: Path to save MP3
        voice: Neural voice persona optimized for UGC
        rate: Speech rate adjustment (+/- percentage)
    """
    import edge_tts

    # Enhanced voice mapping for UGC authenticity (inspired by VoiceStudio)
    voice_mapping = {
        "en-US-JennyNeural": "en-US-JennyNeural",      # Sarah - Authentic UGC Creator (friendly, relatable)
        "en-US-GuyNeural": "en-US-GuyNeural",          # Marcus - High-Energy Direct Response (urgent, persuasive)
        "en-IN-NeerjaNeural": "en-IN-NeerjaNeural",    # Neerja - Luxury & Premium (sophisticated, trustworthy)
        "en-US-ChristopherNeural": "en-US-ChristopherNeural",  # Christopher - Tech & Corporate (authoritative, clear)
        "en-US-AriaNeural": "en-US-AriaNeural",        # Aria - Expressive Commercial (emotional, engaging)
        "en-US-AnaNeural": "en-US-AnaNeural",          # Ana - Young & Energetic (gen-Z, trendy)
        "en-US-BrandonNeural": "en-US-BrandonNeural",  # Brandon - Confident & Direct (no-nonsense, bold)
        "hi-IN-MadhurNeural": "hi-IN-MadhurNeural",    # Madhur - Indian Male (warm, conversational)
        "hi-IN-SwaraNeural": "hi-IN-SwaraNeural",      # Swara - Indian Female (friendly, approachable)
        "en-AU-NatashaNeural": "en-AU-NatashaNeural",  # Natasha - Aussie Authentic (casual, trustworthy)
        "en-GB-SoniaNeural": "en-GB-SoniaNeural",      # Sonia - British Professional (polished, credible)
    }

    selected_voice = voice_mapping.get(voice, "en-US-JennyNeural")  # Default to authentic UGC voice

    # Enhanced SSML processing for professional UGC pacing
    def add_ugc_pauses(script: str) -> str:
        """Add professional SSML pauses and emphasis for UGC-style delivery."""
        # Split into sentences for precise timing
        import re

        # Add pauses between sentences (UGC-style natural breaks)
        script = re.sub(r'([.!?])\s+', r'\1<break time="600ms"/> ', script)

        # Add shorter pauses for commas (natural speech rhythm)
        script = script.replace(', ', ',<break time="250ms"/> ')

        # Add emphasis on key phrases (common in UGC hooks)
        emphasis_keywords = ['exclusive', 'limited', 'special', 'free', 'now', 'today', 'only', 'secret']
        for keyword in emphasis_keywords:
            if keyword in script.lower():
                # Find the keyword and wrap with emphasis tag
                pattern = re.compile(f'\\b{keyword}\\b', re.IGNORECASE)
                script = pattern.sub(f'<emphasis level="strong">{keyword}</emphasis>', script)

        # Add prosody for natural UGC delivery (slight pitch variations)
        sentences = re.split(r'[.!?]+', script)
        processed_sentences = []
        for i, sentence in enumerate(sentences):
            if sentence.strip():
                # Vary pitch slightly for natural UGC delivery
                pitch_adjust = "-2%" if i % 3 == 0 else "+0%"  # Slight variation
                processed_sentences.append(f'<prosody pitch="{pitch_adjust}">{sentence.strip()}</prosody>')

        # Reconstruct with proper SSML wrapper
        ssml_text = ' '.join(processed_sentences)

        # Add UGC-style intro and outro breaths
        ssml_text = f'<break time="300ms"/><prosody rate="95%">{ssml_text}</prosody><break time="800ms"/>'

        return f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">{ssml_text}</speak>'

    # Process text with UGC-style SSML
    ssml_text = add_ugc_pauses(text)

    # Configure voice with UGC-optimized settings
    communicate = edge_tts.Communicate(
        ssml_text,
        selected_voice,
        rate=rate,
        pitch="+0Hz",  # Natural pitch for authenticity
        volume="+0%"    # Normal volume
    )

    await communicate.save(output_path)

    # Log voice synthesis details for debugging
    print(f"✓ Generated UGC voiceover: {selected_voice} | SSML optimized | Saved to {output_path}")


def create_slide(
    title: str,
    subtitle: str,
    badge: str,
    cta: str,
    output_path: str,
    highlight_color: tuple = (16, 185, 129), # Emerald
    industry: str = "universal"
):
    """Render a single 1080x1920 UGC video slide with dynamic gradients, glassmorphism, and bold typography.

    Follows professional UGC ad standards with industry-specific color schemes and modern design.
    """
    width, height = 1080, 1920

    # Industry-specific color schemes inspired by debpalash/VoiceStudio and cliprise/awesome-ai-ugc-video-prompts
    industry_colors = {
        "food": {"grad_start": (251, 191, 36), "grad_end": (220, 38, 38), "accent": (234, 179, 8), "text": (30, 41, 59)},
        "dental": {"grad_start": (56, 189, 248), "grad_end": (14, 165, 233), "accent": (45, 212, 191), "text": (15, 23, 42)},
        "fitness": {"grad_start": (239, 68, 68), "grad_end": (220, 38, 38), "accent": (251, 191, 36), "text": (30, 41, 59)},
        "real_estate": {"grad_start": (139, 92, 246), "grad_end": (124, 58, 237), "accent": (244, 114, 182), "text": (15, 23, 42)},
        "ecommerce": {"grad_start": (16, 185, 129), "grad_end": (5, 150, 105), "accent": (34, 197, 94), "text": (30, 41, 59)},
        "tech": {"grad_start": (59, 130, 246), "grad_end": (37, 99, 235), "accent": (139, 92, 246), "text": (15, 23, 42)},
        "luxury": {"grad_start": (120, 113, 108), "grad_end": (68, 64, 60), "accent": (212, 212, 212), "text": (250, 250, 250)},
        "universal": {"grad_start": (99, 102, 241), "grad_end": (79, 70, 229), "accent": (139, 92, 246), "text": (15, 23, 42)}
    }

    # Get industry-specific colors or fallback to universal
    colors = industry_colors.get(industry, industry_colors["universal"])

    # Create dynamic gradient background with noise texture
    img = Image.new('RGB', (width, height), colors["grad_start"])
    draw = ImageDraw.Draw(img)

    # Add gradient overlay
    for y in range(height):
        ratio = y / height
        r = int(colors["grad_start"][0] * (1 - ratio) + colors["grad_end"][0] * ratio)
        g = int(colors["grad_start"][1] * (1 - ratio) + colors["grad_end"][1] * ratio)
        b = int(colors["grad_start"][2] * (1 - ratio) + colors["grad_end"][2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Add subtle noise texture for UGC authenticity
    import random
    noise = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    noise_draw = ImageDraw.Draw(noise)
    for _ in range(800):
        x, y = random.randint(0, width), random.randint(0, height)
        size = random.randint(1, 3)
        alpha = random.randint(5, 15)
        noise_draw.ellipse([x, y, x + size, y + size], fill=(255, 255, 255, alpha))
    img = Image.alpha_composite(img.convert('RGBA'), noise).convert('RGB')
    draw = ImageDraw.Draw(img)

    # Add floating abstract shapes (glassmorphism effect)
    shapes = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    shapes_draw = ImageDraw.Draw(shapes)

    # Large blurred circles for depth
    for i in range(3):
        x = random.randint(-200, width + 200)
        y = random.randint(-200, height + 200)
        radius = random.randint(200, 500)
        alpha = random.randint(10, 30)
        shape_color = (*colors["accent"], alpha)
        shapes_draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=shape_color)

    img = Image.alpha_composite(img.convert('RGBA'), shapes).convert('RGB')
    draw = ImageDraw.Draw(img)

    # Top category pill (glassmorphism effect)
    pill_font = get_font(36, bold=True)
    pill_text = f"✦  {badge.upper()}  ✦"
    bbox = draw.textbbox((0, 0), pill_text, font=pill_font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    px, py = (width - tw) // 2, 220

    # Glassmorphism pill background
    pill_bg = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    pill_bg_draw = ImageDraw.Draw(pill_bg)
    pill_bg_draw.rounded_rectangle([px - 32, py - 16, px + tw + 32, py + th + 16],
                                  radius=28, fill=(255, 255, 255, 25), outline=(255, 255, 255, 40), width=3)

    # Add blur effect to pill background
    from PIL import ImageFilter
    blurred_pill = pill_bg.filter(ImageFilter.GaussianBlur(radius=10))
    img = Image.alpha_composite(img.convert('RGBA'), blurred_pill).convert('RGB')
    draw = ImageDraw.Draw(img)

    draw.text((px, py), pill_text, font=pill_font, fill=(255, 255, 255))

    # Big Title (Centered, Wrapped with gradient text)
    title_font = get_font(72, bold=True)
    words = title.split()
    lines = []
    curr = []
    for w in words:
        curr.append(w)
        bbox = draw.textbbox((0, 0), " ".join(curr), font=title_font)
        if (bbox[2] - bbox[0]) > (width - 200):
            curr.pop()
            lines.append(" ".join(curr))
            curr = [w]
    if curr:
        lines.append(" ".join(curr))

    ty = 320
    for line in lines[:3]:  # Limit to 3 lines for better visual hierarchy
        bbox = draw.textbbox((0, 0), line, font=title_font)
        lx = (width - (bbox[2] - bbox[0])) // 2

        # Create gradient text effect
        text_mask = Image.new('L', (width, height), 0)
        text_draw = ImageDraw.Draw(text_mask)
        text_draw.text((lx, ty), line, font=title_font, fill=255)

        # Apply gradient to text
        gradient = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        gradient_draw = ImageDraw.Draw(gradient)
        text_w = max(1, bbox[2] - bbox[0])
        text_h = max(1, bbox[3] - bbox[1])
        for i in range(text_w):
            grad_x = lx + i
            ratio = i / text_w
            r = int(255 * (1 - ratio) + colors["accent"][0] * ratio)
            g = int(255 * (1 - ratio) + colors["accent"][1] * ratio)
            b = int(255 * (1 - ratio) + colors["accent"][2] * ratio)
            gradient_draw.line([(grad_x, ty), (grad_x, ty + text_h)], fill=(r, g, b, 255))

        gradient.putalpha(text_mask)
        # Drop shadow for readability
        draw.text((lx + 3, ty + 3), line, font=title_font, fill=(10, 15, 30, 200))
        img = Image.alpha_composite(img.convert('RGBA'), gradient).convert('RGB')
        draw = ImageDraw.Draw(img)

        ty += 100

    # Center Feature Card (Glassmorphism)
    card_y = ty + 40

    # Glass card with blur
    card_bg = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    card_draw = ImageDraw.Draw(card_bg)
    card_draw.rounded_rectangle([60, card_y, width - 60, card_y + 320],
                               radius=32, fill=(255, 255, 255, 20), outline=(255, 255, 255, 30), width=2)

    blurred_card = card_bg.filter(ImageFilter.GaussianBlur(radius=8))
    img = Image.alpha_composite(img.convert('RGBA'), blurred_card).convert('RGB')
    draw = ImageDraw.Draw(img)

    # Subtitle text inside card
    sub_font = get_font(40, bold=False)
    sub_words = subtitle.split()
    sub_lines = []
    curr_sub = []
    for w in sub_words:
        curr_sub.append(w)
        bbox = draw.textbbox((0, 0), " ".join(curr_sub), font=sub_font)
        if (bbox[2] - bbox[0]) > (width - 160):
            curr_sub.pop()
            sub_lines.append(" ".join(curr_sub))
            curr_sub = [w]
    if curr_sub:
        sub_lines.append(" ".join(curr_sub))

    sy = card_y + 80
    for line in sub_lines[:3]:  # Limit to 3 lines
        bbox = draw.textbbox((0, 0), line, font=sub_font)
        lx = (width - (bbox[2] - bbox[0])) // 2
        draw.text((lx, sy), line, font=sub_font, fill=(255, 255, 255, 230))
        sy += 70

    # Bottom WhatsApp Action Pill with glowing effect
    btn_y = height - 280

    # Glow effect
    glow = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.rounded_rectangle([50, btn_y - 10, width - 50, btn_y + 130],
                               radius=60, fill=(37, 211, 102, 40))
    blurred_glow = glow.filter(ImageFilter.GaussianBlur(radius=20))
    img = Image.alpha_composite(img.convert('RGBA'), blurred_glow).convert('RGB')
    draw = ImageDraw.Draw(img)

    # Button with gradient
    btn_gradient = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    btn_grad_draw = ImageDraw.Draw(btn_gradient)
    for x in range(60, width - 60):
        ratio = (x - 60) / (width - 120)
        r = int(37 * (1 - ratio) + 22 * ratio)
        g = int(211 * (1 - ratio) + 163 * ratio)
        b = int(102 * (1 - ratio) + 43 * ratio)
        btn_grad_draw.line([(x, btn_y), (x, btn_y + 110)], fill=(r, g, b, 255))

    btn_mask = Image.new('L', (width, height), 0)
    btn_mask_draw = ImageDraw.Draw(btn_mask)
    btn_mask_draw.rounded_rectangle([60, btn_y, width - 60, btn_y + 110], radius=55, fill=255)

    btn_gradient.putalpha(btn_mask)
    img = Image.alpha_composite(img.convert('RGBA'), btn_gradient).convert('RGB')
    draw = ImageDraw.Draw(img)

    # CTA text with shadow
    cta_font = get_font(44, bold=True)
    c_bbox = draw.textbbox((0, 0), cta, font=cta_font)
    cx = (width - (c_bbox[2] - c_bbox[0])) // 2

    # Text shadow
    shadow_offset = 3
    draw.text((cx + shadow_offset, btn_y + 35 + shadow_offset), cta, font=cta_font, fill=(0, 0, 0, 100))
    # Main text
    draw.text((cx, btn_y + 35), cta, font=cta_font, fill=(255, 255, 255))

    # Add final subtle vignette
    vignette = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    vignette_draw = ImageDraw.Draw(vignette)
    for y in range(height):
        dist_from_center = abs(y - height/2) / (height/2)
        alpha = int(80 * dist_from_center ** 2)
        vignette_draw.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))

    img = Image.alpha_composite(img.convert('RGBA'), vignette).convert('RGB')

    img.save(output_path, "JPEG", quality=95)


async def generate_video_ad(
    product_name: str,
    price_point: str,
    location: str,
    key_benefit: str,
    script_obj: dict,
    output_dir: str,
    voice: str = "en-IN-NeerjaNeural",
    industry: str = "dental"
) -> str:
    """Generate a complete 9:16 vertical MP4 video ad with FFmpeg motion transitions.

    Creates smooth Ken Burns zoompan effects and xfade crossfade transitions between scenes.
    Muxes high-fidelity VoiceStudio neural voiceover (AAC 192k) for professional output.

    Args:
        product_name: Product/service name
        price_point: Price/offer text
        location: Target location
        key_benefit: Main benefit/USP
        script_obj: Dict with keys: hook, problem, solution, cta
        output_dir: Output directory
        voice: VoiceStudio neural voice persona
        industry: Industry type for stock photo selection

    Returns:
        Path to generated MP4 video file
    """
    os.makedirs(output_dir, exist_ok=True)
    run_id = uuid.uuid4().hex[:8]
    temp_dir = os.path.join(output_dir, f"temp_{run_id}")
    os.makedirs(temp_dir, exist_ok=True)

    audio_path = os.path.join(temp_dir, "voice.mp3")
    output_video = os.path.join(output_dir, f"video_ad_{run_id}.mp4")

    # Infer industry if not specified
    combined = (product_name + " " + script_obj.get("hook", "")).lower()
    if any(k in combined for k in ["dental", "smile", "aligner", "teeth", "tooth"]):
        industry = "dental"
    elif any(k in combined for k in ["bhk", "flat", "villa", "realty", "estate", "home"]):
        industry = "real_estate"
    elif any(k in combined for k in ["gym", "fit", "workout"]):
        industry = "fitness"

    # 1. Generate Voiceover with VoiceStudio Neural Engine
    full_text = f"{script_obj['hook']} {script_obj['problem']} {script_obj['solution']} {script_obj['cta']}"
    await generate_voiceover(full_text, audio_path, voice=voice)

    # 2. Get FFmpeg executable
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    # 3. Generate 4 Animated Slide Frames following UGC timing structure:
    #    Hook (0-3s), Problem/Agitation (3-7s), Solution/Product Demo (7-11s), Urgent CTA (11-15s)
    dynamic_cta = get_dynamic_cta(product_name, industry, "")

    # Slide 1: Hook (0-3s) - Attention grabber
    slide1 = os.path.join(temp_dir, "slide1.jpg")
    create_slide(
        title=script_obj.get('hook', f"🔥 {product_name}"),
        subtitle=f"Stop scrolling! This changed everything in {location}",
        badge="ATTENTION",
        cta=dynamic_cta,
        output_path=slide1,
        highlight_color=(239, 68, 68),  # Red for urgency
        industry=industry
    )

    # Slide 2: Problem/Agitation (3-7s) - Pain point
    slide2 = os.path.join(temp_dir, "slide2.jpg")
    create_slide(
        title=script_obj.get('problem', f"The {industry} problem nobody talks about"),
        subtitle=key_benefit.split(',')[0] if ',' in key_benefit else key_benefit,
        badge="PROBLEM",
        cta=dynamic_cta,
        output_path=slide2,
        highlight_color=(245, 158, 11),  # Amber for warning/issue
        industry=industry
    )

    # Slide 3: Solution/Product Demo (7-11s) - Hero reveal
    slide3 = os.path.join(temp_dir, "slide3.jpg")
    create_slide(
        title=script_obj.get('solution', f"{product_name} solves it instantly"),
        subtitle=f"{price_point} · {key_benefit}",
        badge="SOLUTION",
        cta=dynamic_cta,
        output_path=slide3,
        highlight_color=(16, 185, 129),  # Emerald for solution
        industry=industry
    )

    # Slide 4: Urgent CTA (11-15s) - Call to action
    slide4 = os.path.join(temp_dir, "slide4.jpg")
    create_slide(
        title=script_obj.get('cta', '⚡ LIMITED TIME OFFER ⚡'),
        subtitle=f"Available in {location} · Tap WhatsApp to claim {price_point}",
        badge="ACT NOW",
        cta=dynamic_cta,
        output_path=slide4,
        highlight_color=(139, 92, 246),  # Purple for urgency/royalty
        industry=industry
    )

    # 4. Create FFmpeg filtergraph for UGC-style motion effects and transitions
    # Each slide gets specific duration: 3s, 4s, 4s, 4s = 15s total
    # Use different zoom effects for each UGC scene type
    filtergraph = (
        # Hook slide: Quick zoom-in for attention (0-3s)
        "[0:v]zoompan=z='min(zoom+0.002,1.25)':d=75:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=25[v0];"
        # Problem slide: Slow pan for tension (3-7s)
        "[1:v]zoompan=z='min(zoom+0.0008,1.10)':d=100:x='iw/2-(iw/zoom/2)+sin(on/25)*50':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=25[v1];"
        # Solution slide: Smooth reveal zoom (7-11s)
        "[2:v]zoompan=z='min(zoom+0.0015,1.20)':d=100:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)+cos(on/30)*30':s=1080x1920:fps=25[v2];"
        # CTA slide: Steady focus for urgency (11-15s)
        "[3:v]zoompan=z='min(zoom+0.0010,1.15)':d=100:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=25[v3];"
        # UGC-style transitions with timing: 3s, 4s, 4s intervals
        "[v0][v1]xfade=transition=slideleft:duration=0.5:offset=2.5[xf1];"
        "[xf1][v2]xfade=transition=slideright:duration=0.5:offset=6.5[xf2];"
        "[xf2][v3]xfade=transition=fade:duration=0.5:offset=10.5[v_out]"
    )

    # 5. Build FFmpeg command with motion video + audio mux
    cmd = [
        ffmpeg_exe,
        "-y",
        "-i", slide1,
        "-i", slide2,
        "-i", slide3,
        "-i", slide4,
        "-i", audio_path,
        "-filter_complex", filtergraph,
        "-map", "[v_out]",
        "-map", "4:a",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_video
    ]

    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise RuntimeError(f"FFmpeg failed: {proc.stderr.decode('utf-8', errors='ignore')}")

    # Cleanup temp directory
    try:
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
    except Exception:
        pass

    return output_video

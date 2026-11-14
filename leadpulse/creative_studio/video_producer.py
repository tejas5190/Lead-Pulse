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
from PIL import Image, ImageDraw, ImageFont
from .banner_designer import get_font, create_gradient, fetch_stock_photo


async def generate_voiceover(
    text: str,
    output_path: str,
    voice: str = "en-IN-NeerjaNeural",
    rate: str = "+0%"
):
    """Generate audio MP3 using VoiceStudio Neural Engine (Edge-TTS).

    Args:
        text: Full narration script
        output_path: Path to save MP3
        voice: Neural voice persona (VoiceStudio voices)
        rate: Speech rate adjustment (+/- percentage)
    """
    import edge_tts
    # Map VoiceStudio personas to Edge-TTS voices
    voice_mapping = {
        "en-US-JennyNeural": "en-US-JennyNeural",  # Sarah (UGC Authentic Creator)
        "en-US-GuyNeural": "en-US-GuyNeural",        # Marcus (High-Energy Direct Response)
        "en-IN-NeerjaNeural": "en-IN-NeerjaNeural",  # Neerja (Luxury & Premium Narrator)
        "en-US-ChristopherNeural": "en-US-ChristopherNeural",  # Tech & Corporate Storyteller
        "en-US-AriaNeural": "en-US-AriaNeural",      # Expressive Commercial
        "hi-IN-MadhurNeural": "hi-IN-MadhurNeural",  # Indian Male Voice
        "hi-IN-SwaraNeural": "hi-IN-SwaraNeural",    # Indian Female Voice
    }

    selected_voice = voice_mapping.get(voice, voice)

    # Add natural pauses between beats (sentences ending with punctuation)
    processed_text = text.replace(". ", ".<break time=\"500ms\"/> ").replace("! ", "!<break time=\"500ms\"/> ")

    communicate = edge_tts.Communicate(processed_text, selected_voice, rate=rate)
    await communicate.save(output_path)


def create_slide(
    title: str,
    subtitle: str,
    badge: str,
    cta: str,
    output_path: str,
    highlight_color: tuple = (16, 185, 129), # Emerald
    industry: str = "dental"
):
    """Render a single 1080x1920 video slide image with realistic photo background."""
    width, height = 1080, 1920
    base_photo = fetch_stock_photo(industry, width, height)
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    for y in range(height):
        ratio = y / height
        alpha = int(75 + 160 * (ratio ** 1.3))
        overlay_draw.line([(0, y), (width, y)], fill=(15, 23, 42, alpha))
    img = Image.alpha_composite(base_photo.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(img)

    # Accent decorative background circles
    glow = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse([width - 500, 200, width + 300, 1000], fill=(*highlight_color, 35))
    glow_draw.ellipse([-200, height - 800, 400, height - 200], fill=(99, 102, 241, 35))
    img.paste(glow, (0, 0), glow)
    draw = ImageDraw.Draw(img)

    # Top category pill
    pill_font = get_font(32, bold=True)
    pill_text = f"✦  {badge.upper()}  ✦"
    bbox = draw.textbbox((0, 0), pill_text, font=pill_font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    px, py = (width - tw) // 2, 240
    draw.rounded_rectangle([px - 28, py - 12, px + tw + 28, py + th + 12], radius=24, fill=(30, 41, 59), outline=highlight_color, width=2)
    draw.text((px, py), pill_text, font=pill_font, fill=(241, 245, 249))

    # Big Title (Centered, Wrapped)
    title_font = get_font(64, bold=True)
    words = title.split()
    lines = []
    curr = []
    for w in words:
        curr.append(w)
        bbox = draw.textbbox((0, 0), " ".join(curr), font=title_font)
        if (bbox[2] - bbox[0]) > (width - 180):
            curr.pop()
            lines.append(" ".join(curr))
            curr = [w]
    if curr:
        lines.append(" ".join(curr))

    ty = 420
    for line in lines[:4]:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        lx = (width - (bbox[2] - bbox[0])) // 2
        draw.text((lx, ty), line, font=title_font, fill=(255, 255, 255))
        ty += 84

    # Center Feature Card
    card_y = ty + 60
    draw.rounded_rectangle([90, card_y, width - 90, card_y + 360], radius=24, fill=(15, 23, 42, 200), outline=(51, 65, 85), width=2)
    
    sub_font = get_font(38, bold=False)
    sub_words = subtitle.split()
    sub_lines = []
    curr_sub = []
    for w in sub_words:
        curr_sub.append(w)
        bbox = draw.textbbox((0, 0), " ".join(curr_sub), font=sub_font)
        if (bbox[2] - bbox[0]) > (width - 260):
            curr_sub.pop()
            sub_lines.append(" ".join(curr_sub))
            curr_sub = [w]
    if curr_sub:
        sub_lines.append(" ".join(curr_sub))

    sy = card_y + 60
    for line in sub_lines[:4]:
        bbox = draw.textbbox((0, 0), line, font=sub_font)
        lx = (width - (bbox[2] - bbox[0])) // 2
        draw.text((lx, sy), line, font=sub_font, fill=(203, 213, 225))
        sy += 56

    # Bottom WhatsApp Action Pill
    btn_y = height - 320
    draw.rounded_rectangle([90, btn_y, width - 90, btn_y + 110], radius=55, fill=(34, 197, 94))
    cta_font = get_font(42, bold=True)
    c_bbox = draw.textbbox((0, 0), cta, font=cta_font)
    cx = (width - (c_bbox[2] - c_bbox[0])) // 2
    draw.text((cx, btn_y + 32), cta, font=cta_font, fill=(255, 255, 255))

    img.save(output_path, "JPEG", quality=90)


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

    # 3. Generate 3 Animated Slide Frames with stock photography
    slide1 = os.path.join(temp_dir, "slide1.jpg")
    create_slide(
        title=script_obj['hook'],
        subtitle=f"Special Opportunity in {location}",
        badge=product_name,
        cta="📲 Chat on WhatsApp ➔",
        output_path=slide1,
        highlight_color=(99, 102, 241),
        industry=industry
    )

    slide2 = os.path.join(temp_dir, "slide2.jpg")
    create_slide(
        title=f"Starting at {price_point}",
        subtitle=key_benefit,
        badge="PREMIUM PRICING",
        cta="📲 Get Details On WhatsApp ➔",
        output_path=slide2,
        highlight_color=(16, 185, 129),
        industry=industry
    )

    slide3 = os.path.join(temp_dir, "slide3.jpg")
    create_slide(
        title="Consultations Open This Week",
        subtitle=script_obj['cta'],
        badge="LIMITED SLOTS AVAILABLE",
        cta="📲 Book Free VIP Visit ➔",
        output_path=slide3,
        highlight_color=(245, 158, 11),
        industry=industry
    )

    # 4. Create FFmpeg filtergraph for motion effects and transitions
    # Use zoompan for Ken Burns effect (push-in, pan, hero reveal)
    # Use xfade for smooth crossfade transitions (0.5s duration)
    filtergraph = (
        "[0:v]zoompan=z='min(zoom+0.0012,1.15)':d=125:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=25[v0];"
        "[1:v]zoompan=z='min(zoom+0.0015,1.20)':d=125:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=25[v1];"
        "[2:v]zoompan=z='min(zoom+0.0010,1.15)':d=150:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=25[v2];"
        "[v0][v1]xfade=transition=fade:duration=0.5:offset=4.5[xf1];"
        "[xf1][v2]xfade=transition=fade:duration=0.5:offset=9.0[v_out]"
    )

    # 5. Build FFmpeg command with motion video + audio mux
    cmd = [
        ffmpeg_exe,
        "-y",
        "-i", slide1,
        "-i", slide2,
        "-i", slide3,
        "-i", audio_path,
        "-filter_complex", filtergraph,
        "-map", "[v_out]",
        "-map", "3:a",
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

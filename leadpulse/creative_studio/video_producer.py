"""
LeadPulse AI — Programmatic 9:16 Video Ad Producer
Combines AI voiceover (Edge-TTS) with programmatic motion slides and FFmpeg
to generate professional 9:16 Instagram Reels / WhatsApp video ads.
"""
import os
import uuid
import asyncio
import subprocess
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont
from .banner_designer import get_font, create_gradient, fetch_stock_photo


async def generate_voiceover(text: str, output_path: str, voice: str = "en-IN-NeerjaNeural"):
    """Generate audio MP3 using Edge-TTS."""
    import edge_tts
    communicate = edge_tts.Communicate(text, voice)
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
    """Generate a complete 9:16 vertical MP4 video ad."""
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

    # 1. Generate Voiceover
    full_text = f"{script_obj['hook']} {script_obj['problem']} {script_obj['solution']} {script_obj['cta']}"
    await generate_voiceover(full_text, audio_path, voice=voice)

    # 2. Get audio duration using ffprobe
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    # 3. Generate 3 Animated Slide Frames
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

    # 4. Create concat demuxer text file for FFmpeg (using relative basenames)
    concat_file = os.path.join(temp_dir, "concat.txt")
    with open(concat_file, "w") as f:
        f.write("file 'slide1.jpg'\nduration 4.5\n")
        f.write("file 'slide2.jpg'\nduration 4.5\n")
        f.write("file 'slide3.jpg'\nduration 5.0\n")
        f.write("file 'slide3.jpg'\n")

    # 5. Render Video with FFmpeg
    cmd = [
        ffmpeg_exe,
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_file,
        "-i", audio_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-r", "25",
        "-c:a", "aac",
        "-b:a", "128k",
        "-shortest",
        output_video
    ]
    
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise RuntimeError(f"FFmpeg failed: {proc.stderr.decode('utf-8', errors='ignore')}")

    # Cleanup temp slides and audio
    try:
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
    except Exception:
        pass

    return output_video

"""
LeadPulse AI — High-Converting Ad Banner Designer
Generates professional Meta Ad creatives (1080x1080 & 1080x1920)
using Pillow with modern gradient styling, typography, and WhatsApp CTA buttons.
"""
from PIL import Image, ImageDraw, ImageFont
import os
import uuid
import urllib.request
import io
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from .copywriter import get_dynamic_cta

STOCK_PHOTOS = {
    "dental": "https://images.unsplash.com/photo-1629909613654-28e377c37b09?w=1080&q=80",
    "real_estate": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=1080&q=80",
    "fitness": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=1080&q=80",
    "universal": "https://images.unsplash.com/photo-1497366216548-37526070297c?w=1080&q=80"
}

def fetch_stock_photo(industry: str, width: int, height: int) -> Image.Image:
    """Fetch and crop realistic photography for the industry background."""
    url = STOCK_PHOTOS.get(industry) or STOCK_PHOTOS["universal"]
    cache_dir = os.path.join("leadpulse", "static", "cache")
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, f"stock_{industry}.jpg")
    
    if os.path.exists(cache_file):
        try:
            img = Image.open(cache_file).convert("RGB")
            return crop_to_fill(img, width, height)
        except Exception:
            pass
            
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read()
            with open(cache_file, "wb") as f:
                f.write(data)
            img = Image.open(io.BytesIO(data)).convert("RGB")
            return crop_to_fill(img, width, height)
    except Exception as e:
        # Fallback to luxury gradient
        return create_gradient(width, height, (15, 23, 42), (30, 27, 75))

def crop_to_fill(img: Image.Image, width: int, height: int) -> Image.Image:
    """Crop image to fill target aspect ratio centered."""
    target_ratio = width / height
    img_ratio = img.width / img.height
    if img_ratio > target_ratio:
        new_width = int(img.height * target_ratio)
        left = (img.width - new_width) // 2
        img = img.crop((left, 0, left + new_width, img.height))
    else:
        new_height = int(img.width / target_ratio)
        top = (img.height - new_height) // 2
        img = img.crop((0, top, img.width, top + new_height))
    return img.resize((width, height), Image.Resampling.LANCZOS)


def create_gradient(width: int, height: int, start_color: tuple, end_color: tuple) -> Image.Image:
    """Create a vertical gradient image."""
    base = Image.new('RGB', (width, height), start_color)
    top = Image.new('RGB', (width, height), end_color)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        mask_data.extend([int(255 * (y / height))] * width)
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base


def get_font(size: int, bold: bool = False):
    """Load a system TrueType font or fallback to default."""
    font_names = [
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\calibrib.ttf" if bold else "C:\\Windows\\Fonts\\calibri.ttf",
    ]
    for fn in font_names:
        if os.path.exists(fn):
            try:
                return ImageFont.truetype(fn, size)
            except Exception:
                pass
    return ImageFont.load_default()


def generate_ad_banner(
    product_name: str,
    headline: str,
    price_tag: str,
    location: str,
    key_points: list,
    output_dir: str,
    aspect_ratio: str = "1:1",  # "1:1" (1080x1080) or "9:16" (1080x1920)
    brand_name: str = "EXCLUSIVE PREVIEW",
    industry: str = "universal"
) -> str:
    """Generate a high-converting Meta Ad banner PNG image."""
    os.makedirs(output_dir, exist_ok=True)
    
    if aspect_ratio == "9:16":
        width, height = 1080, 1920
    else:
        width, height = 1080, 1080

    # Infer industry from keywords
    combined_text = (product_name + " " + headline).lower()
    if any(k in combined_text for k in ["dental", "smile", "aligner", "teeth", "tooth"]):
        industry = "dental"
    elif any(k in combined_text for k in ["bhk", "flat", "villa", "realty", "estate", "home", "property"]):
        industry = "real_estate"
    elif any(k in combined_text for k in ["gym", "fit", "workout", "trainer", "muscle"]):
        industry = "fitness"
    else:
        industry = "universal"

    # 1. Fetch High-Res Photographic Base & Apply Cinematic Frosted Vignette
    base_photo = fetch_stock_photo(industry, width, height)
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    
    # Smooth gradient darkening toward bottom for crystal clear text readability
    for y in range(height):
        # Top 30% is clearer (alpha ~70), bottom 70% darkens to alpha 235
        ratio = y / height
        alpha = int(70 + 165 * (ratio ** 1.3))
        overlay_draw.line([(0, y), (width, y)], fill=(15, 23, 42, alpha))
        
    img = Image.alpha_composite(base_photo.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(img)

    # 2. Decorative glowing accent glow (semi-transparent circle)
    glow = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse([width - 400, -100, width + 200, 500], fill=(99, 102, 241, 40))
    glow_draw.ellipse([-150, height - 500, 350, height + 100], fill=(16, 185, 129, 30))
    img.paste(glow, (0, 0), glow)

    # Re-acquire draw context
    draw = ImageDraw.Draw(img)

    # 3. Top Brand Pill
    pill_font = get_font(28, bold=True)
    pill_y = 70 if aspect_ratio == "1:1" else 140
    pill_text = f"✨  {brand_name.upper()}  ✨"
    
    bbox = draw.textbbox((0, 0), pill_text, font=pill_font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    px, py = (width - tw) // 2, pill_y
    draw.rounded_rectangle([px - 24, py - 10, px + tw + 24, py + th + 10], radius=20, fill=(49, 46, 129), outline=(99, 102, 241), width=2)
    draw.text((px, py), pill_text, font=pill_font, fill=(199, 210, 254))

    # 4. Product Name
    prod_font = get_font(38, bold=True)
    draw.text((80, pill_y + 90), product_name.upper(), font=prod_font, fill=(148, 163, 184))

    # 5. Bold Main Headline (Wrapped)
    head_font = get_font(56, bold=True)
    words = headline.split()
    lines = []
    curr = []
    for w in words:
        curr.append(w)
        line_str = " ".join(curr)
        bbox = draw.textbbox((0, 0), line_str, font=head_font)
        if (bbox[2] - bbox[0]) > (width - 160):
            curr.pop()
            lines.append(" ".join(curr))
            curr = [w]
    if curr:
        lines.append(" ".join(curr))

    hy = pill_y + 155
    for line in lines[:3]:
        draw.text((80, hy), line, font=head_font, fill=(255, 255, 255))
        hy += 72

    # 6. Glowing Price Badge Card
    badge_y = hy + 30
    draw.rounded_rectangle([80, badge_y, width - 80, badge_y + 110], radius=16, fill=(15, 23, 42), outline=(16, 185, 129), width=3)
    price_font = get_font(52, bold=True)
    draw.text((115, badge_y + 26), f"🏷️ {price_tag}", font=price_font, fill=(52, 211, 153))

    loc_font = get_font(28)
    draw.text((width - 450, badge_y + 38), f"📍 {location}", font=loc_font, fill=(203, 213, 225))

    # 7. Key Feature Bullets
    feat_y = badge_y + 150
    feat_font = get_font(32, bold=False)
    for point in key_points[:3]:
        draw.ellipse([80, feat_y + 10, 94, feat_y + 24], fill=(99, 102, 241))
        draw.text((115, feat_y), point, font=feat_font, fill=(226, 232, 240))
        feat_y += 54

    # 8. WhatsApp CTA Button (High Converting Green Pill)
    btn_y = height - 160 if aspect_ratio == "1:1" else height - 260
    btn_box = [80, btn_y, width - 80, btn_y + 95]
    draw.rounded_rectangle(btn_box, radius=48, fill=(34, 197, 94)) # Emerald Green

    cta_font = get_font(40, bold=True)
    cta_text = get_dynamic_cta(product_name, industry, brand_name)
    c_bbox = draw.textbbox((0, 0), cta_text, font=cta_font)
    c_tw, c_th = c_bbox[2] - c_bbox[0], c_bbox[3] - c_bbox[1]
    draw.text(((width - c_tw) // 2, btn_y + (95 - c_th) // 2 - 4), cta_text, font=cta_font, fill=(255, 255, 255))

    # 9. Bottom Footer Notice
    footer_font = get_font(22)
    footer_text = "⚡ Instant Brochure & Pricing Sent in 5 Seconds · Direct Developer Pricing"
    f_bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
    f_tw = f_bbox[2] - f_bbox[0]
    draw.text(((width - f_tw) // 2, btn_y + 115), footer_text, font=footer_font, fill=(148, 163, 184))

    # Save to disk
    filename = f"banner_{uuid.uuid4().hex[:8]}_{aspect_ratio.replace(':', 'x')}.png"
    filepath = os.path.join(output_dir, filename)
    img.save(filepath, "PNG", quality=95)
    return filepath

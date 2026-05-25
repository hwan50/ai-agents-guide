from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
img = Image.new('RGB', (W, H), '#0D0D0D')
draw = ImageDraw.Draw(img)

# Colors
DARK = '#0D0D0D'
YELLOW = '#FFD700'
WHITE = '#FFFFFF'
GRAY = '#9CA3AF'
GRAY_DARK = '#374151'
ACCENT = '#F59E0B'
CARD_BG = '#1A1A1A'

# Fonts
fp = {
    'heading': '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',
    'body_bold': '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    'body': '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    'mono': '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf',
}

def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

f_h56 = load_font(fp['heading'], 56)
f_h48 = load_font(fp['heading'], 48)
f_h72 = load_font(fp['heading'], 72)
f_b28 = load_font(fp['body_bold'], 28)
f_b24 = load_font(fp['body_bold'], 24)
f_b20 = load_font(fp['body_bold'], 20)
f_b18 = load_font(fp['body_bold'], 18)
f_16 = load_font(fp['body'], 16)
f_14 = load_font(fp['body'], 14)
f_tag = load_font(fp['body_bold'], 12)
f_mono32 = load_font(fp['mono'], 32)
f_mono28 = load_font(fp['mono'], 28)

# Top stickers
def sticker(text, x, y, bg=YELLOW, tc=DARK, font=f_tag):
    bbox = draw.textbbox((0,0), text, font=font)
    tw = bbox[2]-bbox[0]+20
    th = bbox[3]-bbox[1]+12
    draw.rounded_rectangle([x, y, x+tw, y+th], radius=6, fill=bg)
    draw.text((x+10, y+6), text, font=font, fill=tc)
    return x+tw+12

sx = 50
sx = sticker("REAL COST DATA", sx, 35)
sx = sticker("MCP PROTOCOL", sx, 35, bg='#E5E7EB', tc=DARK)
sx = sticker("250× CHEAPER", sx, 35, bg=ACCENT)

# Left: Headline block
y = 115
draw.text((50, y), "Multi-Model", font=f_h56, fill=WHITE)
draw.text((50, y+68), "Pipeline", font=f_h56, fill=WHITE)

# Price line
y_price = y+145
only_w = draw.textbbox((0,0), "Only ", font=f_h48)[2]
draw.text((50, y_price), "Only ", font=f_h48, fill=WHITE)
draw.text((50+only_w, y_price-8), "$0.002", font=f_h72, fill=YELLOW)
q_w = draw.textbbox((0,0), "$0.002", font=f_h72)[2]
draw.text((50+only_w+q_w+10, y_price-8), "?", font=f_h72, fill=YELLOW)

# Subheadline — moved down to avoid overlap
y_sub = y_price + 90
draw.text((50, y_sub), "DeepSeek V4 + Gemini Flash", font=f_b24, fill=WHITE)
draw.text((50, y_sub+32), "Screenshot → Code in 94s · 250× cheaper than Claude", font=f_16, fill=GRAY)

# Benefits — moved down with more spacing
benefits = [
    ("$0.002", "per workflow"),
    ("94s", "Screenshot → React"),
    ("1M", "Token context"),
    ("1,500", "Free/day Gemini"),
]
y_b = y_sub + 95
for i, (big, small) in enumerate(benefits):
    bx = 50 + (i % 2) * 270
    by = y_b + (i // 2) * 100
    draw.text((bx, by), "✓", font=f_b20, fill=YELLOW)
    draw.text((bx+28, by-2), big, font=f_b24, fill=WHITE)
    draw.text((bx+28, by+30), small, font=f_14, fill=GRAY)

# Right: Cost card
cx, cy = 720, 95
cw, ch = 460, 460
draw.rounded_rectangle([cx, cy, cx+cw, cy+ch], radius=12, fill=CARD_BG, outline=YELLOW, width=2)

# Card header
draw.text((cx+30, cy+28), "COST COMPARISON", font=f_b20, fill=WHITE)
draw.text((cx+360, cy+30), "PER TASK", font=f_tag, fill=YELLOW)
draw.line([(cx+30, cy+72), (cx+cw-30, cy+72)], fill=GRAY_DARK, width=1)

# Rows
row_y = cy + 95
row_h = 85
methods = [
    ("DeepSeek + Gemini", "$0.002", YELLOW, "HIGH"),
    ("Claude Code", "$0.50", GRAY, "HIGH"),
    ("GPT-4o", "$0.25", GRAY, "MED"),
]
for i, (name, cost, cost_color, acc) in enumerate(methods):
    ry = row_y + i * row_h
    if i == 0:
        draw.rounded_rectangle([cx+20, ry-5, cx+cw-20, ry+58], radius=6, fill='#2D2D1A')
        draw.text((cx+30, ry+6), "★ RECOMMENDED", font=f_tag, fill=YELLOW)
    
    draw.text((cx+30, ry+30), name, font=f_b18, fill=WHITE)
    # Cost right-aligned
    cost_bbox = draw.textbbox((0,0), cost, font=f_mono32)
    cost_w = cost_bbox[2]-cost_bbox[0]
    draw.text((cx+cw-30-cost_w-80, ry+22), cost, font=f_mono32, fill=cost_color)
    
    # Badge
    draw.rounded_rectangle([cx+cw-95, ry+26, cx+cw-30, ry+50], radius=3, fill=GRAY_DARK)
    draw.text((cx+cw-88, ry+30), f"ACC {acc}", font=f_tag, fill=WHITE)

# Weekly savings
sy = cy + 360
draw.line([(cx+30, sy), (cx+cw-30, sy)], fill=GRAY_DARK, width=1)
draw.text((cx+30, sy+18), "50 components/week:", font=f_16, fill=GRAY)
draw.text((cx+30, sy+44), "Claude: $75/wk", font=f_14, fill=GRAY)
this_text = "→ This: $0.10/wk"
tbbox = draw.textbbox((0,0), this_text, font=f_b20)
tw = tbbox[2]-tbbox[0]
draw.text((cx+cw-30-tw, sy+40), this_text, font=f_b20, fill=YELLOW)

# Bottom URL
draw.text((980, 615), "hwan50.github.io/ai-agents-guide", font=f_14, fill=GRAY_DARK)

# Bottom tags
tags = ["LOW BARRIER", "LOW COST", "OPEN SOURCE", "MCP", "SCREENSHOT→CODE"]
tx = 50
for tag in tags:
    bbox = draw.textbbox((0,0), tag, font=f_tag)
    tw = bbox[2]-bbox[0]+16
    draw.rounded_rectangle([tx, 595, tx+tw, 595+24], radius=3, outline=GRAY_DARK, width=1)
    draw.text((tx+8, 599), tag, font=f_tag, fill=GRAY)
    tx += tw + 10

# Save
out = '/root/.openclaw/workspace/ai-agents-guide/deepseek-gemini-pipeline/hero-image.png'
img.save(out, 'PNG')
print(f'Saved: {out} ({os.path.getsize(out)} bytes)')

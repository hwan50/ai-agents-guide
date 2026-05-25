from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
img = Image.new('RGB', (W, H), '#0D0D0D')
draw = ImageDraw.Draw(img)

# Colors
DARK = '#0D0D0D'
YELLOW = '#FFD700'
YELLOW_SOFT = '#B8972E'
WHITE = '#FFFFFF'
GRAY = '#9CA3AF'
GRAY_DARK = '#374151'
ACCENT = '#F59E0B'
CARD_BG = '#1A1A1A'

# Load fonts - use Noto Sans CJK for Chinese support
font_dir = '/usr/share/fonts/opentype/noto/'
chinese_bold = ImageFont.truetype(font_dir + 'NotoSansCJK-Regular.ttc', 56, index=0)  # SC index
try:
    chinese_large = ImageFont.truetype(font_dir + 'NotoSansCJK-Regular.ttc', 72, index=0)
    chinese_semibold = ImageFont.truetype(font_dir + 'NotoSansCJK-Regular.ttc', 28, index=0)
    chinese_regular = ImageFont.truetype(font_dir + 'NotoSansCJK-Regular.ttc', 20, index=0)
    chinese_small = ImageFont.truetype(font_dir + 'NotoSansCJK-Regular.ttc', 16, index=0)
    chinese_tag = ImageFont.truetype(font_dir + 'NotoSansCJK-Regular.ttc', 14, index=0)
    
    # English fonts
    bold_large = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 56)
    bold_huge = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 72)
    semibold = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)
    regular = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
    small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
except:
    bold_large = bold_huge = semibold = regular = small = chinese_large = chinese_semibold = chinese_regular = chinese_small = chinese_tag = ImageFont.load_default()

# Top: Sticker-style tags
def draw_sticker(text, x, y, bg=YELLOW, text_color=DARK, font=chinese_tag):
    bbox = draw.textbbox((0,0), text, font=font)
    tw = bbox[2] - bbox[0] + 20
    th = bbox[3] - bbox[1] + 12
    draw.rounded_rectangle([x, y, x+tw, y+th], radius=6, fill=bg)
    draw.text((x+10, y+6), text, font=font, fill=text_color)
    return x + tw + 12

# Sticker row at top
sx = 50
sx = draw_sticker("真实成本对比", sx, 35, bg=YELLOW)
sx = draw_sticker("MCP Protocol", sx, 35, bg='#E5E7EB', text_color=DARK)
sx = draw_sticker("250× 更便宜", sx, 35, bg=ACCENT)

# Left: Big headline (English, blog-aligned)
y = 120
draw.text((50, y), "Multi-Model Pipeline", font=chinese_large, fill=WHITE)
draw.text((50, y+85), "Only $0.002 ?", font=bold_huge, fill=YELLOW)

# Subheadline (English, from blog)
y += 175
draw.text((50, y), "DeepSeek V4 + Gemini Flash", font=semibold, fill=WHITE)
draw.text((50, y+32), "Screenshot → Code in 94s, 250× cheaper than Claude", font=regular, fill=GRAY)

# Bottom left: Checkmark benefits
benefits = [
    ("$0.002/次", "per screenshot → code"),
    ("94 秒", "Screenshot → React component"),
    ("1M Token", "DeepSeek context window"),
    ("1500/day", "Gemini Flash free tier"),
]
y_b = 360
for i, (big, small_text) in enumerate(benefits):
    bx = 50 + (i % 2) * 280
    by = y_b + (i // 2) * 110
    # Yellow checkmark
    draw.text((bx, by), "✓", font=semibold, fill=YELLOW)
    # Big number
    draw.text((bx+30, by-4), big, font=chinese_semibold, fill=WHITE)
    # Small desc
    draw.text((bx+30, by+32), small_text, font=chinese_small, fill=GRAY)

# Right side: Card stack
# Main card background with border
card_x = 720
card_y = 100
card_w = 460
card_h = 430
draw.rounded_rectangle([card_x, card_y, card_x+card_w, card_y+card_h], radius=12, fill=CARD_BG, outline=YELLOW, width=2)

# Inner content
draw.text((card_x+30, card_y+30), "成本对比", font=chinese_semibold, fill=WHITE)
draw.text((card_x+340, card_y+32), "真实收益", font=chinese_tag, fill=YELLOW)

# Divider
draw.line([(card_x+30, card_y+75), (card_x+card_w-30, card_y+75)], fill=GRAY_DARK, width=1)

# Cost comparison table
row_y = card_y + 95
row_h = 70
methods = [
    ("DeepSeek + Gemini", "$0.002", YELLOW, "高"),
    ("Claude Code", "$0.50", GRAY, "高"),
    ("GPT-4o", "$0.25", GRAY, "中"),
]
for i, (name, cost, cost_color, acc) in enumerate(methods):
    ry = row_y + i * row_h
    # Highlight bar for winner
    if i == 0:
        draw.rounded_rectangle([card_x+20, ry-5, card_x+card_w-20, ry+50], radius=6, fill='#2D2D1A')
        draw.text((card_x+30, ry+5), "★ 推荐方案", font=chinese_small, fill=YELLOW)
    # Name
    draw.text((card_x+30, ry+25), name, font=chinese_regular, fill=WHITE)
    # Cost
    draw.text((card_x+220, ry+20), cost, font=semibold, fill=cost_color)
    # Accuracy tag
    draw.rounded_rectangle([card_x+320, ry+22, card_x+390, ry+46], radius=3, fill=GRAY_DARK)
    draw.text((card_x+330, ry+26), f"精度{acc}", font=chinese_small, fill=WHITE)

# Bottom of card: Weekly savings
savings_y = card_y + 330
draw.line([(card_x+30, savings_y), (card_x+card_w-30, savings_y)], fill=GRAY_DARK, width=1)
draw.text((card_x+30, savings_y+20), "每周 50 个组件:", font=chinese_regular, fill=GRAY)
draw.text((card_x+30, savings_y+50), "Claude: $75/周", font=chinese_small, fill=GRAY)
draw.text((card_x+230, savings_y+48), "→ 本方案: $0.10/周", font=chinese_semibold, fill=YELLOW)

# Bottom right: URL watermark
draw.text((1050, 615), "hwan50.github.io/ai-agents-guide", font=small, fill=GRAY_DARK)

# Bottom left: Tags
tag_y = 585
tags = ["低门槛", "低成本", "开源", "MCP协议", "截图变代码"]
tx = 50
for tag in tags:
    bbox = draw.textbbox((0,0), tag, font=chinese_small)
    tw = bbox[2]-bbox[0]+16
    draw.rounded_rectangle([tx, tag_y, tx+tw, tag_y+26], radius=3, outline=GRAY_DARK, width=1)
    draw.text((tx+8, tag_y+4), tag, font=chinese_small, fill=GRAY)
    tx += tw + 12

# Save
output_path = '/root/.openclaw/workspace/ai-agents-guide/deepseek-gemini-pipeline/hero-image.png'
img.save(output_path, 'PNG')
print(f'Saved to {output_path}')
print(f'Size: {os.path.getsize(output_path)} bytes')

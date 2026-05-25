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

# Load fonts
try:
    bold_large = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 56)
    bold_huge = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 72)
    bold_title = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 38)
    semibold = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)
    regular = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
    small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
    tag_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 12)
    italic = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf', 16)
except:
    bold_large = bold_huge = bold_title = semibold = regular = small = tag_font = italic = ImageFont.load_default()

# Top: Sticker-style tag
def draw_sticker(text, x, y, bg=YELLOW, text_color=DARK):
    bbox = draw.textbbox((0,0), text, font=tag_font)
    tw = bbox[2] - bbox[0] + 16
    th = bbox[3] - bbox[1] + 10
    # Skewed rect effect (simplified as rounded)
    draw.rounded_rectangle([x, y, x+tw, y+th], radius=4, fill=bg)
    draw.text((x+8, y+5), text, font=tag_font, fill=text_color)
    return x + tw + 10

# Sticker row at top
sx = 50
sx = draw_sticker("真实成本对比", sx, 35)
sx = draw_sticker("MCP Protocol", sx, 35, bg='#E5E7EB', text_color=DARK)
sx = draw_sticker("250× 更便宜", sx, 35, bg=ACCENT)

# Left: Big headline
y = 110
draw.text((50, y), "多模型联动", font=bold_large, fill=WHITE)
draw.text((50, y+70), "只需 $0.002 ?", font=bold_huge, fill=YELLOW)

# Subheadline
y += 170
draw.text((50, y), "DeepSeek V4 推理 + Gemini Flash 识图", font=semibold, fill=GRAY)
draw.text((50, y+32), "截图 → 代码 只要 94 秒，成本 = Claude Code 的 1/250", font=regular, fill=GRAY)

# Bottom left: Checkmark benefits
benefits = [
    ("$0.002/次", "单次截图转代码成本"),
    ("94 秒", "截图 → 可运行 React 组件"),
    ("1M Token", "DeepSeek 上下文窗口"),
    ("1500 次/天", "Gemini Flash 免费额度"),
]
y_b = 340
for i, (big, small_text) in enumerate(benefits):
    bx = 50 + (i % 2) * 280
    by = y_b + (i // 2) * 110
    # Yellow checkmark
    draw.text((bx, by), "✓", font=semibold, fill=YELLOW)
    # Big number
    draw.text((bx+28, by-4), big, font=semibold, fill=WHITE)
    # Small desc
    draw.text((bx+28, by+28), small_text, font=small, fill=GRAY)

# Right side: Card stack (simulating "app screenshot collage")
card_x = 720
card_y = 100
card_w = 460
card_h = 420

# Main card background with border
draw.rounded_rectangle([card_x, card_y, card_x+card_w, card_y+card_h], radius=12, fill=CARD_BG, outline=YELLOW, width=2)

# Inner content
draw.text((card_x+30, card_y+30), "成本计算器", font=semibold, fill=WHITE)
draw.text((card_x+340, card_y+32), "真实收益", font=tag_font, fill=YELLOW)

# Divider
draw.line([(card_x+30, card_y+70), (card_x+card_w-30, card_y+70)], fill=GRAY_DARK, width=1)

# Cost comparison table
row_y = card_y + 90
row_h = 60
methods = [
    ("DeepSeek + Gemini", "$0.002", YELLOW, "高"),
    ("Claude Code", "$0.50-$1.50", GRAY, "高"),
    ("GPT-4o 单模型", "$0.15-$0.40", GRAY, "中"),
]
for i, (name, cost, cost_color, acc) in enumerate(methods):
    ry = row_y + i * row_h
    # Highlight bar for winner
    if i == 0:
        draw.rounded_rectangle([card_x+20, ry-5, card_x+card_w-20, ry+45], radius=6, fill='#2D2D1A')
        draw.text((card_x+30, ry+8), "★ 推荐方案", font=small, fill=YELLOW)
    # Name
    draw.text((card_x+30, ry+25), name, font=regular, fill=WHITE)
    # Cost
    draw.text((card_x+220, ry+20), cost, font=semibold, fill=cost_color)
    # Accuracy tag
    draw.rounded_rectangle([card_x+360, ry+22, card_x+420, ry+42], radius=3, fill=GRAY_DARK)
    draw.text((card_x+370, ry+26), f"精度 {acc}", font=small, fill=WHITE)

# Bottom of card: Weekly savings
savings_y = card_y + 310
draw.line([(card_x+30, savings_y), (card_x+card_w-30, savings_y)], fill=GRAY_DARK, width=1)
draw.text((card_x+30, savings_y+20), "每周做 50 个组件:", font=regular, fill=GRAY)
draw.text((card_x+30, savings_y+50), "Claude Code: $75/周", font=regular, fill=GRAY)
draw.text((card_x+260, savings_y+50), "→ 本方案: $0.10/周", font=semibold, fill=YELLOW)

# Bottom right: URL watermark
draw.text((1050, 610), "hwan50.github.io/ai-agents-guide", font=small, fill=GRAY_DARK)

# Bottom left: Tags
tag_y = 580
tags = ["低门槛", "低成本", "开源工具", "MCP 协议", "截图变代码"]
tx = 50
for tag in tags:
    bbox = draw.textbbox((0,0), tag, font=small)
    tw = bbox[2]-bbox[0]+12
    draw.rounded_rectangle([tx, tag_y, tx+tw, tag_y+24], radius=3, outline=GRAY_DARK, width=1)
    draw.text((tx+6, tag_y+4), tag, font=small, fill=GRAY)
    tx += tw + 10

# Save
output_path = '/root/.openclaw/workspace/ai-agents-guide/deepseek-gemini-pipeline/hero-image.png'
img.save(output_path, 'PNG')
print(f'Saved to {output_path}')
print(f'Size: {os.path.getsize(output_path)} bytes')

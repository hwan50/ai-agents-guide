from PIL import Image, ImageDraw, ImageFont
import random
import os

# Create image
W, H = 1200, 630
img = Image.new('RGB', (W, H), '#F4F0E7')
draw = ImageDraw.Draw(img)

# Colors - deeper and more saturated
INK = '#211F1B'
INK_SOFT = '#46423A'
MUTED = '#7C7567'
COPPER = '#B87333'
PEACH = '#F5C6AA'      # Deeper peach
SAGE = '#B8D4B8'       # Deeper sage
BG = '#F4F0E7'

# Helper: draw hand-drawn style line (slight wobble)
def wobble_line(xy, fill, width=3, wobble=2):
    x1, y1, x2, y2 = xy
    if x1 == x2:  # vertical
        y_start, y_end = min(y1, y2), max(y1, y2)
        x_base = x1
        for y in range(y_start, y_end, 3):
            offset = random.randint(-wobble, wobble)
            draw.line([(x_base+offset, y), (x_base+offset, min(y+3, y_end))], fill=fill, width=width)
    elif y1 == y2:  # horizontal
        x_start, x_end = min(x1, x2), max(x1, x2)
        y_base = y1
        for x in range(x_start, x_end, 3):
            offset = random.randint(-wobble, wobble)
            draw.line([(x, y_base+offset), (min(x+3, x_end), y_base+offset)], fill=fill, width=width)
    else:
        draw.line([(x1, y1), (x2, y2)], fill=fill, width=width)

# Helper: draw hand-drawn rectangle
def hand_rect(box, fill=None, outline=INK, width=3):
    x1, y1, x2, y2 = box
    # Top
    wobble_line((x1, y1, x2, y1), outline, width)
    # Bottom
    wobble_line((x1, y2, x2, y2), outline, width)
    # Left
    wobble_line((x1, y1, x1, y2), outline, width)
    # Right
    wobble_line((x2, y1, x2, y2), outline, width)
    if fill:
        draw.rectangle(box, fill=fill)

# Load fonts
try:
    fraunces_large = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', 68)
    fraunces_sub = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-BoldItalic.ttf', 26)
    fraunces_card = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', 22)
    inter_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 13)
    inter_tag = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 10)
    inter_tiny = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    inter_credit = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf', 11)
    inter_label = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 9)
except:
    fraunces_large = ImageFont.load_default()
    fraunces_sub = fraunces_large
    fraunces_card = fraunces_large
    inter_small = fraunces_large
    inter_tag = fraunces_large
    inter_tiny = fraunces_large
    inter_credit = fraunces_large
    inter_label = fraunces_large

# Draw corner brackets (thicker, hand-drawn)
def draw_bracket(x, y, orientation, size=35):
    s = size
    w = 3
    if orientation == 'tl':
        wobble_line((x, y+s, x, y), INK, w)
        wobble_line((x, y, x+s, y), INK, w)
    elif orientation == 'tr':
        wobble_line((x-s, y, x, y), INK, w)
        wobble_line((x, y, x, y+s), INK, w)
    elif orientation == 'bl':
        wobble_line((x, y-s, x, y), INK, w)
        wobble_line((x, y, x+s, y), INK, w)
    elif orientation == 'br':
        wobble_line((x-s, y, x, y), INK, w)
        wobble_line((x, y, x, y-s), INK, w)

draw_bracket(40, 40, 'tl')
draw_bracket(1160, 40, 'tr')
draw_bracket(40, 590, 'bl')
draw_bracket(1160, 590, 'br')

# Left side: Title
y = 155
draw.text((80, y), 'DEEPSEEK', font=fraunces_large, fill=INK)
draw.text((80, y+78), '+ GEMINI', font=fraunces_large, fill=INK)
draw.text((80, y+155), 'A Multi-Model Coding Pipeline', font=fraunces_sub, fill=COPPER)

# Pill tags
tags = ['VISION', 'REASONING', 'MCP']
tag_x = 80
for tag in tags:
    bbox = draw.textbbox((0,0), tag, font=inter_tag)
    tw = bbox[2]-bbox[0]
    th = bbox[3]-bbox[1]
    pad_x, pad_y = 14, 8
    hand_rect([tag_x, y+205, tag_x+tw+pad_x*2, y+205+th+pad_y*2], outline=INK, width=2)
    draw.text((tag_x+pad_x, y+205+pad_y-1), tag, font=inter_tag, fill=INK)
    tag_x += tw + pad_x*2 + 14

# Right side: Card 1 (Gemini Flash)
card_x, card_y = 610, 150
card_w, card_h = 530, 145
card1_box = [card_x, card_y, card_x+card_w, card_y+card_h]
# Fill background first
draw.rectangle(card1_box, fill=PEACH)
# Draw hand-drawn border on top
hand_rect(card1_box, outline=INK, width=3)
# Vertical divider
wobble_line((card_x+40, card_y, card_x+40, card_y+card_h), INK, 1)

# Number + title
draw.text((card_x+58, card_y+58), '01', font=inter_small, fill=INK)
draw.text((card_x+105, card_y+52), 'Gemini Flash', font=fraunces_card, fill=INK)
draw.text((card_x+105, card_y+88), 'image analysis · OCR · vision', font=inter_tiny, fill=INK_SOFT)

# Arrow between cards
arrow_x = card_x + card_w//2
arrow_y1 = card_y + card_h + 10
arrow_y2 = card_y + card_h + 45
wobble_line((arrow_x, arrow_y1, arrow_x, arrow_y2), INK, 2)
draw.polygon([(arrow_x-6, arrow_y2-8), (arrow_x, arrow_y2+2), (arrow_x+6, arrow_y2-8)], fill=INK)

# Card 2 (DeepSeek V4)
card_y2 = card_y + card_h + 55
card2_box = [card_x, card_y2, card_x+card_w, card_y2+card_h]
draw.rectangle(card2_box, fill=SAGE)
hand_rect(card2_box, outline=INK, width=3)
wobble_line((card_x+40, card_y2, card_x+40, card_y2+card_h), INK, 1)

draw.text((card_x+58, card_y2+58), '02', font=inter_small, fill=INK)
draw.text((card_x+105, card_y2+52), 'DeepSeek V4', font=fraunces_card, fill=INK)
draw.text((card_x+105, card_y2+88), 'code generation · reasoning · 1M context', font=inter_tiny, fill=INK_SOFT)

# Bottom left label
draw.text((80, 605), 'BUILT WITH MCP PROTOCOL', font=inter_label, fill=MUTED)

# Bottom right credit
draw.text((1100, 605), '@hwan50', font=inter_credit, fill=MUTED)

# Save
output_path = '/root/.openclaw/workspace/ai-agents-guide/deepseek-gemini-pipeline/hero-image.png'
img.save(output_path, 'PNG')
print(f'Saved to {output_path}')
print(f'Size: {os.path.getsize(output_path)} bytes')

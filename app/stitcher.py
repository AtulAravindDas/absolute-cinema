from PIL import Image,ImageDraw,ImageFont
import os

# Loading the fonts
def load_font(font_path,size):
    if os.path.exists(font_path):
        font = ImageFont.truetype(font_path, size)
    else:
        font = ImageFont.load_default(size=size)
    return font

narration_font=load_font("/System/Library/Fonts/NewYorkItalic.ttf", 24)
dialogue_font=load_font("/System/Library/Fonts/SFNS.ttf", 24)

#Loading page constraints
PAGE_W, PAGE_H=1200,1600
GUTTER=8
BORDER=12
BG_COLOR=(10,10,10)
USABLE_H = PAGE_H - 2 * BORDER - GUTTER
TOP_H=int(0.55*USABLE_H)
BOTTOM_H=USABLE_H - TOP_H
PANEL_W=PAGE_W-2*BORDER
BOT_W=(PANEL_W - GUTTER) // 2
LINE_H=30
TEXT_PADDING = 10
MAX_LINES = 6

def load_panel(path, w, h):
    try:
        return Image.open(path).convert("RGB").resize((w, h), Image.LANCZOS)
    except FileNotFoundError:
        return Image.new("RGB", (w, h), BG_COLOR)

def _wrap_text(text, font, max_width, draw):
    word_list = text.split(" ")
    lines=[]
    current_string=""
    for word in word_list:
        test_string = current_string + " " + word if current_string else word
        measure=draw.textbbox((0,0), test_string, font=font)
        if measure[2]<=max_width:
            current_string=test_string
        else:
            lines.append(current_string)
            current_string = word
    lines.append(current_string)
    return lines

def _draw_text_overlay(img, narration, dialogue):
    draw = ImageDraw.Draw(img)
    narration_lines = _wrap_text(narration, narration_font, img.width - TEXT_PADDING * 2, draw)
    dialogue_lines = _wrap_text(dialogue, dialogue_font, img.width - TEXT_PADDING * 2, draw)
    lines = [("narr", line) for line in narration_lines] + [("dial", line) for line in dialogue_lines]
    lines = lines[:MAX_LINES]
    bar_h = len(lines) * LINE_H + TEXT_PADDING * 2
    y0 = img.height - bar_h - TEXT_PADDING

    img = img.convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(overlay).rectangle([0, y0, img.width, y0 + bar_h], fill=(0, 0, 0, 200))
    img = Image.alpha_composite(img, overlay)

    draw = ImageDraw.Draw(img)

    for i in range(len(lines)):
        kind,line=lines[i]
        y=y0 + (i * LINE_H) + TEXT_PADDING
        if kind=="narr":
            draw.text((TEXT_PADDING, y), line, font=narration_font, fill=(255, 220, 120, 255))
        else:
            draw.text((TEXT_PADDING, y), line, font=dialogue_font, fill=(255, 255, 255))
    return img.convert("RGB")
        
def stitch_page(page_num, panel_texts, image_dir="outputs/images", output_dir="outputs/pages"):
    os.makedirs(output_dir, exist_ok=True)
    page = Image.new("RGB", (PAGE_W, PAGE_H), BG_COLOR)

    path = os.path.join(image_dir, f"page_{page_num}_panel_1.png")
    p1 = load_panel(path, PANEL_W, TOP_H)
    p1 = _draw_text_overlay(p1, panel_texts[0][0], panel_texts[0][1])
    page.paste(p1, (BORDER, BORDER))

    path = os.path.join(image_dir, f"page_{page_num}_panel_2.png")
    p2 = load_panel(path, BOT_W, BOTTOM_H)
    p2 = _draw_text_overlay(p2, panel_texts[1][0], panel_texts[1][1])
    page.paste(p2, (BORDER, BORDER + TOP_H + GUTTER))

    path = os.path.join(image_dir, f"page_{page_num}_panel_3.png")
    p3 = load_panel(path, BOT_W, BOTTOM_H)
    p3 = _draw_text_overlay(p3, panel_texts[2][0], panel_texts[2][1])
    page.paste(p3, (BORDER + BOT_W + GUTTER, BORDER + TOP_H + GUTTER))

    out_path = os.path.join(output_dir, f"page_{page_num}.png")
    page.save(out_path)
    return out_path
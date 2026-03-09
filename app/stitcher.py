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

def _wrap_text(text, font, max_width, draw):
    word_list = text.split(" ")
    lines=[]
    current_string=""
    for word in word_list:
        test_string = current_string + " " + word if current_string else word
        measure=draw.textbbox((0,0), test_string, font=font)
        print(measure)
        print("\n")
draw=ImageDraw.Draw(Image.new("RGB",(100,100)))
_wrap_text("A Midsummer nights dream", narration_font, BOT_W, draw)
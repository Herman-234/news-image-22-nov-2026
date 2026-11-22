#!/usr/bin/env python3
"""Draw the 22 November 2026 world-news front page as a 1024x1024 PNG.

Deterministic: same input -> same bytes. No network, no timestamps.
Run:  python3 draw.py            (writes entry.png beside this file)

Headlines were verified against live news pages on 22 Nov 2026:
 1. Channel News Asia / France 24 (via news.co.za world archive)
 2. France 24 (via news.co.za world archive)
 3. France 24 (via news.co.za world archive)
 4. France 24 (via news.co.za world archive)
 5. AP wire (via balitangmarino.com international news, dateline TOKYO, Nov 22)
 6. AP wire (via balitangmarino.com international news, dateline LONDON, Nov 22)
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (20, 33, 61)
GOLD = (244, 169, 0)
PAPER = (247, 243, 234)
INK = (24, 24, 24)
GREY = (105, 105, 105)
CARD = (255, 255, 255)
BORDER = (205, 200, 190)
ACCENTS = [(178, 34, 34), (0, 90, 130), (120, 60, 140), (0, 110, 70), (160, 90, 0), (40, 90, 160)]

# (number, region, headline, source)
STORIES = [
    ("1", "MEXICO",
     "Mexico captures FBI most-wanted cartel boss 'El Chapo Isidro' in Sinaloa raid",
     "Channel News Asia"),
    ("2", "FRANCE",
     "French cost-of-living protests enter sixth Saturday as turnout falls",
     "France 24"),
    ("3", "UKRAINE",
     "Russian missile strikes Zelenskyy's hometown Kryvyi Rih, killing two",
     "France 24"),
    ("4", "CLIMATE",
     "COP31 climate talks in Antalya stretch into overtime as deal risks failure",
     "France 24"),
    ("5", "ASIA",
     "Japan and India agree to deepen military and defence industry ties",
     "AP wire"),
    ("6", "TECH",
     "TikTok launches global deepfake-detection tool for public figures",
     "AP wire"),
]

LEAD_DECK = ("FBI most-wanted Fausto Isidro Meza Flores seized after a US "
             "intelligence tip; 11 killed in the violence that followed.")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ---
    d.rectangle([0, 0, W, 146], fill=NAVY)
    f_title = font(BOLD, 64)
    d.text((W / 2, 22), "THE WORLD TODAY", font=f_title, fill=(255, 255, 255),
           anchor="ma")
    f_date = font(BOLD, 30)
    d.text((W / 2, 96), "SUNDAY, 22 NOVEMBER 2026", font=f_date, fill=GOLD,
           anchor="ma")
    d.rectangle([0, 146, W, 150], fill=GOLD)

    # --- lead story ---
    num, region, headline, source = STORIES[0]
    accent = ACCENTS[0]
    d.rectangle([24, 162, 1000, 416], fill=CARD, outline=BORDER, width=2)
    d.rectangle([24, 162, 34, 416], fill=accent)
    d.text((52, 178), num, font=font(BOLD, 64), fill=accent)
    f_lead = font(BOLD, 40)
    lines = wrap(d, headline, f_lead, 830)
    y = 182
    for line in lines[:2]:
        d.text((140, y), line, font=f_lead, fill=INK)
        y += 48
    f_deck = font(REG, 24)
    deck_lines = wrap(d, LEAD_DECK, f_deck, 830)
    y = 182 + 48 * len(lines[:2]) + 10
    for line in deck_lines[:2]:
        d.text((140, y), line, font=f_deck, fill=(70, 70, 70))
        y += 30
    d.text((140, 382), region + "  •  " + source.upper(), font=font(BOLD, 20),
           fill=GREY)

    # --- stories 2-6 ---
    f_head = font(BOLD, 27)
    f_tag = font(BOLD, 18)
    y0 = 424
    for i, (num, region, headline, source) in enumerate(STORIES[1:], start=1):
        accent = ACCENTS[i]
        y1 = y0 + 106
        d.rectangle([24, y0, 1000, y1], fill=CARD, outline=BORDER, width=2)
        d.rectangle([24, y0, 32, y1], fill=accent)
        d.text((46, y0 + 26), num, font=font(BOLD, 40), fill=accent)
        lines = wrap(d, headline, f_head, 850)
        ty = y0 + 12
        for line in lines[:2]:
            d.text((110, ty), line, font=f_head, fill=INK)
            ty += 33
        d.text((110, y0 + 82), region + "  •  " + source.upper(),
               font=f_tag, fill=GREY)
        y0 = y1 + 5

    # --- footer ---
    d.text((W / 2, 982),
           "Sources verified 22 Nov 2026: Channel News Asia  •  France 24  •  AP wire",
           font=font(REG, 16), fill=GREY, anchor="ma")

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()

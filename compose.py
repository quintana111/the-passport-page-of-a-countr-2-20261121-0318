#!/usr/bin/env python3
"""Render the Republic of Meridia passport spread (1024x1024, deterministic)."""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
CREAM = (247, 240, 220)
PAPER = (250, 244, 228)
TEAL = (13, 74, 76)
TEAL_LT = (38, 110, 112)
GOLD = (176, 138, 48)
GOLD_LT = (201, 164, 74)
INK = (30, 42, 44)
BURG = (122, 44, 48)
FAINT = (214, 200, 168)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img, "RGBA")

# ---- outer frame ----
d.rectangle([8, 8, W - 9, H - 9], outline=GOLD, width=4)
d.rectangle([18, 18, W - 19, H - 19], outline=TEAL, width=2)

# ---- guilloche: fine wavy lines across both pages ----
for y0 in range(30, H - 20, 14):
    pts = []
    for x in range(24, W - 24, 8):
        y = y0 + 3 * math.sin(x / 46.0 + y0 / 30.0)
        pts.append((x, y))
    d.line(pts, fill=(TEAL[0], TEAL[1], TEAL[2], 14), width=1)

# ---- spine ----
d.line([512, 22, 512, H - 22], fill=TEAL, width=3)
d.line([518, 22, 518, H - 22], fill=GOLD, width=1)
d.line([506, 22, 506, H - 22], fill=GOLD, width=1)


def centered(x0, x1, y, text, font, fill):
    w = d.textlength(text, font=font)
    d.text(((x0 + x1 - w) / 2, y), text, font=font, fill=fill)


def star(cx, cy, r_out, r_in, n=8, fill=None, outline=None, width=2):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill, outline=outline)
    if outline:
        d.line(pts + [pts[0]], fill=outline, width=width)


def emblem(cx, cy, r, fill=TEAL, gold=GOLD):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=fill, width=3)
    d.ellipse([cx - r * 0.78, cy - r * 0.78, cx + r * 0.78, cy + r * 0.78],
              outline=gold, width=2)
    star(cx, cy, r * 0.62, r * 0.26, 8, fill=gold)
    d.ellipse([cx - r * 0.12, cy - r * 0.12, cx + r * 0.12, cy + r * 0.12],
              fill=fill)


# ================= TOP BANNER (spans the spread) =================
emblem(512, 78, 34)
centered(24, 1000, 122, "REPUBLIC OF MERIDIA", F(SERIF_B, 44), TEAL)
centered(24, 1000, 172, "P A S S P O R T", F(SERIF_B, 20), GOLD)
d.line([180, 205, 844, 205], fill=GOLD, width=2)
d.line([180, 209, 844, 209], fill=TEAL, width=1)

# ================= LEFT PAGE: data page =================
LX0, LX1 = 30, 500
centered(LX0, LX1, 224, "DATA PAGE", F(SANS_B, 15), TEAL_LT)
d.line([LX0 + 30, 248, LX1 - 30, 248], fill=GOLD, width=1)

# --- geometric portrait (stylized, not a real person) ---
px0, py0, px1, py1 = 52, 262, 212, 452
d.rectangle([px0, py0, px1, py1], outline=TEAL, width=3)
d.rectangle([px0 + 5, py0 + 5, px1 - 5, py1 - 5], outline=GOLD, width=1)
# faceted background
d.polygon([(px0 + 6, py0 + 6), (px1 - 6, py0 + 6), (px1 - 6, py1 - 6),
           (px0 + 6, py1 - 6)], fill=(226, 232, 224))
d.polygon([(px0 + 6, py0 + 6), (150, py0 + 6), (110, 320), (px0 + 6, 360)],
          fill=(196, 214, 206))
d.polygon([(150, py0 + 6), (px1 - 6, py0 + 6), (px1 - 6, 300), (150, 380)],
          fill=(168, 192, 184))
# head + shoulders, geometric
d.ellipse([108, 292, 156, 348], fill=(232, 196, 158))          # face
d.polygon([(108, 330), (132, 306), (156, 330), (156, 348), (108, 348)],
          fill=(226, 186, 146))
d.polygon([(96, 352), (132, 336), (168, 352), (186, py1 - 6), (78, py1 - 6)],
          fill=TEAL)                                            # shoulders
d.polygon([(118, 352), (132, 344), (146, 352), (146, py1 - 6), (118, py1 - 6)],
          fill=GOLD_LT)                                         # collar
d.ellipse([118, 318, 128, 326], fill=INK)                       # eye L
d.ellipse([136, 318, 146, 326], fill=INK)                       # eye R
d.arc([118, 330, 146, 344], 20, 160, fill=BURG, width=2)        # smile
# hair: teal geometric cap
d.pieslice([104, 288, 160, 330], 180, 360, fill=TEAL)
d.polygon([(104, 306), (118, 290), (132, 300), (146, 290), (160, 306),
           (160, 296), (104, 296)], fill=TEAL)
centered(px0, px1, py1 + 8, "PHOTO", F(SANS, 11), TEAL_LT)

# --- coat of arms (small shield) ---
sx, sy = 300, 330
d.polygon([(sx - 52, sy - 40), (sx + 52, sy - 40), (sx + 52, sy + 18),
           (sx, sy + 58), (sx - 52, sy + 18)], outline=GOLD, width=3)
d.polygon([(sx - 44, sy - 32), (sx + 44, sy - 32), (sx + 44, sy + 14),
           (sx, sy + 48), (sx - 44, sy + 14)], fill=TEAL)
star(sx, sy - 2, 24, 10, 8, fill=GOLD)
d.line([sx - 44, sy + 22, sx + 44, sy + 22], fill=GOLD, width=2)
centered(LX0, LX1, sy + 66, "COAT OF ARMS", F(SANS, 11), TEAL_LT)

# --- data fields ---
fields = [
    ("SURNAME", "AMARA"),
    ("GIVEN NAMES", "ELENA MARIS"),
    ("NATIONALITY", "MERIDIAN"),
    ("DATE OF BIRTH", "14 MAR 1998"),
    ("PLACE OF BIRTH", "PORT SERENNE"),
    ("SEX", "F"),
    ("DATE OF ISSUE", "02 JUN 2026"),
    ("DATE OF EXPIRY", "01 JUN 2036"),
    ("PASSPORT No.", "MD 4829137"),
]
y = 486
for label, value in fields:
    d.text((52, y), label, font=F(SANS, 12), fill=TEAL_LT)
    d.text((52, y + 15), value, font=F(SERIF_B, 19), fill=INK)
    y += 42

# --- MRZ strip ---
mz0, mz1 = 30, 500
d.rectangle([mz0, 872, mz1, 1000 - 26], fill=(238, 231, 210),
            outline=TEAL, width=2)
d.text((44, 884), "P<MDAMARA<<ELENA<MARIS<<<<<<<<<<<<<<<<<<<<",
       font=F(MONO, 15), fill=INK)
d.text((44, 908), "MD4829137<7MD9803142F3606015<<<<<<<<<<<<<<04",
       font=F(MONO, 15), fill=INK)
d.text((44, 934), "MERIDIA  \u2022  ELECTRONIC PASSPORT  \u2022  MD",
       font=F(SANS_B, 11), fill=TEAL)

# ================= RIGHT PAGE: visa / stamp page =================
RX0, RX1 = 524, 994
centered(RX0, RX1, 224, "VISAS & ENTRY STAMPS", F(SANS_B, 15), TEAL_LT)
d.line([RX0 + 30, 248, RX1 - 30, 248], fill=GOLD, width=1)

# --- large watermark emblem behind stamps ---
d.ellipse([759 - 150, 560 - 150, 759 + 150, 560 + 150],
          outline=(TEAL[0], TEAL[1], TEAL[2], 46), width=4)
d.ellipse([759 - 118, 560 - 118, 759 + 118, 560 + 118],
          outline=(GOLD[0], GOLD[1], GOLD[2], 46), width=3)
star(759, 560, 92, 38, 8, fill=None, outline=(TEAL[0], TEAL[1], TEAL[2], 46))


def stamp(cx, cy, city, date, code, color, angle):
    """One entry stamp, drawn on its own layer then rotated."""
    LW, LH = 270, 160
    layer = Image.new("RGBA", (LW, LH), (0, 0, 0, 0))
    s = ImageDraw.Draw(layer)
    s.ellipse([6, 6, LW - 7, LH - 7], outline=color, width=4)
    s.ellipse([14, 14, LW - 15, LH - 15], outline=color, width=2)
    pts = []
    for i in range(16):
        r = 22 if i % 2 == 0 else 9
        a = math.pi * i / 8 - math.pi / 2
        pts.append((LW / 2 + r * math.cos(a), 48 + r * math.sin(a)))
    s.polygon(pts, fill=color)
    s.text((LW / 2, 74), city, font=F(SERIF_B, 19), fill=color, anchor="ma")
    s.text((LW / 2, 100), date, font=F(SANS_B, 14), fill=color, anchor="ma")
    s.text((LW / 2, 120), code, font=F(MONO, 12), fill=color, anchor="ma")
    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=False)
    img.paste(layer, (cx - LW // 2, cy - LH // 2), layer)


stamp(655, 340, "PORT SERENNE", "02 JUN 2026", "ENTRY  \u2022  MD-01", TEAL, -8)
stamp(885, 370, "CALDOR BAY", "19 JUL 2026", "ENTRY  \u2022  MD-07", BURG, 7)
stamp(655, 550, "VELMORA", "03 SEP 2026", "ENTRY  \u2022  MD-12", TEAL, 6)
stamp(885, 580, "OSTARA", "21 OCT 2026", "ENTRY  \u2022  MD-19", BURG, -6)

# --- visa note box ---
d.rectangle([RX0 + 24, 700, RX1 - 24, 800], outline=TEAL, width=2)
d.rectangle([RX0 + 29, 705, RX1 - 29, 795], outline=GOLD, width=1)
centered(RX0, RX1, 716, "VISA — MULTIPLE ENTRY", F(SERIF_B, 17), TEAL)
centered(RX0, RX1, 742, "Valid for travel to all Meridian ports",
         F(SERIF, 14), INK)
centered(RX0, RX1, 766, "Issued 02 JUN 2026  \u2022  Port Serenne",
         F(SERIF, 14), INK)

# --- signature line ---
d.line([RX0 + 60, 880, RX1 - 60, 880], fill=INK, width=1)
centered(RX0, RX1, 888, "E. Amara", font=F(SERIF, 26), fill=INK)
centered(RX0, RX1, 922, "HOLDER'S SIGNATURE", F(SANS, 11), TEAL_LT)

# --- footer ---
centered(24, 1000, H - 22, "", F(SANS, 10), TEAL_LT)

img.save("/tmp/passport-test.png", "PNG", optimize=True)
print("saved /tmp/passport-test.png")

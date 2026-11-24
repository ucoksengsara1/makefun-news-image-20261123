#!/usr/bin/env python3
"""THE MORNING MERIDIAN — NI23 G4 composer, akun8 (@ucoksengsara4119).

A 1024x1024 front page for Monday 23 November 2026, drawn with PIL.
Lead story: pool #9 — a Russian cargo ship still burns off Finland
(the pool says "still burns", never "sunk"). Every story, number and
discard comes from the locked pool file ni23-pool.md and nowhere else.
Two layouts share the same locked data for the duel: A fills the card
grid row by row, B fills it column by column and swaps the bottom band.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

FD = "/home/hatch/workspace/tools/bedah-19nov/news-image/fonts/"
W = 1024
PAPER = (252, 252, 250)
WHITE = (255, 255, 255)
ROYAL = (27, 58, 143)
ROYAL_D = (16, 34, 92)
INK = (24, 28, 40)
GREY = (96, 102, 116)
LIGHT = (214, 221, 235)
RED = (139, 26, 26)
GOLD = (176, 132, 30)
GREEN = (46, 110, 60)

def fb(n):
    return ImageFont.truetype(FD + "Archivo-Bold.ttf", n)

def fr(n):
    return ImageFont.truetype(FD + "Archivo.ttf", n)

def fsr(n):
    return ImageFont.truetype(FD + "Archivo.ttf", n)

def pfb(n):
    return ImageFont.truetype(FD + "PlayfairDisplay-Black.ttf", n)

def pf(n):
    return ImageFont.truetype(FD + "PlayfairDisplay-Bold.ttf", n)

# ---- locked pool data -------------------------------------------------
# grid tuple: (num, region, topic, src, head, deck, kind)
grid = [
 (4, "Middle East", "MIDDLE EAST · WAR", "AP live",
  "Tankers Burn in Hormuz",
  "Tankers ablaze as Iran-US war widens in Gulf.", "flame"),
 (5, "Europe", "EUROPE · CLIMATE", "BBC · AP",
  "COP31 Ends With No Deal in Antalya",
  "COP31: Turkiye draft omits fossil fuels.", "leaf"),
 (6, "Europe", "EUROPE · WAR", "BBC",
  "Boy Pulled Alive From Kyiv Rubble",
  "Boy, 7, freed after hours; 6 killed.", "boy"),
 (7, "North America", "N. AMERICA · POLITICS", "BBC",
  "House Majority Confirmed 258-173",
  "258-173: biggest majority since 1992.", "capitol"),
 (8, "Global", "GLOBAL · TECHNOLOGY", "Salonvision wire",
  "UN Talks on Killer AI Go On",
  "Talks on lethal AI continue in Geneva.", "robot"),
 (9, "Southeast Asia", "WORLD COURT · JUSTICE", "Guardian · NYT",
  "ICJ: Myanmar Guilty of Genocide",
  "700,000+ Rohingya fled in 2017.", "gavel"),
 (10, "South Asia", "SOUTH ASIA · CRICKET", "ObserverVoice",
  "India's Record 720/9 at Wellington",
  "720/9 declared - highest NZ Test total.", "cricket"),
 (11, "Global", "GLOBAL · MARKETS", "ObserverVoice",
  "Gold Slides to $3,538 an Ounce",
  "Down $2,000 from record $5,595.", "coin"),
 (12, "North America", "N. AMERICA · SAFETY", "BBC",
  "US Army to Blast Old Explosives",
  "US Army defies court order in Iowa.", "bolt"),
]

GRID_META = {
 4: ("STRAIT OF HORMUZ", "REPORTED"), 5: ("ANTALYA, TURKIYE", "OFFICIAL"),
 6: ("KYIV, UKRAINE", "REPORTED"), 7: ("WASHINGTON", "OFFICIAL"),
 8: ("GENEVA", "ONGOING"), 9: ("THE HAGUE", "OFFICIAL"),
 10: ("WELLINGTON", "REPORTED"), 11: ("LONDON", "REPORTED"),
 12: ("IOWA, USA", "OFFICIAL"),
}
GRID_REGION = {4: "Middle East", 5: "Europe", 6: "Europe",
               7: "North America", 8: "Global", 9: "Southeast Asia",
               10: "South Asia", 11: "Global", 12: "North America"}

NUMS = [
 ("258-173", "House majority, confirmed (card 7)"),
 ("720/9d", "India's record total (card 10)"),
 ("14", "missing in Kyiv (card 3)"),
 ("6", "killed in Kyiv strike (card 6)"),
 ("$3,538", "gold per ounce (card 11)"),
 ("50", "missing, Indonesia update (story 26)"),
]

TL = [
 ("00:02Z", "UN killer-AI talks roll on"),
 ("02:00Z", "Albanese on COP31"),
 ("06:30Z", "Kyiv boy freed"),
 ("09:15Z", "House confirmed"),
 ("12:40Z", "Gold at $3,538"),
 ("15:05Z", "India declare 720/9"),
]

BRIEFS = [
 "Russia-bound ship towed after attack (BBC)",
 "Houthi missile intercepted (AFP)",
 "Swimmer crosses Hormuz for wildlife",
 "US releases more UFO footage (BBC)",
 "Albanese: COP31 failure, hard times (AFP)",
 "Benghazi blast: suspected drone (BBC)",
 "UK-EU reset a 'landmark' - Burnham (BBC)",
 "Thousands march in Lisbon on costs",
 "Myanmar junta: ASEAN ruling 'unfair'",
 "Escaped lion spreads fear in Turkiye",
 "Nepal PM Shah meets Modi in Delhi",
 "Guru Nanak Jayanti marked today",
 "UP air-raid drills in 75 districts",
 "Indonesia fire update: 7 dead, 50 missing",
 "India chase win; NZ 119/2 Wellington",
 "India win ODI series in NZ 3-2",
 "Snooker: Anupama defends world title",
 "World Chess Championship draws fans",
 "Kota pilgrim bus tragedy: 9 dead",
 "Tata Steel pipe sale: Rs 28,000 cr",
 "SpiceJet audit call; IndiGo 65.9%",
 "IFFI 2026: BRICS roundtable in Goa",
 "Modi opens AI Centre at IIT Patna",
 "JEE Main 2027 registration closes",
 "Google: $5m for IIT Kharagpur AI",
 "India-EU pact likely signed 16 Dec",
]

BRIEF_REGIONS = [
 "Europe", "Middle East", "Middle East", "North America", "Asia-Pacific",
 "Africa", "Europe", "Europe", "Southeast Asia", "Europe", "South Asia",
 "South Asia", "South Asia", "Southeast Asia", "South Asia", "South Asia",
 "South Asia", "Global", "South Asia", "South Asia", "South Asia",
 "South Asia", "South Asia", "South Asia", "South Asia", "Europe",
]

dc = ("Xi-Trump-Putin summit - 19 Nov 2026 · "
      "Missiles fall in Poland - 20 Nov 2026 · "
      "Paolo Bulgari dies - reported 22 Nov 2026 · "
      "Kim Jong-un speech, Seoul - 22 Nov 2026 · "
      "Kerch Bridge strike - reported 22 Nov 2026 · "
      "S. Korea minister quits - 22 Nov 2026 · "
      "Indonesia factory fire itself - 22 Nov 2026")

PINS = [(1, 29, 2), (2, 26, 4), (3, 30, 2), (4, 27, 5), (5, 28, 3),
        (6, 31, 3), (7, 7, 2), (8, 27, 1), (9, 40, 5), (10, 44, 6),
        (11, 28, 1), (12, 4, 3)]

MAP_LEGEND = "Dotted map: numbered marks - each numbered dot marks a story's place."

REGION_ORDER = ["Europe", "South Asia", "North America", "Middle East",
                "Southeast Asia", "Global", "Africa", "Asia-Pacific"]
REGION_LABEL = {"Europe": "EUROPE", "South Asia": "SOUTH ASIA",
                "North America": "N. AMERICA", "Middle East": "MIDDLE EAST",
                "Southeast Asia": "SE ASIA", "Global": "GLOBAL",
                "Africa": "AFRICA", "Asia-Pacific": "ASIA-PACIFIC"}
REGION_COL = {"Europe": ROYAL, "South Asia": GREEN, "North America": RED,
              "Middle East": GOLD, "Southeast Asia": (110, 60, 140),
              "Global": (30, 130, 150), "Africa": (190, 100, 30),
              "Asia-Pacific": GREY}
LEAD_REGIONS = ["Europe", "Middle East", "Europe"]

def region_counts():
    counts = {}
    for r in LEAD_REGIONS:
        counts[r] = counts.get(r, 0) + 1
    for t in grid:
        counts[t[1]] = counts.get(t[1], 0) + 1
    for r in BRIEF_REGIONS:
        counts[r] = counts.get(r, 0) + 1
    return counts

COUNTS = region_counts()
TOTAL = 3 + len(grid) + len(BRIEFS)
NREG = len(COUNTS)

# ---- helpers ----------------------------------------------------------
def wrap(d, text, font, width, maxlines):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    if len(lines) > maxlines:
        lines = lines[:maxlines]
        last = lines[-1]
        while last and d.textlength(last + "…", font=font) > width:
            last = last[:-1]
        lines[-1] = last + "…"
    return lines

def motif(d, kind, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(233, 238, 248))
    cx, cy = x + s // 2, y + s // 2
    u = s / 64.0
    def P(px, py):
        return (x + px * u, y + py * u)
    if kind == "ship":
        d.polygon([P(6, 36), P(58, 36), P(50, 48), P(14, 48)], fill=ROYAL_D)
        d.rectangle([cx - 14 * u, cy - 8 * u, cx + 10 * u, cy + 4 * u], fill=ROYAL)
        d.polygon([P(30, 6), P(38, 22), P(22, 22)], fill=RED)
        d.arc([x + 8 * u, y + 48 * u, x + 24 * u, y + 58 * u], 0, 180, fill=ROYAL, width=2)
        d.arc([x + 38 * u, y + 48 * u, x + 54 * u, y + 58 * u], 0, 180, fill=ROYAL, width=2)
    elif kind == "radar":
        d.line([P(10, 52), P(54, 52)], fill=INK, width=3)
        d.line([P(32, 52), P(32, 26)], fill=INK, width=3)
        d.polygon([P(32, 26), P(56, 10), P(60, 19), P(36, 33)], fill=ROYAL)
        for r in (9, 16, 23):
            d.arc([cx - r * u, cy - 30 * u, cx + r * u, cy - 12 * u], 300, 60, fill=RED, width=2)
    elif kind in ("building", "boy"):
        d.rectangle([P(12, 10), P(38, 52)], fill=ROYAL)
        d.rectangle([P(42, 24), P(56, 52)], fill=GREY)
        for r in range(3):
            for c in range(2):
                d.rectangle([P(17 + c * 11, 16 + r * 12), P(24 + c * 11, 23 + r * 12)], fill=WHITE)
        d.polygon([P(6, 52), P(58, 52), P(48, 43), P(18, 44)], fill=(180, 186, 200))
        if kind == "boy":
            d.ellipse([P(44, 30), P(54, 40)], fill=RED)
    elif kind == "flame":
        d.polygon([P(32, 4), P(46, 32), P(40, 50), P(24, 50), P(18, 32)], fill=RED)
        d.polygon([P(32, 22), P(39, 36), P(35, 48), P(28, 48), P(25, 36)], fill=GOLD)
        d.rectangle([P(8, 52), P(56, 56)], fill=ROYAL_D)
    elif kind == "leaf":
        d.ellipse([P(12, 8), P(44, 40)], fill=GREEN)
        d.line([P(14, 52), P(42, 10)], fill=(30, 80, 42), width=3)
        d.line([P(10, 54), P(54, 10)], fill=RED, width=4)
    elif kind == "capitol":
        d.polygon([P(6, 22), P(58, 22), P(32, 6)], fill=ROYAL_D)
        for i in range(5):
            d.rectangle([P(10 + i * 10, 24), P(15 + i * 10, 46)], fill=ROYAL)
        d.rectangle([P(6, 48), P(58, 54)], fill=ROYAL_D)
    elif kind == "robot":
        d.rectangle([P(14, 18), P(50, 46)], outline=ROYAL_D, width=3)
        d.ellipse([P(21, 26), P(29, 34)], fill=RED)
        d.ellipse([P(35, 26), P(43, 34)], fill=RED)
        d.line([P(32, 18), P(32, 8)], fill=INK, width=2)
        d.ellipse([P(29, 4), P(35, 10)], fill=GOLD)
    elif kind == "gavel":
        d.line([P(12, 52), P(52, 12)], fill=(120, 84, 30), width=5)
        d.rectangle([P(40, 6), P(58, 19)], fill=ROYAL_D)
        d.rectangle([P(8, 54), P(34, 59)], fill=ROYAL_D)
    elif kind == "cricket":
        d.rectangle([P(28, 6), P(37, 44)], fill=(190, 150, 70))
        d.ellipse([P(42, 36), P(54, 48)], fill=RED)
        for i in range(3):
            d.line([P(10 + i * 8, 48), P(10 + i * 8, 56)], fill=INK, width=2)
    elif kind == "coin":
        d.ellipse([P(10, 10), P(54, 54)], fill=GOLD)
        d.ellipse([P(17, 17), P(47, 47)], outline=(140, 100, 20), width=2)
        d.text((cx, cy), "$", font=fb(26), fill=(110, 78, 10), anchor="mm")
    elif kind == "bolt":
        d.polygon([P(36, 4), P(18, 34), P(29, 34), P(24, 60), P(46, 28), P(34, 28)], fill=GOLD)
    else:
        d.ellipse([P(14, 14), P(50, 50)], outline=ROYAL, width=3)

def _card_frame(d, x, y, w, h, num, loc, chip, big=False):
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=RED if big else LIGHT,
                width=3 if big else 1)
    d.rectangle([x, y, x + w, y + 19], fill=ROYAL_D)
    d.text((x + 7, y + 3), "%d · %s" % (num, loc), font=fb(12), fill=WHITE)
    f = fb(11)
    cw = int(d.textlength(chip, font=f)) + 12
    d.rounded_rectangle([x + w - cw - 5, y + 2, x + w - 5, y + 17], 4,
                        fill=RED if chip == "CLAIM" else GOLD)
    d.text((x + w - cw + 1, y + 4), chip, font=f, fill=WHITE)

def lead(d, x, y, w, h, num, loc, src, head, deck, kind, chip, cat):
    _card_frame(d, x, y, w, h, num, loc, chip, big=True)
    motif(d, kind, x + w - 62, y + 24, 54)
    d.text((x + 8, y + 23), cat, font=fb(10), fill=RED)
    yy = y + 36
    for ln in wrap(d, head, fb(30), w - 72, 2):
        d.text((x + 8, yy), ln, font=fb(30), fill=INK)
        yy += 31
    for ln in wrap(d, deck, fr(15), w - 16, 1):
        d.text((x + 8, y + h - 27), ln, font=fr(15), fill=(52, 58, 72))
    d.text((x + 8, y + h - 12), "Source: " + src, font=fsr(11), fill=GREY)

def mini(d, x, y, w, h, num, loc, src, head, deck, kind, chip, cat):
    _card_frame(d, x, y, w, h, num, loc, chip)
    motif(d, kind, x + w - 62, y + 24, 54)
    d.text((x + 8, y + 23), cat, font=fb(10), fill=RED)
    yy = y + 34
    for ln in wrap(d, head, fb(28), w - 72, 2):
        d.text((x + 8, yy), ln, font=fb(28), fill=INK)
        yy += 29
    for ln in wrap(d, deck, fr(15), w - 16, 1):
        d.text((x + 8, y + h - 27), ln, font=fr(15), fill=(52, 58, 72))
    d.text((x + 8, y + h - 12), "Source: " + src, font=fsr(11), fill=GREY)

def grid_card(d, t, x, y, w, h):
    num, region, topic, src, head, deck, kind = t
    loc, chip = GRID_META[num]
    mini(d, x, y, w, h, num, loc, src, head, deck, kind, chip, topic)

# ---- furniture --------------------------------------------------------
def topbar(d):
    d.rectangle([0, 0, W, 24], fill=ROYAL_D)
    d.text((12, 5), "THE MORNING MERIDIAN", font=fb(13), fill=WHITE)
    kick = "%d STORIES · %d REGIONS · EVERY ONE FROM 23 NOVEMBER 2026" % (TOTAL, NREG)
    d.text((W - 12, 5), kick, font=fb(13), fill=(200, 212, 240), anchor="ra")

def masthead(d):
    d.text((W // 2, 30), "Monday 23 November 2026", font=pfb(76), fill=ROYAL_D, anchor="ma")
    d.text((W // 2, 112), "THE MORNING MERIDIAN", font=pf(24), fill=ROYAL, anchor="ma")
    sub = "Russian cargo ship still burns off Finland · IRGC claims Patriot radars hit · 14 missing in Kyiv, Zelenskiy says"
    d.text((W // 2, 140), sub, font=fb(13), fill=RED, anchor="ma")
    d.line([12, 158, W - 12, 158], fill=ROYAL, width=2)

def region_strip(d, y):
    x = 12
    d.text((x, y + 3), "REGIONS:", font=fb(12), fill=ROYAL_D)
    x += 72
    for name in REGION_ORDER:
        if name not in COUNTS:
            continue
        label = "%s %d" % (REGION_LABEL[name], COUNTS[name])
        w_ = int(d.textlength(label, font=fb(12))) + 14
        d.rounded_rectangle([x, y, x + w_, y + 19], 4, fill=REGION_COL[name])
        d.text((x + 7, y + 3), label, font=fb(12), fill=WHITE)
        x += w_ + 7

def timeline(d, y):
    d.rectangle([12, y, W - 12, y + 22], fill=(238, 241, 248))
    x = 18
    for t, ev in TL:
        d.text((x, y + 4), t, font=fb(12), fill=RED)
        x += int(d.textlength(t, font=fb(12))) + 4
        seg = ev + "   ·   "
        d.text((x, y + 4), seg, font=fr(12), fill=INK)
        x += int(d.textlength(seg, font=fr(12)))

def numbers_strip(d, y, h=52):
    d.rectangle([12, y, W - 12, y + h], fill=ROYAL_D)
    colw = (W - 24) // 6
    for i, (val, lab) in enumerate(NUMS):
        x = 12 + i * colw + 10
        d.text((x, y + 4), val, font=fb(25), fill=WHITE)
        for j, ln in enumerate(wrap(d, lab, fr(10), colw - 18, 2)):
            d.text((x, y + 32 + j * 11), ln, font=fr(10), fill=(200, 212, 240))

MAP = [
 "     . . . . . . . . . . . . . . . . . . . . . .",
 "  . ##### . . . . . .  #### . ######### . . . .",
 " . ####### . . . . . ###### . ########### . . .",
 "  . ##### . . . . . . ##### .  ######### . ## .",
 " . . ### . . . . . . . ### . . ######## . #### ",
 " . . ## . . . . . . . . ## . . . ###### . ### .",
 " . . # . . . . . . . . ### . . . #### . . ## . ",
 "  . . . . . . . . . . . ## . . . . ## . . . . .",
]

def dotted_map(d, x, y, w_):
    d.text((x, y), "WHERE IT HAPPENED", font=fb(12), fill=ROYAL_D)
    for j, ln in enumerate(wrap(d, MAP_LEGEND, fr(10), w_, 2)):
        d.text((x, y + 15 + j * 11), ln, font=fr(10), fill=GREY)
    cw = w_ / 46.0
    for r, row in enumerate(MAP):
        for i, ch in enumerate(row[:46]):
            if ch == "#":
                d.ellipse([x + i * cw, y + 40 + r * 8, x + i * cw + 4, y + 44 + r * 8],
                          fill=(170, 182, 205))
    for n, col, row in PINS:
        px, py = x + col * cw, y + 40 + row * 8
        d.ellipse([px - 7, py - 7, px + 8, py + 8], fill=RED)
        d.text((px, py - 5), str(n), font=fb(9), fill=WHITE, anchor="ma")

def datecheck(d, x, y, w_):
    d.text((x, y), "DATE CHECK — NOT TODAY'S NEWS:", font=fb(12), fill=RED)
    items = [s.strip() for s in dc.split("·")]
    colw = (w_ - 10) // 2
    for i, item in enumerate(items):
        cx = x + (i % 2) * colw
        cy = y + 18 + (i // 2) * 16
        for ln in wrap(d, "✗ " + item, fr(11), colw - 6, 1):
            d.text((cx, cy), ln, font=fr(11), fill=(90, 30, 26))

def also_band(d, y, cols=4):
    d.text((12, y), "ALSO ON THE MERIDIAN — MORE OF MONDAY 23 NOVEMBER 2026",
           font=fb(13), fill=ROYAL_D)
    colw = (W - 24 - (cols - 1) * 10) // cols
    per = (len(BRIEFS) + cols - 1) // cols
    for ci in range(cols):
        x = 12 + ci * (colw + 10)
        for ri, b in enumerate(BRIEFS[ci * per:(ci + 1) * per]):
            line = "%d. %s" % (13 + ci * per + ri, b)
            for ln in wrap(d, line, fsr(11), colw, 1):
                d.text((x, y + 17 + ri * 12), ln, font=fsr(11), fill=INK)

def footer(d, y):
    d.line([12, y, W - 12, y], fill=ROYAL, width=2)
    d.text((12, y + 5),
           "HOW SURE: REPORTED = carried by named wires · CLAIM = one side's account, labelled as such · ONGOING = still developing · OFFICIAL / ON RECORD = officials on the record.",
           font=fr(11), fill=INK)
    d.text((12, y + 19),
           "Every story happened, or was first reported, on Monday 23 November 2026. Contested claims are attributed. · Original drawings.",
           font=fb(11), fill=ROYAL_D)

# ---- layouts ----------------------------------------------------------
def _trio(d, y0, colw, gap, rowh):
    lead(d, 12, y0, colw, rowh, 1, "GULF OF FINLAND", "BBC · JagranJosh",
         "Cargo Ship Still Burns Off Finland",
         "Still burns; a 2nd Russia-bound ship towed.", "ship",
         "ONGOING", "EUROPE · SEA WAR")
    mini(d, 12 + colw + gap, y0, colw, rowh, 2, "BAHRAIN", "AP / AFP wires",
         "IRGC Claims It Hit Patriot Radars",
         "IRGC claims 2 Patriot radars destroyed.", "radar",
         "CLAIM", "MIDDLE EAST · WAR")
    mini(d, 12 + 2 * (colw + gap), y0, colw, rowh, 3, "KYIV, UKRAINE", "JagranJosh",
         "14 Missing in Kyiv, Zelenskiy Says",
         "14 missing after drone hit Kyiv building.", "building",
         "ON RECORD", "EUROPE · WAR")

def build_a():
    img = Image.new("RGB", (W, W), PAPER)
    d = ImageDraw.Draw(img)
    topbar(d); masthead(d)
    region_strip(d, 164)
    timeline(d, 188)
    y0, rowh, gap = 216, 123, 4
    colw = (W - 24 - 2 * gap) // 3
    _trio(d, y0, colw, gap, rowh)
    for idx, t in enumerate(grid):
        r, i = divmod(idx, 3)
        grid_card(d, t, 12 + i * (colw + gap), y0 + (r + 1) * (rowh + gap), colw, rowh)
    yy = y0 + 4 * rowh + 3 * gap + 6
    numbers_strip(d, yy)
    by = yy + 60
    dotted_map(d, 12, by, 400)
    datecheck(d, 428, by, 584)
    also_band(d, by + 104)
    footer(d, 992)
    return img

def build_b():
    img = Image.new("RGB", (W, W), PAPER)
    d = ImageDraw.Draw(img)
    topbar(d); masthead(d)
    region_strip(d, 164)
    timeline(d, 188)
    y0, rowh, gap = 216, 123, 4
    colw = (W - 24 - 2 * gap) // 3
    _trio(d, y0, colw, gap, rowh)
    order = [grid[i] for i in (0, 3, 6, 1, 4, 7, 2, 5, 8)]
    for idx, t in enumerate(order):
        r, i = divmod(idx, 3)
        grid_card(d, t, 12 + i * (colw + gap), y0 + (r + 1) * (rowh + gap), colw, rowh)
    yy = y0 + 4 * rowh + 3 * gap + 6
    numbers_strip(d, yy)
    by = yy + 60
    datecheck(d, 12, by, 560)
    dotted_map(d, 596, by, 416)
    also_band(d, by + 104)
    footer(d, 992)
    return img

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "A"
    img = build_a() if which == "A" else build_b()
    img.save(sys.argv[2], optimize=True)
    print(sys.argv[2], img.size)

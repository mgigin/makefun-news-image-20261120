#!/usr/bin/env python3
"""Build entry.png v3: one-page world-news broadsheet for Friday 20 Nov 2026.

Original layout drawn with PIL at 2x supersample, downsampled to 1024x1024.
Deterministic: no randomness, no network. main.ts only copies entry.png.
Design goal vs v2: bolder graphic panels with large labels (legible at 300px),
honest region-chip counts computed from the 35-story set, Tokyo close -5.1%.
"""
from PIL import Image, ImageDraw, ImageFont
import math

S = 2
W = H = 1024 * S
PAPER = (248, 244, 233)
INK = (18, 30, 58)
RED = (178, 34, 26)
NAVY = (16, 38, 92)
GREY = (95, 95, 95)
LIGHT = (231, 225, 207)

FD = "/usr/share/fonts/truetype/dejavu/"
def F(name, size):
    return ImageFont.truetype(FD + name, int(size * S))

SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def text(xy, s, font, fill=INK, anchor="la"):
    d.text((xy[0] * S, xy[1] * S), s, font=font, fill=fill, anchor=anchor)

def tw(s, font):
    return d.textlength(s, font=font) / S

def rect(x0, y0, x1, y1, fill=None, outline=None, width=1):
    d.rectangle([x0 * S, y0 * S, x1 * S, y1 * S], fill=fill, outline=outline,
                width=int(width * S))

def line(x0, y0, x1, y1, fill=INK, width=1):
    d.line([x0 * S, y0 * S, x1 * S, y1 * S], fill=fill, width=int(width * S))

def wrap(s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(t, font) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines

MX = 26

# ---------- kicker ----------
text((MX, 14), "THE WORLD IN ONE DAY", F(SANS_B, 14), RED)
text((1024 - MX, 14), "35 STORIES · 7 REGIONS · EVERY ONE DATED FRIDAY 20 NOVEMBER 2026",
     F(SANS_B, 11), INK, anchor="ra")
line(MX, 36, 1024 - MX, 36, INK, 2.5)

# ---------- masthead ----------
text((512, 42), "Friday 20 November 2026", F(SERIF_B, 60), INK, anchor="ma")
text((512, 112),
     "Russian missiles hit Kyiv's bridges  ·  Cyclone Akvan strikes India  ·  "
     "An AI sell-off sinks Asia's markets  ·  UK and EU seal a deal",
     F(SERIF, 14), INK, anchor="ma")
line(MX, 138, 1024 - MX, 138, INK, 1)

# ---------- stat band ----------
stats = [
    ("3", "bridges over the Dnipro damaged in Kyiv"),
    ("300,000+", "people moved to shelters before Akvan"),
    ("-6.2%", "Taiwan's share index, Friday's close"),
    ("100,000", "youth visas a year in the UK-EU deal"),
    ("2.3%", "Japan's consumer inflation in October"),
    ("118", "runs by Glenn Phillips against India"),
]
colw = (1024 - 2 * MX) / 6
for i, (num, lab) in enumerate(stats):
    x = MX + i * colw
    text((x, 146), num, F(SERIF_B, 23), RED)
    for j, ln in enumerate(wrap(lab, F(SANS, 9.5), colw - 10)):
        text((x, 174 + j * 11.5), ln, F(SANS, 9.5), INK)
    if i:
        line(x - 6, 148, x - 6, 202, LIGHT, 1)
line(MX, 208, 1024 - MX, 208, INK, 1)

# ---------- region chips (counts computed from the 35 stories below) ----------
regions = [("EUROPE 10", (37, 99, 235)), ("ASIA 11", (190, 24, 93)),
           ("MIDDLE EAST 4", (124, 58, 237)), ("AFRICA 1", (21, 128, 61)),
           ("AMERICAS 6", (217, 119, 6)), ("OCEANIA 3", (8, 145, 178))]
x = MX
for name, col in regions:
    wch = tw(name, F(SANS_B, 10)) + 16
    rect(x, 216, x + wch, 236, fill=col)
    text((x + wch / 2, 220), name, F(SANS_B, 10), (255, 255, 255), anchor="ma")
    x += wch + 6

# ---------- lead illustrations ----------
def ill_kyiv(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(14, 30, 74))
    rect(x, y + h - 24, x + w, y + h, fill=(32, 84, 146))
    line(x + 8, y + h - 38, x + w - 8, y + h - 38, (205, 215, 235), 3)
    for fx in (0.22, 0.5, 0.78):
        txp = x + w * fx
        line(txp, y + 16, txp, y + h - 24, (205, 215, 235), 3)
        line(txp, y + 16, txp - 34, y + h - 38, (155, 175, 210), 1)
        line(txp, y + 16, txp + 34, y + h - 38, (155, 175, 210), 1)
    for fx, fy, r in ((0.22, 0.44, 13), (0.5, 0.37, 16), (0.78, 0.44, 13)):
        cx, cy = x + w * fx, y + h * fy
        for k in range(10):
            a = k * math.pi / 5
            line(cx, cy, cx + r * math.cos(a), cy + r * math.sin(a), (250, 180, 60), 2)
        d.ellipse([(cx - 6) * S, (cy - 6) * S, (cx + 6) * S, (cy + 6) * S], fill=(255, 216, 92))
    text((x + 8, y + 6), "KYIV", F(SANS_B, 17), (255, 255, 255))
    text((x + w - 8, y + 6), "3 bridges hit", F(SANS_B, 11), (255, 216, 92), anchor="ra")

def ill_cyclone(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(216, 198, 152))
    d.polygon([(x * S, (y + h) * S), ((x + w * 0.62) * S, (y + h) * S),
               ((x + w) * S, (y + h * 0.45) * S), ((x + w) * S, (y + h) * S)],
              fill=(22, 98, 124))
    cx, cy = x + w * 0.70, y + h * 0.46
    for r in range(36, 4, -6):
        d.arc([(cx - r) * S, (cy - r * 0.8) * S, (cx + r) * S, (cy + r * 0.8) * S],
              start=200 + r * 4, end=520 + r * 4, fill=(246, 246, 241), width=int(3 * S))
    d.ellipse([(cx - 4) * S, (cy - 4) * S, (cx + 4) * S, (cy + 4) * S], fill=(246, 246, 241))
    text((x + 8, y + 6), "CYCLONE AKVAN", F(SANS_B, 16), (58, 46, 18))
    text((x + 8, y + h - 20), "Landfall · 8 am", F(SANS_B, 11), (58, 46, 18))

def ill_markets(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(16, 16, 24))
    text((x + 8, y + 6), "AI SELL-OFF", F(SANS_B, 17), (255, 255, 255))
    text((x + 8, y + 28), "Asia, Friday's close", F(SANS_B, 10), (242, 122, 112))
    pts = [(0.05, 0.60), (0.20, 0.66), (0.35, 0.62), (0.48, 0.74), (0.58, 0.80)]
    xy = [(x + w * a, y + h * b) for a, b in pts]
    for i in range(len(xy) - 1):
        line(xy[i][0], xy[i][1], xy[i + 1][0], xy[i + 1][1], (236, 72, 62), 3)
    rows = [("Taipei", "-6.2%"), ("Seoul", "-5.2%"), ("Tokyo", "-5.1%"), ("Hong Kong", "-1.9%")]
    for i, (lab, val) in enumerate(rows):
        yy = y + 50 + i * 13.5
        text((x + w - 108, yy), lab, F(SANS, 8.5), (205, 205, 205))
        text((x + w - 8, yy), val, F(SANS_B, 9.5), (242, 122, 112), anchor="ra")

leads = [
    (ill_kyiv, "1  KYIV, UKRAINE · WAR", "OFFICIALS' COUNT",
     "Russian missiles hit three Kyiv bridges",
     "An overnight barrage of about 110 missiles and 400 drones killed at "
     "least nine people across Ukraine and cut power and water in the capital.",
     "(Reuters, AP)"),
    (ill_cyclone, "2  ODISHA, INDIA · CYCLONE", "CONFIRMED · IMD",
     "Cyclone Akvan comes ashore in eastern India",
     "The storm crossed the coast near Gopalpur from about 8 am after more "
     "than 300,000 people were moved to shelters. No deaths were reported.",
     "(IMD, PTI)"),
    (ill_markets, "3  TAIPEI · SEOUL · TOKYO · MARKETS", "CLOSING PRICES",
     "AI sell-off sinks Asia's stock markets",
     "Taiwan's index fell 6.2% to end its worst week since 1991. Seoul lost "
     "5.2% and Tokyo 5.1% as chipmakers led the slide.",
     "(Reuters, Anadolu)"),
]
cw = (1024 - 2 * MX - 16) / 3
for i, (ill, kicker, tag, head, body, src) in enumerate(leads):
    x = MX + i * (cw + 8)
    ill(x, 246, cw, 110)
    text((x, 362), kicker, F(SANS_B, 9), RED)
    text((x + cw, 362), tag, F(SANS, 7.8), GREY, anchor="ra")
    yy = 376
    for ln in wrap(head, F(SERIF_B, 17), cw):
        text((x, yy), ln, F(SERIF_B, 17), INK); yy += 20.5
    yy += 2
    for ln in wrap(body, F(SANS, 9.5), cw):
        text((x, yy), ln, F(SANS, 9.5), INK); yy += 12
    text((x, yy + 1), src, F(SANS, 8.5), GREY)
line(MX, 496, 1024 - MX, 496, INK, 1)

# ---------- mid cards with graphic panels ----------
def panel(x, y, w, h, bg, label, sub, draw_fn):
    rect(x, y, x + w, y + h, fill=bg)
    draw_fn(x, y, w, h)
    text((x + 6, y + 4), label, F(SANS_B, 12.5), (255, 255, 255))
    text((x + 6, y + h - 15), sub, F(SANS, 7.5), (255, 255, 255))

def g_flags(x, y, w, h):
    # two flags: blue with yellow stars circle + red-white-blue stripes
    rect(x + 8, y + h - 30, x + 44, y + h - 16, fill=(30, 60, 160))
    for k in range(8):
        a = k * math.pi / 4
        cx, cy = x + 26 + 7 * math.cos(a), y + h - 23 + 4 * math.sin(a)
        d.ellipse([(cx - 1.6) * S, (cy - 1.6) * S, (cx + 1.6) * S, (cy + 1.6) * S], fill=(255, 220, 80))
    rect(x + 52, y + h - 30, x + 88, y + h - 16, fill=(200, 40, 50))
    line(x + 52, y + h - 23, x + 88, y + h - 23, (255, 255, 255), 3)
    line(x + 70, y + h - 30, x + 70, y + h - 16, (255, 255, 255), 3)

def g_globe(x, y, w, h):
    cx, cy = x + w - 26, y + h - 22
    d.ellipse([(cx - 14) * S, (cy - 14) * S, (cx + 14) * S, (cy + 14) * S], outline=(255, 255, 255), width=int(2 * S))
    line(cx - 14, cy, cx + 14, cy, (255, 255, 255), 1)
    d.arc([(cx - 6) * S, (cy - 14) * S, (cx + 6) * S, (cy + 14) * S], 0, 360, fill=(255, 255, 255), width=int(1 * S))

def g_missile(x, y, w, h):
    line(x + 16, y + h - 14, x + w - 30, y + 26, (255, 255, 255), 3)
    d.polygon([((x + w - 30) * S, (y + 22) * S), ((x + w - 20) * S, (y + 30) * S), ((x + w - 34) * S, (y + 34) * S)], fill=(255, 255, 255))
    line(x + 16, y + h - 14, x + 26, y + h - 22, (250, 190, 70), 2)

def g_shield(x, y, w, h):
    cx, cy = x + w - 26, y + h - 22
    d.polygon([(cx * S, (cy - 14) * S), ((cx + 12) * S, (cy - 9) * S), ((cx + 10) * S, (cy + 6) * S),
               (cx * S, (cy + 14) * S), ((cx - 10) * S, (cy + 6) * S), ((cx - 12) * S, (cy - 9) * S)],
              outline=(255, 255, 255), width=int(2 * S))

def g_banner(x, y, w, h):
    rect(x + 12, y + h - 30, x + w - 12, y + h - 20, fill=(255, 255, 255))
    line(x + 20, y + h - 20, x + 20, y + h - 8, (255, 255, 255), 2)
    line(x + w - 20, y + h - 20, x + w - 20, y + h - 8, (255, 255, 255), 2)

def g_chart(x, y, w, h):
    for i, hh in enumerate((10, 16, 22)):
        rect(x + w - 44 + i * 12, y + h - 8 - hh, x + w - 37 + i * 12, y + h - 8, fill=(255, 255, 255))

def g_scales(x, y, w, h):
    cx, cy = x + w - 26, y + h - 22
    line(cx, cy - 13, cx, cy + 9, (255, 255, 255), 2)
    line(cx - 13, cy - 10, cx + 13, cy - 10, (255, 255, 255), 2)
    line(cx - 13, cy - 10, cx - 17, cy + 2, (255, 255, 255), 1); line(cx - 13, cy - 10, cx - 9, cy + 2, (255, 255, 255), 1)
    line(cx + 13, cy - 10, cx + 9, cy + 2, (255, 255, 255), 1); line(cx + 13, cy - 10, cx + 17, cy + 2, (255, 255, 255), 1)
    line(cx - 8, cy + 12, cx + 8, cy + 12, (255, 255, 255), 2)

def g_derrick(x, y, w, h):
    cx, cy = x + w - 26, y + h - 22
    line(cx - 11, cy + 14, cx, cy - 14, (255, 255, 255), 2); line(cx + 11, cy + 14, cx, cy - 14, (255, 255, 255), 2)
    line(cx - 7, cy + 3, cx + 7, cy + 3, (255, 255, 255), 1); line(cx - 9, cy + 9, cx + 9, cy + 9, (255, 255, 255), 1)

def g_chip(x, y, w, h):
    cx, cy = x + w - 26, y + h - 22
    rect(cx - 10, cy - 10, cx + 10, cy + 10, outline=(255, 255, 255), width=2)
    rect(cx - 4, cy - 4, cx + 4, cy + 4, fill=(255, 255, 255))
    for dx in (-6, 0, 6):
        line(cx + dx, cy - 14, cx + dx, cy - 10, (255, 255, 255), 2)
        line(cx + dx, cy + 10, cx + dx, cy + 14, (255, 255, 255), 2)

def g_bat(x, y, w, h):
    line(x + 14, y + h - 12, x + 38, y + h - 32, (255, 255, 255), 4)
    d.ellipse([(x + 38) * S, (y + h - 20) * S, (x + 47) * S, (y + h - 11) * S], fill=(255, 255, 255))

cards = [
    ((30, 60, 160), "UK-EU DEAL", "Agreed · Reuters", g_flags,
     "5", "BRUSSELS · DIPLOMACY", "UK and EU seal a \"reset\" deal",
     "Food trade, youth visas, carbon link.", "(Reuters)"),
    ((15, 118, 110), "COP31: NO DEAL", "Ongoing · UN News", g_globe,
     "4", "ANTALYA · CLIMATE", "COP31 reaches its last day with no deal",
     "The draft text leaves out fossil fuels.", "(AP, UN News)"),
    ((150, 30, 30), "POLAND: MISSILE", "Minister says · Reuters", g_missile,
     "6", "EASTERN POLAND · SECURITY", "Russian cruise missile lands in Poland",
     "It fell in a field; two airports paused.", "(AP, Reuters)"),
    ((124, 58, 237), "IRAQ: ARMY IN", "Witnessed · Reuters", g_shield,
     "7", "CENTRAL IRAQ · SECURITY", "Iraqi army enters a militia stronghold",
     "Troops deploy to Jurf al-Sakhar.", "(Reuters)"),
    ((190, 24, 93), "ITALY: STRIKE", "Reported · Reuters", g_banner,
     "8", "ITALY · LABOUR", "General strike over Italy's budget",
     "Workers and students march.", "(Reuters, CGIL)"),
    ((21, 128, 61), "JAPAN: +2.3%", "Official data · Reuters", g_chart,
     "12", "TOKYO · ECONOMY", "Japan's inflation picks up to 2.3%",
     "A December rate rise stays in view.", "(Statistics Bureau)"),
    ((201, 138, 27), "SEOUL: IMPEACH", "Party decision · Yonhap", g_scales,
     "10", "SEOUL · POLITICS", "Korea's ruling party to impeach top judge",
     "It follows an overturned conviction.", "(Yonhap)"),
    ((217, 119, 6), "KENYA: OIL", "Ceremony held · allAfrica", g_derrick,
     "11", "TURKANA, KENYA · ENERGY", "Kenya starts drilling its first oil well",
     "First crude is due on 1 December.", "(allAfrica)"),
    ((75, 85, 99), "NVIDIA: -14%", "Reported · Reuters", g_chip,
     "9", "US · TECH", "Nvidia sinks 14% on SEC probe report",
     "SEC said to examine its accounting.", "(Reuters)"),
    ((8, 145, 178), "PHILLIPS: 118", "Scorecard · ICC", g_bat,
     "13", "WELLINGTON · CRICKET", "Phillips hits 118 against India",
     "Hundreds v India in all three formats.", "(ICC)"),
]
sw = (1024 - 2 * MX - 4 * 8) / 5
for i, (bg, label, sub, fn, num, place, head, body, src) in enumerate(cards):
    x = MX + (i % 5) * (sw + 8)
    y = 504 + (i // 5) * 104
    panel(x, y, sw, 46, bg, label, sub, fn)
    text((x, y + 52), f"{num}  {place}", F(SANS_B, 7.8), RED)
    yy = y + 65
    for ln in wrap(head, F(SERIF_B, 10.5), sw)[:2]:
        text((x, yy), ln, F(SERIF_B, 10.5), INK); yy += 12.5
    for ln in wrap(body, F(SANS, 8), sw)[:1]:
        text((x, yy), ln, F(SANS, 8), INK); yy += 10
    text((x, y + 98), src, F(SANS, 7), GREY)
line(MX, 716, 1024 - MX, 716, INK, 1)

# ---------- world map + more stories ----------
text((MX, 724), "WHERE IT HAPPENED", F(SANS_B, 10.5), RED)
MX0, MY0, MW, MH = MX, 742, 336, 150
rect(MX0, MY0, MX0 + MW, MY0 + MH, fill=(241, 236, 221), outline=LIGHT, width=1)
LAND = (198, 180, 142)
continents = [
    [(0.03, 0.30), (0.10, 0.16), (0.22, 0.12), (0.27, 0.24), (0.24, 0.40), (0.17, 0.44), (0.12, 0.52), (0.07, 0.44), (0.03, 0.38)],
    [(0.16, 0.56), (0.23, 0.54), (0.27, 0.66), (0.23, 0.86), (0.19, 0.90), (0.17, 0.72)],
    [(0.46, 0.18), (0.55, 0.14), (0.58, 0.26), (0.54, 0.34), (0.48, 0.32), (0.45, 0.26)],
    [(0.47, 0.38), (0.56, 0.36), (0.60, 0.50), (0.56, 0.70), (0.51, 0.72), (0.47, 0.55)],
    [(0.58, 0.16), (0.78, 0.12), (0.90, 0.22), (0.88, 0.38), (0.78, 0.48), (0.70, 0.58), (0.66, 0.44), (0.60, 0.30)],
    [(0.80, 0.62), (0.90, 0.60), (0.93, 0.72), (0.85, 0.78), (0.80, 0.72)],
]
for poly in continents:
    d.polygon([((MX0 + MW * a) * S, (MY0 + MH * b) * S) for a, b in poly], fill=LAND)
pins = {1: (0.565, 0.26), 2: (0.72, 0.44), 3: (0.85, 0.34), 4: (0.605, 0.32),
        5: (0.49, 0.215), 6: (0.56, 0.21), 7: (0.635, 0.375), 8: (0.495, 0.305),
        9: (0.10, 0.34), 10: (0.84, 0.35), 11: (0.545, 0.52), 12: (0.905, 0.29),
        13: (0.955, 0.80)}
for n, (a, b) in pins.items():
    cx, cy = MX0 + MW * a, MY0 + MH * b
    d.ellipse([(cx - 6.5) * S, (cy - 6.5) * S, (cx + 6.5) * S, (cy + 6.5) * S], fill=RED)
    text((cx, cy - 4.5), str(n), F(SANS_B, 7), (255, 255, 255), anchor="ma")
text((MX, MY0 + MH + 6), "Each number is the story with that number on this page.",
     F(SANS, 7.5), GREY)

LX = MX + MW + 18
text((LX, 724), "ALSO ON FRIDAY 20 NOVEMBER — 22 MORE STORIES", F(SANS_B, 10.5), RED)
more = [
    "14 Lviv: rail station strike kills 2 (BBC)",
    "15 Estonia: shut 5 Russia crossings Dec 1 (Reuters)",
    "16 Hormuz: tanker hit, fire, no casualties (UKMTO)",
    "17 Yemen: coalition hits Hodeidah port (Reuters)",
    "18 China: loan rates held: 3.0% / 3.5% (PBOC)",
    "19 Delhi: Pakistan minister at SCO forum (PTI)",
    "20 Barcelona: cancer pill: 60.7% respond (EORTC)",
    "21 Argentina: country risk past 1,000 to 1,070 (JPMorgan)",
    "22 Washington: Trump threatens data-centre penalties (AJP)",
    "23 Tokyo: SoftBank shares fall 14.6% (Morningstar)",
    "24 Seoul: Kospi falls about 5% (Reuters)",
    "25 Ganjam: 209 mm rain as Akvan crosses (PTI)",
    "26 Lebanon: Israeli strikes hit the south (Anadolu)",
    "27 Berlin: pupils strike over conscription (Al Jazeera)",
    "28 Wellington: Nicholls 175* in 216-run stand (ICC)",
    "29 Copenhagen: Greenland defence bill approved (AFP)",
    "30 London: UK, Norway fund 2 naval vessels (BBC)",
    "31 Jakarta: asset-forfeiture bill passes (Reuters)",
    "32 Washington: Iran war cost $48.3bn (Reuters)",
    "33 Florida: St Johns River at 18.7 ft, a record (NWS)",
    "34 Iowa: Army postpones 68-barrel blast (AP)",
    "35 Sydney: ASX 200 falls 1.58% in a week (AAP)",
]
colw2 = (1024 - MX - LX - 10) / 2
for i, s in enumerate(more):
    x = LX + (i // 11) * (colw2 + 10)
    y = 742 + (i % 11) * 15.5
    num, rest = s.split(" ", 1)
    text((x, y), num, F(SANS_B, 8.5), RED)
    text((x + 20, y), rest, F(SANS, 8.5), INK)

# ---------- date check ----------
DY = 916
rect(MX, DY, 1024 - MX, DY + 60, outline=RED, width=1.5)
text((MX + 10, DY + 6), "DATE CHECK", F(SANS_B, 10.5), RED)
check = ("Left out on purpose — Thursday 19 Nov news: ICJ Myanmar verdict; Shenzhen Trump-Xi-Putin summit; "
         "Anthropic's IPO debut; GTA VI launch; Bukele's third-term filing; Senegal migrant boat; Tonga's "
         "drought emergency. Wed 18 Nov: $190.4m Van Gogh sale. Not yet happened, so not shown: "
         "BepiColombo's Mercury orbit capture (Sat 21 Nov), any final COP31 text (due Sat morning), "
         "the ATP Finals final (Sun 22 Nov), and Estonia's border closure (1 Dec).")
yy = DY + 21
for ln in wrap(check, F(SANS, 8.5), 1024 - 2 * MX - 20):
    text((MX + 10, yy), ln, F(SANS, 8.5), INK); yy += 11

text((512, 984),
     "Every story here happened, or was first reported, on Friday 20 November 2026. Officials' counts are attributed.",
     F(SANS, 8.5), INK, anchor="ma")
text((512, 998),
     "Sources named beside each story · Original drawings",
     F(SANS, 8.5), GREY, anchor="ma")

out = img.resize((1024, 1024), Image.LANCZOS)
out = out.quantize(colors=256, method=Image.MEDIANCUT)
out.save("entry.png", optimize=True)
print("wrote entry.png", out.size)

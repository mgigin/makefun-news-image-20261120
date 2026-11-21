#!/usr/bin/env python3
"""Build entry.png: one-page world-news poster for Friday 20 November 2026.

Original layout: cream broadsheet, navy ink, red accents. Drawn with PIL at
2x supersample, downsampled to 1024x1024. Deterministic: no randomness,
no network. The shipped program (main.ts) only copies entry.png to /output.
"""
from PIL import Image, ImageDraw, ImageFont
import math

S = 2                      # supersample factor
W = H = 1024 * S
PAPER = (247, 243, 232)
INK = (20, 33, 61)
RED = (179, 35, 27)
GOLD = (201, 138, 27)
TEAL = (15, 118, 110)
GREY = (90, 90, 90)
LIGHT = (232, 226, 208)

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

MX = 28  # side margin

# ---------- kicker row ----------
y = 16
text((MX, y), "THE WORLD IN ONE DAY", F(SANS_B, 13), RED)
right = "35 STORIES · 7 REGIONS · EVERY ONE DATED FRIDAY 20 NOVEMBER 2026"
text((1024 - MX, y), right, F(SANS_B, 10.5), INK, anchor="ra")
line(MX, y + 22, 1024 - MX, y + 22, INK, 2)

# ---------- masthead ----------
text((512, 44), "Friday 20 November 2026", F(SERIF_B, 54), INK, anchor="ma")
text((512, 108),
     "Russian missiles hit Kyiv's bridges  ·  Cyclone Akvan strikes India  ·  "
     "An AI sell-off sinks Asia's markets  ·  UK and EU seal a deal",
     F(SERIF, 13.5), INK, anchor="ma")
line(MX, 134, 1024 - MX, 134, INK, 1)

# ---------- stat band ----------
stats = [
    ("3", "bridges hit over the Dnipro in Kyiv"),
    ("300,000+", "people moved to shelters before Akvan"),
    ("-6.2%", "Taiwan's index at Friday's close"),
    ("100,000", "youth visas a year in the UK-EU deal"),
    ("2.3%", "Japan consumer inflation in October"),
    ("118", "Phillips runs against India"),
]
colw = (1024 - 2 * MX) / 6
for i, (num, lab) in enumerate(stats):
    x = MX + i * colw
    text((x, 142), num, F(SERIF_B, 21), RED)
    for j, ln in enumerate(wrap(lab, F(SANS, 9), colw - 10)):
        text((x, 168 + j * 11), ln, F(SANS, 9), INK)
    if i:
        line(x - 6, 144, x - 6, 196, LIGHT, 1)
line(MX, 202, 1024 - MX, 202, INK, 1)

# ---------- region chips + timeline ----------
regions = [("EUROPE 10", (37, 99, 235)), ("ASIA 10", (190, 24, 93)),
           ("MIDDLE EAST 4", (124, 58, 237)), ("AFRICA 1", (21, 128, 61)),
           ("AMERICAS 6", (217, 119, 6)), ("OCEANIA 3", (8, 145, 178)),
           ("GLOBAL 1", (75, 85, 99))]
x = MX
for name, col in regions:
    wch = tw(name, F(SANS_B, 9.5)) + 14
    rect(x, 210, x + wch, 228, fill=col)
    text((x + wch / 2, 214), name, F(SANS_B, 9.5), (255, 255, 255), anchor="ma")
    x += wch + 6

rect(MX, 234, MX + 108, 252, fill=RED)
text((MX + 54, 238), "THE DAY IN UTC", F(SANS_B, 9.5), (255, 255, 255), anchor="ma")
timeline = [("00:00", "Kyiv bridges hit"), ("02:00", "Akvan landfall"),
            ("05:30", "Taiwan ends -6.2%"), ("05:50", "Missile lands in Poland"),
            ("15:00", "COP31 runs past close"), ("19:10", "SEC eyes Nvidia")]
tx = MX + 122
for t, ev in timeline:
    text((tx, 236), t, F(SANS_B, 10), INK)
    text((tx, 250), ev, F(SANS, 8.5), GREY)
    tx += 146
line(MX, 266, 1024 - MX, 266, INK, 1)

# ---------- lead illustrations ----------
def ill_kyiv(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(16, 32, 72))
    # river
    rect(x, y + h - 26, x + w, y + h, fill=(30, 80, 140))
    # bridge deck + towers
    line(x + 8, y + h - 40, x + w - 8, y + h - 40, (200, 210, 230), 3)
    for fx in (0.22, 0.5, 0.78):
        txp = x + w * fx
        line(txp, y + 18, txp, y + h - 26, (200, 210, 230), 3)
        line(txp, y + 18, txp - 34, y + h - 40, (150, 170, 205), 1)
        line(txp, y + 18, txp + 34, y + h - 40, (150, 170, 205), 1)
    # explosion bursts
    for fx, fy, r in ((0.22, 0.45, 13), (0.5, 0.38, 16), (0.78, 0.45, 13)):
        cx, cy = x + w * fx, y + h * fy
        for k in range(10):
            a = k * math.pi / 5
            line(cx, cy, cx + r * math.cos(a), cy + r * math.sin(a), (250, 180, 60), 2)
        d.ellipse([(cx - 6) * S, (cy - 6) * S, (cx + 6) * S, (cy + 6) * S], fill=(255, 214, 90))
    text((x + 8, y + h - 20), "KYIV · 3 BRIDGES HIT", F(SANS_B, 10), (255, 255, 255))

def ill_cyclone(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(214, 196, 150))
    # sea corner
    d.polygon([(x * S, (y + h) * S), ((x + w * 0.62) * S, (y + h) * S),
               ((x + w) * S, (y + h * 0.45) * S), ((x + w) * S, (y + h) * S)],
              fill=(23, 96, 120))
    # spiral
    cx, cy = x + w * 0.68, y + h * 0.42
    for r in range(34, 4, -6):
        d.arc([(cx - r) * S, (cy - r * 0.8) * S, (cx + r) * S, (cy + r * 0.8) * S],
              start=200 + r * 4, end=520 + r * 4, fill=(245, 245, 240), width=int(3 * S))
    d.ellipse([(cx - 4) * S, (cy - 4) * S, (cx + 4) * S, (cy + 4) * S], fill=(245, 245, 240))
    text((x + 8, y + 8), "CYCLONE AKVAN", F(SANS_B, 15), (60, 48, 20))
    text((x + 8, y + h - 20), "LANDFALL · 8 AM", F(SANS_B, 10), (60, 48, 20))

def ill_markets(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(18, 18, 24))
    text((x + 8, y + 8), "AI SELL-OFF", F(SANS_B, 15), (255, 255, 255))
    text((x + 8, y + 28), "ASIA, FRIDAY'S CLOSE", F(SANS_B, 9), (240, 120, 110))
    pts = [(0.05, 0.55), (0.25, 0.62), (0.45, 0.58), (0.65, 0.72), (0.85, 0.8), (0.97, 0.86)]
    xy = [(x + w * a, y + h * b) for a, b in pts]
    for i in range(len(xy) - 1):
        line(xy[i][0], xy[i][1], xy[i + 1][0], xy[i + 1][1], (235, 70, 60), 3)
    for (lx, lab, val) in ((0.10, "TAIPEI", "-6.2%"), (0.45, "SEOUL", "-5.2%"), (0.78, "TOKYO", "-4.8%")):
        text((x + w * lx, y + h - 30), lab, F(SANS, 8), (200, 200, 200))
        text((x + w * lx, y + h - 18), val, F(SANS_B, 10), (240, 120, 110))

leads = [
    (ill_kyiv, "1  KYIV, UKRAINE · WAR", "CLAIM · KYIV",
     "Russian missiles hit three Kyiv bridges",
     "About 110 missiles and 400 drones hit overnight, killing at least nine "
     "and cutting power and water in Kyiv.", "(Reuters, AP)"),
    (ill_cyclone, "2  ODISHA, INDIA · CYCLONE", "CONFIRMED · IMD",
     "Cyclone Akvan comes ashore in eastern India",
     "The storm came ashore near Gopalpur after 300,000+ people moved to "
     "shelters. No deaths were reported.", "(IMD, PTI)"),
    (ill_markets, "3  ASIA · MARKETS", "CONFIRMED · EXCHANGES",
     "AI sell-off sinks Asia's stock markets",
     "Taiwan fell 6.2%, its worst week since 1991. Seoul lost about 5% and "
     "Tokyo 4.8% as chipmakers led the slide.", "(Reuters, Morningstar)"),
]
cw = (1024 - 2 * MX - 16) / 3
for i, (ill, kicker, tag, head, body, src) in enumerate(leads):
    x = MX + i * (cw + 8)
    ill(x, 274, cw, 104)
    text((x, 384), kicker, F(SANS_B, 9), RED)
    text((x + cw, 384), tag, F(SANS, 8), GREY, anchor="ra")
    yy = 398
    for ln in wrap(head, F(SERIF_B, 16.5), cw):
        text((x, yy), ln, F(SERIF_B, 16.5), INK); yy += 20
    yy += 2
    for ln in wrap(body, F(SANS, 9.5), cw):
        text((x, yy), ln, F(SANS, 9.5), INK); yy += 12
    text((x, yy + 1), src, F(SANS, 8.5), GREY)
line(MX, 512, 1024 - MX, 512, INK, 1)

# ---------- small story cards ----------
def icon(x, y, kind, col):
    cx, cy = x + 16, y + 16
    if kind == "globe":
        d.ellipse([(cx - 13) * S, (cy - 13) * S, (cx + 13) * S, (cy + 13) * S], outline=col, width=int(2 * S))
        line(cx - 13, cy, cx + 13, cy, col, 1)
        d.arc([(cx - 6) * S, (cy - 13) * S, (cx + 6) * S, (cy + 13) * S], 0, 360, fill=col, width=int(1 * S))
    elif kind == "flag":
        line(cx - 10, cy - 13, cx - 10, cy + 13, col, 2)
        d.polygon([((cx - 10) * S, (cy - 13) * S), ((cx + 12) * S, (cy - 8) * S), ((cx - 10) * S, (cy - 2) * S)], fill=col)
    elif kind == "missile":
        line(cx - 12, cy + 10, cx + 8, cy - 10, col, 3)
        d.polygon([((cx + 8) * S, (cy - 14) * S), ((cx + 14) * S, (cy - 4) * S), ((cx + 4) * S, (cy - 4) * S)], fill=col)
        line(cx - 12, cy + 10, cx - 6, cy + 4, (250, 180, 60), 2)
    elif kind == "shield":
        d.polygon([((cx) * S, (cy - 13) * S), ((cx + 11) * S, (cy - 8) * S), ((cx + 9) * S, (cy + 6) * S),
                   ((cx) * S, (cy + 13) * S), ((cx - 9) * S, (cy + 6) * S), ((cx - 11) * S, (cy - 8) * S)], outline=col, width=int(2 * S))
    elif kind == "banner":
        rect(cx - 13, cy - 12, cx + 13, cy - 4, fill=col)
        line(cx - 9, cy - 4, cx - 9, cy + 12, col, 2)
        line(cx + 9, cy - 4, cx + 9, cy + 12, col, 2)
    elif kind == "chip":
        rect(cx - 9, cy - 9, cx + 9, cy + 9, outline=col, width=2)
        rect(cx - 4, cy - 4, cx + 4, cy + 4, fill=col)
        for dx in (-6, 0, 6):
            line(cx + dx, cy - 13, cx + dx, cy - 9, col, 2)
            line(cx + dx, cy + 9, cx + dx, cy + 13, col, 2)
    elif kind == "scales":
        line(cx, cy - 12, cx, cy + 8, col, 2)
        line(cx - 12, cy - 9, cx + 12, cy - 9, col, 2)
        line(cx - 12, cy - 9, cx - 16, cy + 2, col, 1); line(cx - 12, cy - 9, cx - 8, cy + 2, col, 1)
        line(cx + 12, cy - 9, cx + 8, cy + 2, col, 1); line(cx + 12, cy - 9, cx + 16, cy + 2, col, 1)
        line(cx - 8, cy + 11, cx + 8, cy + 11, col, 2)
    elif kind == "derrick":
        line(cx - 10, cy + 13, cx, cy - 13, col, 2); line(cx + 10, cy + 13, cx, cy - 13, col, 2)
        line(cx - 6, cy + 2, cx + 6, cy + 2, col, 1); line(cx - 8, cy + 8, cx + 8, cy + 8, col, 1)
    elif kind == "bars":
        for i, hh in enumerate((8, 13, 18)):
            rect(cx - 12 + i * 9, cy + 12 - hh, cx - 6 + i * 9, cy + 12, fill=col)
    elif kind == "bat":
        line(cx - 11, cy + 11, cx + 6, cy - 6, col, 4)
        d.ellipse([(cx + 6) * S, (cy + 4) * S, (cx + 13) * S, (cy + 11) * S], fill=col)

cards = [
    ("globe", TEAL, "4", "ANTALYA", "CLIMATE", "COP31 reaches its last day with no deal",
     "Draft drops fossil fuels; talks run into overtime.", "(AP, UN News) CONFIRMED · UN"),
    ("flag", (37, 99, 235), "5", "BRUSSELS", "DIPLOMACY", "UK and EU seal a \"reset\" deal",
     "Food, visas, carbon: 100,000 youth visas a year.", "(Reuters) CONFIRMED · REUTERS"),
    ("missile", RED, "6", "EASTERN POLAND", "SECURITY", "Russian cruise missile lands in Poland",
     "Kh-101 fell in a field; NATO calls it a violation.", "(AP, Reuters) CONFIRMED · WARSAW"),
    ("shield", (124, 58, 237), "7", "CENTRAL IRAQ", "SECURITY", "Iraqi army enters a militia stronghold",
     "Troops move into Jurf al-Sakhar by deal with militia.", "(Reuters) CONFIRMED · REUTERS"),
    ("banner", (190, 24, 93), "8", "ITALY", "LABOUR", "General strike over Italy's budget",
     "Marches in 100+ cities over the budget.", "(Reuters, CGIL) CLAIM · CGIL"),
    ("chip", (21, 128, 61), "9", "US", "TECH", "Nvidia sinks 14% on SEC probe report",
     "SEC said to examine its accounting.", "(Reuters) REPORTED · REUTERS"),
    ("scales", GOLD, "10", "SEOUL", "POLITICS", "Korea's ruling party to impeach top judge",
     "Follows martial-law verdict reversal.", "(Yonhap) CONFIRMED · YONHAP"),
    ("derrick", (217, 119, 6), "11", "TURKANA, KENYA", "ENERGY", "Kenya starts drilling its first oil well",
     "First crude due 1 Dec; 20,000 barrels a day.", "(allAfrica) CONFIRMED · GOVT"),
    ("bars", (8, 145, 178), "12", "TOKYO", "ECONOMY", "Japan's inflation picks up to 2.3%",
     "December rate rise stays in view.", "(Statistics Bureau) CONFIRMED · DATA"),
    ("bat", (75, 85, 99), "13", "WELLINGTON", "CRICKET", "Phillips hits 118 against India",
     "First in all formats vs India in a year.", "(ICC) CONFIRMED · ICC"),
]
sw = (1024 - 2 * MX - 4 * 8) / 5
for i, (kind, col, num, place, beat, head, body, src) in enumerate(cards):
    x = MX + (i % 5) * (sw + 8)
    y = 520 + (i // 5) * 100
    rect(x, y, x + sw, y + 34, fill=(238, 233, 216))
    icon(x + 4, y + 1, kind, col)
    text((x + 38, y + 5), f"{num} · {place}", F(SANS_B, 8), col)
    text((x + 38, y + 18), beat, F(SANS, 7.5), GREY)
    yy = y + 40
    for ln in wrap(head, F(SERIF_B, 10), sw)[:2]:
        text((x, yy), ln, F(SERIF_B, 10), INK); yy += 12.5
    for ln in wrap(body, F(SANS, 7.8), sw)[:2]:
        text((x, yy), ln, F(SANS, 7.8), INK); yy += 10
    text((x, y + 90), src, F(SANS, 6.8), GREY)
line(MX, 724, 1024 - MX, 724, INK, 1)

# ---------- world map + more stories ----------
text((MX, 732), "WHERE IT HAPPENED", F(SANS_B, 10), RED)
MX0, MY0, MW, MH = MX, 750, 330, 148
rect(MX0, MY0, MX0 + MW, MY0 + MH, fill=(240, 235, 220), outline=LIGHT, width=1)
LAND = (196, 178, 140)
# simplified continents (x,y fractions of map box)
continents = [
    [(0.03, 0.30), (0.10, 0.16), (0.22, 0.12), (0.27, 0.24), (0.24, 0.40), (0.17, 0.44), (0.12, 0.52), (0.07, 0.44), (0.03, 0.38)],  # N America
    [(0.16, 0.56), (0.23, 0.54), (0.27, 0.66), (0.23, 0.86), (0.19, 0.90), (0.17, 0.72)],                                          # S America
    [(0.46, 0.18), (0.55, 0.14), (0.58, 0.26), (0.54, 0.34), (0.48, 0.32), (0.45, 0.26)],                                          # Europe
    [(0.47, 0.38), (0.56, 0.36), (0.60, 0.50), (0.56, 0.70), (0.51, 0.72), (0.47, 0.55)],                                          # Africa
    [(0.58, 0.16), (0.78, 0.12), (0.90, 0.22), (0.88, 0.38), (0.78, 0.48), (0.70, 0.58), (0.66, 0.44), (0.60, 0.30)],              # Asia
    [(0.80, 0.62), (0.90, 0.60), (0.93, 0.72), (0.85, 0.78), (0.80, 0.72)],                                                        # Oceania
]
for poly in continents:
    d.polygon([((MX0 + MW * a) * S, (MY0 + MH * b) * S) for a, b in poly], fill=LAND)
pins = {1: (0.565, 0.26), 2: (0.72, 0.44), 3: (0.85, 0.34), 4: (0.605, 0.32),
        5: (0.49, 0.215), 6: (0.56, 0.21), 7: (0.635, 0.375), 8: (0.495, 0.305),
        9: (0.10, 0.34), 10: (0.84, 0.35), 11: (0.545, 0.52), 12: (0.905, 0.29),
        13: (0.955, 0.80)}
for n, (a, b) in pins.items():
    cx, cy = MX0 + MW * a, MY0 + MH * b
    d.ellipse([(cx - 6) * S, (cy - 6) * S, (cx + 6) * S, (cy + 6) * S], fill=RED)
    text((cx, cy - 4), str(n), F(SANS_B, 6.5), (255, 255, 255), anchor="ma")
text((MX, MY0 + MH + 6), "Pins 1-13: the lead and feature stories. Each number matches its story.",
     F(SANS, 7.5), GREY)

LX = MX + MW + 18
text((LX, 732), "ALSO ON FRIDAY 20 NOVEMBER — 22 MORE STORIES", F(SANS_B, 10), RED)
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
    y = 750 + (i % 11) * 15.5
    num, rest = s.split(" ", 1)
    text((x, y), num, F(SANS_B, 8.5), RED)
    text((x + 20, y), rest, F(SANS, 8.5), INK)

# ---------- date check ----------
DY = 920
rect(MX, DY, 1024 - MX, DY + 62, outline=RED, width=1.5)
text((MX + 10, DY + 7), "DATE CHECK", F(SANS_B, 10), RED)
check = ("Left out on purpose — Thursday 19 Nov news: ICJ Myanmar verdict; Shenzhen Trump-Xi-Putin summit; "
         "Anthropic $83 IPO debut; GTA VI launch; Bukele's third-term filing; Fiona the hippo's death; "
         "Senegal migrant boat; Tonga's drought emergency. Wed 18 Nov: $190.4m Van Gogh sale; Rio Tinto's "
         "Panguna pledge. Not yet happened, so not shown: BepiColombo's Mercury orbit capture (Sat 21 Nov), "
         "any final COP31 text (due Sat morning), the ATP Finals final (Sun 22 Nov), and Estonia's border "
         "closure (1 Dec).")
yy = DY + 22
for ln in wrap(check, F(SANS, 8.5), 1024 - 2 * MX - 20):
    text((MX + 10, yy), ln, F(SANS, 8.5), INK); yy += 11

text((512, 990),
     "Every story here happened, or was first reported, on Friday 20 November 2026. "
     "CLAIM = one side's account, not independently confirmed.",
     F(SANS, 8.5), INK, anchor="ma")
text((512, 1004),
     "Sources: AP, Reuters, AFP, Al Jazeera, Yonhap, IMD, BBC, ICC, EORTC, JPMorgan, PTI, UKMTO, AAP, NWS · Original drawings",
     F(SANS, 8.5), GREY, anchor="ma")

out = img.resize((1024, 1024), Image.LANCZOS)
out = out.quantize(colors=256, method=Image.MEDIANCUT)
out.save("entry.png", optimize=True)
print("wrote entry.png", out.size)

"""Target brand generator.
Draws the chunky 'target' letters as geometry (no fonts), writes every logo concept to logos/,
a self-contained library page (index.html), and the UI takes page (../ui/components.html).
Run:  python gen.py
Rules: no concentric rings, no bullseye, no red (Target Corp's trade dress). See /DESIGN.md.
"""
import base64, json, pathlib

HERE = pathlib.Path(__file__).parent
LOGOS = HERE / "logos"
UI = HERE.parent / "ui"
from letters import *  # colors, rr(), letters, word(), WM_W, WM_VB

# ---------------------------------------------------------------- marks
def brackets(x, y, s, color, w=14, inset=12, arm=26):
    a, b = inset, 100 - inset
    d = (f"M{a} {a+arm} V{a} H{a+arm} M{b-arm} {a} H{b} V{a+arm} "
         f"M{b} {b-arm} V{b} H{b-arm} M{a+arm} {b} H{a} V{b-arm}")
    return f'<path transform="translate({x} {y}) scale({s})" d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linejoin="miter" stroke-linecap="butt"/>'

def crosshair(x, y, s, color, dot=None, t=14):
    h = t / 2
    bars = (f'<rect x="{50-h}" y="6" width="{t}" height="30" rx="3"/><rect x="{50-h}" y="64" width="{t}" height="30" rx="3"/>'
            f'<rect x="6" y="{50-h}" width="30" height="{t}" rx="3"/><rect x="64" y="{50-h}" width="30" height="{t}" rx="3"/>')
    d = f'<rect x="43" y="43" width="14" height="14" rx="2" fill="{dot}"/>' if dot else ""
    return f'<g transform="translate({x} {y}) scale({s})" fill="{color}">{bars}{d}</g>'

def svg(vb, body, note):
    x, y, w, h = vb
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}" width="{round(w*2)}" height="{round(h*2)}">\n'
            f'  <!-- {note} -->\n  {body}\n</svg>\n')

items = []
def add(fam, slug, name, note, vb, body, wide=False, keep=False):
    f = f"{len(items)+1:02d}-{slug}.svg"
    items.append((fam, f, name, note, svg(vb, body, note), wide, keep))

def badge(bg, fg, pad=22, rx=18, text="target"):
    g, w = word(text, fg, pad, pad - 4)
    W, H = w + pad * 2, 126 + pad * 2
    return (0, 0, W, H), f'<rect width="{W}" height="{H}" rx="{rx}" fill="{bg}"/>{g}'

# ---------------------------------------------------------------- 0. targets (founder's direction, 2026-11-21)
# Concentric shapes drawn as one even-odd path: fill, hole, fill, hole...
# Rounded squares on purpose: they share the bowl shape of a, g and e, so a later morph can turn rings into letters.
def rings(sizes, cx=50, cy=50, kind="rr", rfrac=.37):
    d = []
    for s in sizes:
        h = s / 2
        if kind == "circle":
            d.append(f"M{cx-h} {cy} A{h} {h} 0 1 0 {cx+h} {cy} A{h} {h} 0 1 0 {cx-h} {cy} Z")
        else:
            d.append(rr(cx - h, cy - h, s, s, max(1.5, s * rfrac)))
    return " ".join(d)

def tgt(sizes, fill=INK, kind="rr", rfrac=.37, cx=50, cy=50, extra=""):
    return f'<path fill-rule="evenodd" fill="{fill}" d="{rings(sizes, cx, cy, kind, rfrac)}" {extra}/>'

F = "Targets"
SQ = (0, 0, 100, 100)
add(F, "target-squircle", "Squircle target", "Ring and center in rounded squares: the same shape as the bowls of a, g and e.", SQ, tgt([92, 64, 38]))
add(F, "target-bands", "Three bands", "More rings, thinner: reads most like a target, still square-ish.", SQ, tgt([94, 76, 58, 40, 22]))
add(F, "target-ultra", "Ultra thick", "Fat rings, thin gaps. The heaviest version, closest to the wordmark's weight.", SQ, tgt([96, 72, 60, 36, 24]))
add(F, "target-square", "Hard square", "Nearly sharp corners. Severe, architectural.", SQ, tgt([92, 64, 38], rfrac=.06))
add(F, "target-round", "Round target", "Classic circles in black. Closest to Target Corp's bullseye: the riskiest one legally.", SQ, tgt([92, 64, 38], kind="circle"))
add(F, "target-point", "Ring + point", "One thick ring and an accent point in the middle: aim, lit.", SQ, tgt([92, 56]) + f'<rect x="41" y="41" width="18" height="18" rx="4" fill="{ACCENT}"/>')
add(F, "target-offcenter", "Off-center hit", "The point sits off center, where you actually aimed.", SQ, tgt([92, 62]) + f'<rect x="54" y="30" width="18" height="18" rx="4" fill="{INK}"/>')
add(F, "target-sight", "Sight cuts", "The target cut by a crosshair: rings plus aim in one mark.", SQ,
    f'<mask id="tx"><rect width="100" height="100" fill="white"/><rect x="46" y="0" width="8" height="100" fill="black"/><rect x="0" y="46" width="100" height="8" fill="black"/></mask>'
    + tgt([94, 70, 46], extra='mask="url(#tx)"'))
add(F, "target-locked", "Locked target", "A small target inside the focus brackets: both brand ideas.", SQ, brackets(0, 0, 1, INK, 10) + tgt([46, 30, 14]))
add(F, "target-t", "t in the middle", "The bullseye is the t from the wordmark.", SQ, tgt([94, 66]) + L_t(INK)[1].replace("<path", '<path transform="translate(38 23) scale(.46)"'))
add(F, "target-diamond", "Diamond", "The squircle target turned 45°. Reads like a sign.", SQ, f'<g transform="rotate(45 50 50) translate(14 14) scale(.72)">{tgt([92, 64, 38])}</g>')
add(F, "target-line", "Line target", "Outlined rings for small UI spots.", SQ,
    f'<path fill="none" stroke="{INK}" stroke-width="6" d="{rings([88, 58, 28])}"/>')
add(F, "target-arrow", "Hit", "An arrow in the center ring. Literal, but instantly readable.", SQ,
    tgt([92, 64, 38]) + f'<path d="M50 50 L86 14" stroke="{PAPER}" stroke-width="12" stroke-linecap="butt"/><path d="M50 50 L86 14" stroke="{INK}" stroke-width="6"/><path d="M76 10 H90 V24" fill="none" stroke="{INK}" stroke-width="6"/>')
add(F, "target-tile", "Target tile", "App icon: white squircle target on black.", SQ,
    f'<rect width="100" height="100" rx="22" fill="{INK}"/>' + tgt([70, 48, 28], PAPER))
add(F, "target-tile-accent", "Accent tile", "Black target on the accent.", SQ,
    f'<rect width="100" height="100" rx="22" fill="{ACCENT}"/>' + tgt([70, 48, 28], INK), keep=True)
g, w = word("target", INK, 150, 4)
add(F, "target-lockup", "Target + word", "The mark leading the wordmark. The ring height matches the word.", (0, 0, w + 156, 134),
    tgt([128, 90, 52], cx=64, cy=67) + g, True)
add(F, "target-material", "As material", "A giant target cropped by the screen edge, mini-style.", (0, 0, 400, 220),
    f'<rect width="400" height="220" rx="24" fill="{INK}"/><clipPath id="tm"><rect width="400" height="220" rx="24"/></clipPath>'
    f'<g clip-path="url(#tm)">{tgt([420, 320, 220, 120], PAPER, cx=330, cy=150)}</g>', True)
# the a in the wordmark already is a target: add a point in its counter
gw, w = word("target")
add(F, "target-in-word", "The a is a target", "The wordmark with an accent point in the a's counter. The bridge for the morph.", WM_VB,
    gw + f'<rect x="{58+29}" y="57" width="12" height="12" rx="2" fill="{ACCENT}"/>', True)

# ---------------------------------------------------------------- A. wordmarks
F = "Wordmarks"
g, w = word("target"); add(F, "wordmark", "target", "The wordmark. Squarish bowls, heavy stems, starts and ends on a t.", WM_VB, g, True)
g, w = word("target"); add(F, "wordmark-dot", "target.", "A square full stop in the accent. The one place the color lives.", (-2, 0, w + 40, 134), g + f'<rect x="{w+8}" y="76" width="24" height="24" fill="{ACCENT}"/>', True)
g, w = word("target", INK, 40, 20)
add(F, "wordmark-locked", "Locked on", "Focus brackets snapped around the word: the brand idea in one picture.", (0, 0, w + 80, 174),
    g + f'<path d="M6 46 V6 H46 M{w+34} 6 H{w+74} V46 M{w+74} 128 V168 H{w+34} M46 168 H6 V128" fill="none" stroke="{INK}" stroke-width="10"/>', True)
g1, w1 = word("tar", INK, 0, 0); g2, w2 = word("get", INK, 0, 108)
add(F, "wordmark-stacked", "Stacked", "tar / get on two lines: a square block that fits an app icon.", (-2, 0, max(w1, w2) + 4, 242), g1 + g2)
g, w = word("target", INK, 0, 0)
add(F, "wordmark-underline", "On the line", "The word sitting on a heavy rule, like a selected tab.", (-2, 0, w + 4, 160), g + f'<rect x="0" y="146" width="{w}" height="12" fill="{INK}"/>', True)

# ---------------------------------------------------------------- B. thick badges
F = "Thick badges"
vb, b = badge(INK, PAPER); add(F, "badge-black", "Black badge", "The mark as a solid block. Drops into UI as a label.", vb, b, True)
vb, b = badge(PAPER, INK); add(F, "badge-white", "White badge", "Same block in white, for dark UI.", (vb[0]-20, vb[1]-20, vb[2]+40, vb[3]+40), f'<rect x="-20" y="-20" width="{vb[2]+40}" height="{vb[3]+40}" fill="{INK}"/>' + b, True, keep=True)
vb, b = badge(ACCENT, INK); add(F, "badge-accent", "Accent badge", "The badge in the one brand color.", vb, b, True, keep=True)
vb, b = badge(INK, PAPER, pad=12, rx=10); add(F, "badge-tight", "Tight badge", "Minimum padding. Most mini-like.", vb, b, True)
g1, _ = word("tar", PAPER, 30, 26); g2, _ = word("get", PAPER, 30, 134)
add(F, "badge-stacked", "Stacked block", "tar / get in a square block.", (0, 0, 270, 300), f'<rect width="270" height="300" rx="34" fill="{INK}"/>' + g1 + g2)
g, _ = word("target", INK, 0, 0, .25)
add(F, "badge-in-use", "In use", "The badge as the space switcher inside a dark dropdown, the way mini uses its mark.", (0, 0, 460, 120),
    f'<rect width="460" height="120" fill="#2350FF"/><rect x="20" y="16" width="420" height="88" rx="18" fill="{INK}"/>'
    f'<rect x="40" y="34" width="134" height="52" rx="10" fill="{PAPER}"/>' + word("target", INK, 52, 43, .27)[0] +
    f'<text x="192" y="73" font-family="system-ui, sans-serif" font-size="34" fill="#eee">Work</text><path d="M388 54 H408 L398 66 Z" fill="#eee"/>', True, keep=True)

# ---------------------------------------------------------------- C. marks
F = "Marks"
add(F, "brackets", "Brackets", "Focus brackets: four heavy corners around nothing. You fill the middle.", (0, 0, 100, 100), brackets(0, 0, 1, INK))
add(F, "brackets-dot", "Brackets + point", "Brackets locked on a single square point in the accent.", (0, 0, 100, 100), brackets(0, 0, 1, INK) + f'<rect x="40" y="40" width="20" height="20" fill="{ACCENT}"/>')
add(F, "brackets-t", "Brackets + t", "The t from the wordmark, locked on.", (0, 0, 100, 100), brackets(0, 0, 1, INK) + L_t(INK)[1].replace("<path", '<path transform="translate(39 28) scale(.44)"'))
add(F, "crosshair", "Crosshair", "Four heavy bars, open center. Aim without a bullseye.", (0, 0, 100, 100), crosshair(0, 0, 1, INK))
add(F, "crosshair-dot", "Crosshair + point", "The crosshair with an accent point in the gap.", (0, 0, 100, 100), crosshair(0, 0, 1, INK, ACCENT))
add(F, "crosshair-thick", "Fat crosshair", "Bars at maximum weight: almost a plus, the gap keeps it a sight.", (0, 0, 100, 100), crosshair(0, 0, 1, INK, None, 22))
add(F, "t-t", "t…t", "target starts and ends on a t. The two t's face each other like brackets.", (0, 0, 130, 110),
    L_t(INK)[1].replace("<path", '<path transform="translate(8 2)"') + L_t(INK)[1].replace("<path", '<path transform="translate(122 2) scale(-1 1)"'))
add(F, "aim-block", "Aim block", "A black block with one square point cut out, off-center: the spot you're aiming at.", (0, 0, 100, 100),
    f'<mask id="ab"><rect width="100" height="100" fill="white"/><rect x="56" y="26" width="18" height="18" fill="black"/></mask><rect width="100" height="100" rx="20" fill="{INK}" mask="url(#ab)"/>')
add(F, "g-mark", "The g", "The g alone: the only letter with a tail below the line.", (0, 0, 100, 140), L_g(INK)[1].replace("<path", '<path transform="translate(13 0)"', 2))

# ---------------------------------------------------------------- D. app icons
F = "App icons"
TILE = '<clipPath id="tc"><rect width="100" height="100" rx="22"/></clipPath>'
add(F, "icon-crosshair", "Crosshair tile", "White crosshair, accent point, black tile.", (0, 0, 100, 100), f'{TILE}<rect width="100" height="100" rx="22" fill="{INK}"/>' + crosshair(18, 18, .64, PAPER, ACCENT))
add(F, "icon-brackets", "Bracket tile", "White brackets around a white t.", (0, 0, 100, 100), f'<rect width="100" height="100" rx="22" fill="{INK}"/>' + brackets(14, 14, .72, PAPER, 15) + L_t(PAPER)[1].replace("<path", '<path transform="translate(38 30) scale(.42)"'))
g1, _ = word("tar", PAPER, 16, 12, .3); g2, _ = word("get", PAPER, 16, 46, .3)
add(F, "icon-stacked", "Stacked tile", "tar / get filling the tile.", (0, 0, 100, 100), f'<rect width="100" height="100" rx="22" fill="{INK}"/>' + g1 + g2)
g, _ = word("target", PAPER, 12, 40, .42)
add(F, "icon-cropped", "Cropped tile", "The wordmark too big for the tile, cut by its edge.", (0, 0, 100, 100), f'{TILE}<g clip-path="url(#tc)"><rect width="100" height="100" fill="{INK}"/>{g}</g>')
add(F, "icon-accent", "Accent tile", "Black crosshair on the accent.", (0, 0, 100, 100), f'<rect width="100" height="100" rx="22" fill="{ACCENT}"/>' + crosshair(18, 18, .64, INK), keep=True)

# ---------------------------------------------------------------- E. lockups
F = "Lockups"
g, w = word("target", INK, 140, 0)
add(F, "lockup-crosshair", "Crosshair + word", "Mark and wordmark side by side.", (0, -10, w + 150, 150), crosshair(0, 10, 1.1, INK) + g, True)
g, w = word("target", INK, 134, 0)
add(F, "lockup-brackets", "Brackets + word", "Bracket mark leading the word.", (0, -10, w + 144, 150), brackets(0, 10, 1.1, INK) + f'<rect x="44" y="54" width="22" height="22" fill="{INK}"/>' + g, True)

# ---------------------------------------------------------------- write logos + library
LOGOS.mkdir(exist_ok=True)
for old in LOGOS.glob("*.svg"):
    old.unlink()
for fam, f, name, note, text, wide, keep in items:
    (LOGOS / f).write_text(text, encoding="utf-8")
def b64(t): return "data:image/svg+xml;base64," + base64.b64encode(t.encode()).decode()
def to_dark(t): return t.replace(INK, "#__ink").replace(PAPER, INK).replace("#__ink", PAPER)
data = {f: [b64(text), b64(text if keep else to_dark(text))] for _, f, _, _, text, _, keep in items}
fams = []
for fam, f, name, note, _, wide, keep in items:
    if not fams or fams[-1][0] != fam:
        fams.append([fam, []])
    fams[-1][1].append([f, name, note, wide, keep])
page = (HERE / "library-template.html").read_text(encoding="utf-8")
page = page.replace("__SVG__", json.dumps(data)).replace("__FAMS__", json.dumps(fams)).replace("__COUNT__", str(len(items)))
(HERE / "index.html").write_text(page, encoding="utf-8")
print(len(items), "logos ->", LOGOS)

# ---------------------------------------------------------------- UI takes
tpl = UI / "components-template.html"
if tpl.exists():
    vb = " ".join(str(v) for v in WM_VB)
    html = tpl.read_text(encoding="utf-8")
    html = html.replace("__WM__", word("target", "currentColor")[0]).replace("__WMVB__", vb)
    html = html.replace("__CROSS__", crosshair(0, 0, 1, "currentColor")).replace("__BRK__", brackets(0, 0, 1, "currentColor"))
    (UI / "components.html").write_text(html, encoding="utf-8")
    print("ui/components.html written")

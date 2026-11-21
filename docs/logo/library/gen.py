"""Tab logo library generator.
Writes every concept as its own SVG in this folder, plus index.html (self-contained preview).
Run:  python gen.py
All letters are drawn here as geometry (no fonts), from the same t, bowl and stem.
"""
import base64, json, pathlib

OUT = pathlib.Path(__file__).parent
INK, PAPER, ACCENT, GRAY, GRAY2 = "#111", "#fff", "#FFD500", "#9a9a96", "#4a4a48"

# ---------- primitives ----------
# The t: 50 wide, top at y=6, crossbar 26..44, baseline 100, tail always visible.
T = "M10 6 H30 V26 H46 V44 H30 V72 Q30 82 42 82 H50 V100 H40 Q10 100 10 72 V44 H0 V26 H10 Z"

def ring(cx, cy=63, R=37, r=16, solid=False):
    outer = f"M{cx-R} {cy} A{R} {R} 0 1 0 {cx+R} {cy} A{R} {R} 0 1 0 {cx-R} {cy} Z"
    if solid:
        return outer
    return outer + f" M{cx-r} {cy} A{r} {r} 0 1 0 {cx+r} {cy} A{r} {r} 0 1 0 {cx-r} {cy} Z"

def wordmark(fill=INK, solid_bowls=False, stroke=None, heavy=0):
    """'tab': 215 wide, 0..100 tall. heavy=N fattens every stroke by N units (counters shrink)."""
    paint = f'fill="none" stroke="{stroke}" stroke-width="4" stroke-linejoin="round"' if stroke else f'fill="{fill}"'
    if heavy:
        paint += f' stroke="{fill}" stroke-width="{heavy}" stroke-linejoin="miter"'
    # extra weight needs extra spacing, or the letters glue together
    da, db = heavy * 0.9, heavy * 1.8
    return (f'<g {paint}><path d="{T}"/>'
            f'<g transform="translate({da} 0)"><path fill-rule="evenodd" d="{ring(93, solid=solid_bowls)}"/>'
            f'<rect x="110" y="26" width="20" height="74"/></g>'
            f'<g transform="translate({db} 0)"><rect x="138" y="0" width="20" height="100"/>'
            f'<path fill-rule="evenodd" d="{ring(178, solid=solid_bowls)}"/></g></g>')

def wm_width(heavy=0):
    return 215 + heavy * 1.8

def t(x, y, s, fill=INK, extra=""):
    return f'<path transform="translate({x} {y}) scale({s})" d="{T}" fill="{fill}" {extra}/>'

def arrow_key(x, y, s, color, w=11):
    """The Tab key symbol, in a 100 box (shaft, head, wall)."""
    return (f'<g transform="translate({x} {y}) scale({s})" stroke="{color}" stroke-width="{w}" fill="none" stroke-linejoin="miter">'
            f'<path d="M18 50 H64"/><path d="M50 33 L67 50 L50 67"/><path d="M80 30 V70"/></g>')

WIDE_TAB = "M14 84 A10 10 0 0 0 24 74 V40 A18 18 0 0 1 42 22 H198 A18 18 0 0 1 216 40 V74 A10 10 0 0 0 226 84 Z"

def svg(vb, body, note):
    x, y, w, h = vb
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}" width="{w*2}" height="{h*2}">\n'
            f'  <!-- {note} -->\n  {body}\n</svg>\n')

SQ = (0, 0, 100, 100)
items = []  # (family, file, name, note, svg_text, wide, keep_colors)

def add(family, slug, name, note, vb, body, wide=False, keep=False):
    n = len(items) + 1
    f = f"{n:02d}-{slug}.svg"
    items.append((family, f, name, note, svg(vb, body, note), wide, keep))

# ---------- 0. thick badges: the logo as a solid block, usable inside UI (like mini's chip) ----------
F = "Thick badges"
def badge(fill_bg, fill_fg, heavy, pad=18, rx=16):
    w, h = wm_width(heavy) + heavy + pad * 2, 100 + heavy + pad * 2
    return (w, h, f'<rect width="{w}" height="{h}" rx="{rx}" fill="{fill_bg}"/>'
                  f'<g transform="translate({pad + heavy/2} {pad + heavy/2})">{wordmark(fill_fg, heavy=heavy)}</g>')
w, h, b = badge(PAPER, INK, 10); add(F, "badge-white", "White badge", "Extra-heavy wordmark in a white block. Drops into any dark control as a label.", (-24, -24, w + 48, h + 48), f'<rect x="-24" y="-24" width="{w+48}" height="{h+48}" fill="{INK}"/>' + b, True, keep=True)
w, h, b = badge(INK, PAPER, 10); add(F, "badge-black", "Black badge", "The same block in black, for light UI.", (0, 0, w, h), b, True)
w, h, b = badge(INK, PAPER, 18, pad=14, rx=12); add(F, "badge-ultra", "Ultra badge", "Fattened until the counters almost close. Maximum weight, tightest padding.", (0, 0, w, h), b, True)
w, h, b = badge(ACCENT, INK, 10); add(F, "badge-accent", "Accent badge", "The badge in the one brand color.", (0, 0, w, h), b, True, keep=True)
add(F, "badge-t", "t block", "The square version: heavy t in a block, for spots too small for the word.", (0, 0, 100, 100),
    f'<rect width="100" height="100" rx="18" fill="{INK}"/><path transform="translate(29 8) scale(.84)" d="{T}" fill="{PAPER}" stroke="{PAPER}" stroke-width="8" stroke-linejoin="miter"/>')
add(F, "badge-in-use", "In use", "The badge as a label inside a dark dropdown, the way mini uses its mark.", (0, 0, 420, 120),
    f'<rect width="420" height="120" fill="#2350FF"/><rect x="20" y="16" width="380" height="88" rx="18" fill="{INK}"/>'
    f'<rect x="42" y="36" width="108" height="48" rx="9" fill="{PAPER}"/><g transform="translate(53 40) scale(.4)">{wordmark(INK, heavy=10)}</g>'
    f'<text x="170" y="73" font-family="system-ui, sans-serif" font-size="34" fill="#eee">Spaces</text>'
    f'<path d="M352 54 H372 L362 66 Z" fill="#eee"/>', True, keep=True)

# ---------- A. wordmarks ----------
F = "Wordmarks"
add(F, "wordmark", "tab", "The base wordmark. Heavy, tight, geometric.", (-10, -10, 235, 120), wordmark(), True)
add(F, "wordmark-period", "tab.", "A full stop: decided, done. The dot is square to match the stems.",
    (-10, -10, 265, 120), wordmark() + f'<rect x="166" y="82" width="0" height="0"/><rect x="226" y="80" width="20" height="20" fill="{INK}"/>', True)
add(F, "wordmark-crossbar", "Crossbar strip", "The t's crossbar runs the full width, like a tab strip at x-height.",
    (-10, -10, 235, 120), wordmark() + f'<rect x="0" y="26" width="215" height="12" fill="{INK}"/>', True)
add(F, "wordmark-key", "tab ⇥", "The wordmark followed by the Tab key symbol, same stroke weight.",
    (-10, -10, 330, 120), wordmark() +
    f'<g stroke="{INK}" stroke-width="20" fill="none" stroke-linejoin="miter"><path d="M228 63 H276"/><path d="M258 39 L282 63 L258 87"/><path d="M302 26 V100"/></g>', True)
add(F, "wordmark-cursor", "tab|", "Being typed: a text cursor after the b.",
    (-10, -10, 265, 120), wordmark() + f'<rect x="232" y="-4" width="8" height="108" fill="{INK}"/>', True)
add(F, "wordmark-outline", "Outline", "The wordmark as a line. For huge sizes and backgrounds only.",
    (-10, -10, 235, 120), wordmark(stroke=INK), True)
add(F, "wordmark-strip", "On the strip", "Wordmark sitting on a heavy strip line that runs past both ends.",
    (-30, -10, 275, 140), wordmark() + f'<rect x="-30" y="112" width="275" height="10" fill="{INK}"/>', True)
add(F, "wordmark-pill", "In a capsule", "Wordmark inside a black capsule, like a selected tab title.",
    (0, 0, 300, 140), f'<rect x="0" y="0" width="300" height="140" rx="70" fill="{INK}"/><g transform="translate(64 22) scale(.8)">{wordmark(PAPER)}</g>', True)
add(F, "wordmark-dots", "Solid bowls", "Bowls filled in: louder, more graphic, less readable.",
    (-10, -10, 235, 120), wordmark(solid_bowls=True), True)

# ---------- B. monograms ----------
F = "Monograms"
add(F, "t-circle", "t in a circle", "The simplest badge. The t sits slightly left of center.", SQ,
    f'<circle cx="50" cy="50" r="46" fill="{INK}"/>' + t(36, 22, .58, PAPER))
add(F, "t-square", "t in a square", "Hard square, no rounding. Most severe.", SQ,
    f'<rect x="4" y="4" width="92" height="92" fill="{INK}"/>' + t(20, 24, .6, PAPER))
add(F, "t-capsule", "t in a wide capsule", "Wide capsule, t at the right end. Reads as a tab title, not a switch.", (0, 0, 160, 100),
    f'<rect x="4" y="18" width="152" height="64" rx="32" fill="{INK}"/>' + t(102, 28, .45, PAPER))
add(F, "t-arrow", "t ⇥", "The crossbar becomes an arrow: the letter t and the Tab key at once.", (0, 0, 100, 100),
    f'<g transform="translate(10 0)"><path d="{T}" fill="{INK}"/><rect x="40" y="26" width="22" height="18" fill="{INK}"/>'
    f'<polygon points="58,12 82,35 58,58" fill="{INK}"/></g>')
add(F, "t-stencil", "Stencil t", "A cut through the stem, like a stencil. Industrial.", SQ,
    f'<mask id="m"><rect width="100" height="100" fill="#fff"/><rect x="0" y="52" width="100" height="5" fill="#000"/></mask>'
    f'<g mask="url(#m)"><path transform="translate(25 -3)" d="{T}" fill="{INK}"/></g>')
add(F, "t-italic", "Leaning t", "Slanted forward: speed, motion.", SQ,
    f'<path transform="translate(30 -3) skewX(-12)" d="{T}" fill="{INK}"/>')
add(F, "t-round", "Rounded t", "Same skeleton, round ends. Friendlier.", SQ,
    f'<g stroke="{INK}" stroke-width="20" stroke-linecap="round" fill="none"><path d="M42 12 V66 Q42 86 62 86 H66"/><path d="M26 36 H62"/></g>')
add(F, "t-outline", "Outline t", "The t as a line. Light, for UI chrome.", SQ,
    f'<path transform="translate(25 -3)" d="{T}" fill="none" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')

# ---------- C. tab key ----------
F = "Tab key"
add(F, "key-arrow", "⇥", "The Tab key symbol alone. Owns the name's second meaning.", SQ, arrow_key(0, 0, 1, INK, 13))
add(F, "key-circle", "⇥ in a circle", "The symbol on a round badge.", SQ,
    f'<circle cx="50" cy="50" r="46" fill="{INK}"/>' + arrow_key(8, 8, .84, PAPER, 13))
add(F, "key-tag", "Tag", "An arrow-shaped tag (a pull-tab, a label) with the t in it.", (0, 0, 120, 100),
    f'<path d="M8 22 H76 Q80 22 83 25 L106 46 Q110 50 106 54 L83 75 Q80 78 76 78 H8 Z" fill="{INK}"/>' + t(24, 26, .48, PAPER))
add(F, "key-arrow-t", "→ t", "An arrow that hits a t instead of a wall.", (0, 0, 130, 100),
    f'<g stroke="{INK}" stroke-width="13" fill="none" stroke-linejoin="miter"><path d="M6 56 H56"/><path d="M40 37 L60 56 L40 75"/></g>' + t(72, 4, .92))

# ---------- D. tab shapes (wide only: no tombstones) ----------
F = "Tab shapes"
add(F, "shape-strip3", "Three tabs", "A strip of three; ours is the black one.", (0, 0, 220, 70),
    f'<path d="M150 62 V36 A12 12 0 0 1 162 24 H204 A12 12 0 0 1 216 36 V62 Z" fill="none" stroke="{INK}" stroke-width="3"/>'
    f'<path d="M80 62 V36 A12 12 0 0 1 92 24 H134 A12 12 0 0 1 146 36 V62 Z" fill="none" stroke="{INK}" stroke-width="3"/>'
    f'<path d="M6 62 V36 A12 12 0 0 1 18 24 H64 A12 12 0 0 1 76 36 V62 Z" fill="{INK}"/>' + t(20, 28, .3, PAPER) +
    f'<rect x="0" y="60" width="220" height="4" fill="{INK}"/>', True)
add(F, "shape-outline", "Outline tab", "The wide tab drawn as one line, strip included.", (0, 0, 240, 100),
    f'<path d="M0 84 H14 A10 10 0 0 0 24 74 V40 A18 18 0 0 1 42 22 H198 A18 18 0 0 1 216 40 V74 A10 10 0 0 0 226 84 H240" fill="none" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>', True)
add(F, "shape-notch", "Negative tab", "A slab with a tab-shaped bite out of its top. The tab is the gap.", (0, 0, 200, 100),
    f'<mask id="m"><rect width="200" height="100" fill="#fff"/><path d="M40 0 V18 A10 10 0 0 0 50 28 H150 A10 10 0 0 0 160 18 V0 Z" fill="#000"/></mask>'
    f'<rect x="0" y="10" width="200" height="80" rx="14" fill="{INK}" mask="url(#m)"/>' + t(28, 40, .4, PAPER), True)
add(F, "shape-minimal", "t + ×", "A wide tab with just the t and the close mark. A tab with nothing in it but us.", (0, 0, 240, 100),
    f'<rect x="0" y="83" width="240" height="3" fill="{INK}"/><path d="{WIDE_TAB}" fill="{INK}"/>' + t(42, 30, .46, PAPER) +
    f'<path d="M186 45 L200 59 M200 45 L186 59" stroke="{PAPER}" stroke-width="5" stroke-linecap="round"/>', True)

# ---------- E. keyboard ----------
F = "Keyboard"
add(F, "keycap", "Keycap", "The Tab key itself: label bottom-left, ⇥ top-right.", (0, 0, 150, 100),
    f'<rect x="4" y="8" width="142" height="86" rx="14" fill="{INK}"/><rect x="12" y="10" width="126" height="68" rx="10" fill="#2b2b2b"/>'
    f'<g transform="translate(24 46) scale(.18)">{wordmark(PAPER)}</g>' + arrow_key(98, 14, .4, PAPER, 9))
add(F, "keycap-line", "Keycap, line", "The key drawn as an outline.", (0, 0, 150, 100),
    f'<rect x="6" y="10" width="138" height="82" rx="14" fill="none" stroke="{INK}" stroke-width="5"/>'
    f'<g transform="translate(24 46) scale(.18)">{wordmark(INK)}</g>' + arrow_key(98, 16, .4, INK, 9))
add(F, "key-square", "⇥ key", "A square key with only the symbol.", SQ,
    f'<rect x="6" y="6" width="88" height="88" rx="16" fill="{INK}"/><rect x="12" y="8" width="76" height="70" rx="11" fill="#2b2b2b"/>' + arrow_key(14, 6, .72, PAPER, 12))

# ---------- F. abstract ----------
F = "Abstract"
add(F, "abs-bars", "Tab list", "Three bars: a list of open tabs, the current one on top.", SQ,
    f'<rect x="10" y="18" width="80" height="18" rx="9" fill="{INK}"/><rect x="10" y="42" width="58" height="18" rx="9" fill="{GRAY}"/><rect x="10" y="66" width="38" height="18" rx="9" fill="{GRAY}"/>')
add(F, "abs-stack", "Stack", "Three tabs stacked; ours in front.", SQ,
    f'<rect x="32" y="12" width="58" height="36" rx="9" fill="{GRAY2}"/><rect x="22" y="30" width="58" height="36" rx="9" fill="{GRAY}"/><rect x="10" y="48" width="58" height="36" rx="9" fill="{INK}"/>')
add(F, "abs-bowl", "The bowl", "The a from the wordmark on its own: a ring and a stem.", SQ,
    f'<g transform="translate(-30 -13)"><path fill-rule="evenodd" d="{ring(93)}" fill="{INK}"/><rect x="110" y="26" width="20" height="74" fill="{INK}"/></g>')
add(F, "abs-corner", "The corner", "Just the rounded top corner of a tab. The least you need to say 'tab'.", SQ,
    f'<path d="M16 90 V44 A28 28 0 0 1 44 16 H90" fill="none" stroke="{INK}" stroke-width="18"/>')
add(F, "abs-grid", "Tab overview", "A 2×2 grid of tabs, one active.", SQ,
    f'<rect x="10" y="10" width="37" height="37" rx="9" fill="{INK}"/><rect x="53" y="10" width="37" height="37" rx="9" fill="{GRAY}"/>'
    f'<rect x="10" y="53" width="37" height="37" rx="9" fill="{GRAY}"/><rect x="53" y="53" width="37" height="37" rx="9" fill="{GRAY}"/>')

# ---------- G. lockups ----------
F = "Lockups"
add(F, "lockup-key", "⇥ + tab", "Icon and wordmark side by side.", (0, 0, 360, 120),
    f'<rect x="0" y="10" width="100" height="100" rx="22" fill="{INK}"/>' + arrow_key(0, 10, 1, PAPER, 11) +
    f'<g transform="translate(130 10)">{wordmark()}</g>', True)
add(F, "lockup-t-arrow", "t⇥ + tab", "The arrow-t monogram leading the wordmark.", (0, 0, 340, 120),
    f'<g transform="translate(0 10)"><path d="{T}" fill="{INK}"/><rect x="40" y="26" width="22" height="18" fill="{INK}"/><polygon points="58,12 82,35 58,58" fill="{INK}"/></g>'
    f'<rect x="102" y="10" width="4" height="100" fill="{GRAY}"/><g transform="translate(124 10)">{wordmark()}</g>', True)
add(F, "lockup-accent", "Accent lockup", "The one place the yellow lives: behind the wordmark.", (0, 0, 300, 140),
    f'<rect width="300" height="140" rx="24" fill="{ACCENT}"/><g transform="translate(42 20)">{wordmark()}</g>', True, keep=True)

# ---------- write ----------
for old in OUT.glob("[0-9][0-9]-*.svg"):
    old.unlink()
for fam, f, name, note, text, wide, keep in items:
    (OUT / f).write_text(text, encoding="utf-8")

data = {f: "data:image/svg+xml;base64," + base64.b64encode(text.encode()).decode() for _, f, _, _, text, _, _ in items}
fams = []
for fam, f, name, note, _, wide, keep in items:
    if not fams or fams[-1][0] != fam:
        fams.append([fam, []])
    fams[-1][1].append([f, name, note, wide, keep])

page = (OUT / "template.html").read_text(encoding="utf-8")
page = page.replace("__SVG__", json.dumps(data)).replace("__FAMS__", json.dumps(fams)).replace("__COUNT__", str(len(items)))
(OUT / "index.html").write_text(page, encoding="utf-8")
print(len(items), "logos written")

# (UI takes moved to docs/brand/gen.py with the Target rebrand.)

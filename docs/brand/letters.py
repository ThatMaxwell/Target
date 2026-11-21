"""Shared geometry for the chunky 'target' wordmark. Used by gen.py (logos) and motion.py (animation)."""

INK, PAPER, ACCENT, GRAY, GRAY2 = "#111", "#fff", "#FFD500", "#9a9a96", "#4a4a48"

# ---------------------------------------------------------------- letters
# x-height 26..100, baseline 100, ascender 4, descender 130. Stroke ~24.
# Bowls are rounded rectangles, not circles: chunkier, less "bubbly".
def rr(x, y, w, h, r):
    return (f"M{x+r} {y} H{x+w-r} A{r} {r} 0 0 1 {x+w} {y+r} V{y+h-r} A{r} {r} 0 0 1 {x+w-r} {y+h} "
            f"H{x+r} A{r} {r} 0 0 1 {x} {y+h-r} V{y+r} A{r} {r} 0 0 1 {x+r} {y} Z")

_mask_n = [0]
def _mid():
    _mask_n[0] += 1
    return f"e{_mask_n[0]}"

def L_t(fill):
    return 52, f'<path fill="{fill}" d="M8 4 H32 V26 H50 V46 H32 V68 Q32 76 40 76 H52 V100 H38 Q8 100 8 70 V46 H0 V26 H8 Z"/>'

def L_a(fill):
    return 74, (f'<path fill="{fill}" fill-rule="evenodd" d="{rr(0,26,70,74,30)} {rr(24,48,22,30,10)}"/>'
                f'<rect fill="{fill}" x="50" y="26" width="24" height="74"/>')

def L_r(fill):
    return 58, f'<path fill="{fill}" d="M0 26 H24 V36 Q30 26 46 26 H58 V50 H46 Q24 50 24 70 V100 H0 Z"/>'

def L_g(fill):
    return 74, (f'<path fill="{fill}" fill-rule="evenodd" d="{rr(0,26,70,70,30)} {rr(24,46,22,28,10)}"/>'
                f'<path fill="{fill}" d="M50 26 H74 V104 Q74 130 46 130 H6 V110 H44 Q50 110 50 104 Z"/>')

def L_e(fill):
    m = _mid()
    return 72, (f'<mask id="{m}" maskUnits="userSpaceOnUse" x="-4" y="20" width="84" height="86">'
                f'<path fill="white" d="{rr(0,26,72,74,30)}"/><path fill="black" d="{rr(22,44,28,12,6)}"/>'
                f'<rect fill="black" x="22" y="72" width="60" height="10"/></mask>'
                f'<rect mask="url(#{m})" fill="{fill}" x="-4" y="20" width="84" height="86"/>')

LETTERS = {"t": L_t, "a": L_a, "r": L_r, "g": L_g, "e": L_e}
GAP = 6

def word(text, fill=INK, x=0, y=0, s=1):
    """Returns (svg_group, width). Height spans y 4..130 at s=1."""
    parts, cx = [], 0
    for ch in text:
        w, g = LETTERS[ch](fill)
        parts.append(f'<g transform="translate({cx} 0)">{g}</g>')
        cx += w + GAP
    width = cx - GAP
    return f'<g transform="translate({x} {y}) scale({s})">{"".join(parts)}</g>', width

WM_W = word("target")[1]           # 412
WM_VB = (-2, 0, WM_W + 4, 134)     # tight box around the wordmark incl. descender

# ---------------------------------------------------------------- digits (for the clock)
# Same system as the letters: stroke ~24, rounded-rect bowls. Cap height 4..100. Tabular cell DW wide.
DW, COLON_W = 66, 22

def _p(d, fill, extra=""):
    return f'<path fill="{fill}" d="{d}"{extra}/>'

def _eo(d, fill, extra=""):
    return f'<path fill="{fill}" fill-rule="evenodd" d="{d}"{extra}/>'

def _d6(fill, extra=""):
    return (_eo(f"{rr(0,38,66,62,30)} {rr(24,60,18,18,9)}", fill, extra)
            + _p("M0 70 V40 Q0 4 36 4 H58 V28 H37 Q24 28 24 41 V70 Z", fill, extra))

DIGITS = {
    "0": lambda f: _eo(f"{rr(0,4,66,96,32)} {rr(24,28,18,48,9)}", f),
    "1": lambda f: _p("M18 4 H55 V100 H31 V28 H18 Z", f),
    "2": lambda f: _p("M0 36 Q0 4 33 4 Q66 4 66 36 Q66 54 50 66 L37 76 H66 V100 H0 V78 L32 54 "
                      "Q42 46 42 37 Q42 28 33 28 Q24 28 24 37 V40 H0 Z", f),
    "3": lambda f: _p("M0 4 H64 V25 L45 44 Q66 50 66 71 Q66 100 33 100 Q0 100 0 74 H24 Q25 78 33 78 "
                      "Q42 78 42 70 Q42 61 31 61 H22 V43 L36 26 H0 Z", f),
    "4": lambda f: _eo("M36 4 H62 V58 H68 V80 H62 V100 H38 V80 H-2 V58 Z M38 58 V43 L27 58 Z", f),
    "5": lambda f: _p("M3 4 H63 V26 H27 V40 Q31 38 37 38 Q66 38 66 69 Q66 100 33 100 Q0 100 0 74 H24 "
                      "Q25 78 33 78 Q42 78 42 69 Q42 60 33 60 Q27 60 25 64 H3 Z", f),
    "6": lambda f: _d6(f),
    "7": lambda f: _p("M0 4 H66 V26 L35 100 H9 L41 26 H0 Z", f),
    "8": lambda f: (_eo(f"{rr(5,4,56,48,24)} {rr(27,24,12,10,5)}", f)
                    + _eo(f"{rr(0,44,66,56,28)} {rr(24,64,18,16,8)}", f)),
    "9": lambda f: f'<g transform="rotate(180 33 52)">{_d6(f)}</g>',
    ":": lambda f: _p(f"{rr(0,30,22,22,6)} {rr(0,72,22,22,6)}", f),
}

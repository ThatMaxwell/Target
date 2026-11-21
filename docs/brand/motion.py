"""Logo motion: the squircle target becomes the thick 'target' badge. Five takes.

Every moving value is computed here from real easing curves and springs, sampled at 60 fps,
and written as SMIL keyframes (linear between samples). Phases overlap and hand their speed
to each other, so nothing stalls between steps. Output is plain SVG: no JS, no CSS.

Run:  python motion.py
Out:  motion/take-N-name.svg       plays once, the real thing (reload to replay)
      motion/take-N-name-loop.svg  loops with a pause, for reviewing
"""
import math, pathlib
from letters import LETTERS, GAP, INK, PAPER, WM_W

OUTDIR = pathlib.Path(__file__).parent / "motion"
FPS = 60
PAD = 22
W, H = WM_W + 2 * PAD, 170           # the thick badge: 456 x 170
CX, CY = W / 2, H / 2
TX, TY = PAD, PAD - 4                # where the word sits inside the badge
WORD = "target"
WID = [LETTERS[c](INK)[0] for c in WORD]
OFF = [sum(WID[:i]) + GAP * i for i in range(len(WORD))]
DIST = [abs(TX + OFF[i] + WID[i] / 2 - CX) for i in range(len(WORD))]   # letter distance from center
T_OUT, T_HOLE, T_CEN, RF = 150, 104, 62, .37                             # the squircle target
BADGE_R = 18
MARGIN = 16


# ---------------------------------------------------------------- numbers, shapes
def n(v, p=2):
    s = f"{v:.{p}f}".rstrip("0").rstrip(".")
    return "0" if s in ("", "-0") else s

def rr(x, y, w, h, r):
    """Rounded rect. Always the same commands, so SMIL can tween between any two of them."""
    w, h = max(w, 0), max(h, 0)
    r = max(0, min(r, w / 2, h / 2))
    f = lambda v: n(v, 1)
    return (f"M{f(x+r)} {f(y)}H{f(x+w-r)}A{f(r)} {f(r)} 0 0 1 {f(x+w)} {f(y+r)}V{f(y+h-r)}"
            f"A{f(r)} {f(r)} 0 0 1 {f(x+w-r)} {f(y+h)}H{f(x+r)}A{f(r)} {f(r)} 0 0 1 {f(x)} {f(y+h-r)}"
            f"V{f(y+r)}A{f(r)} {f(r)} 0 0 1 {f(x+r)} {f(y)}Z")

def rc(cx, cy, w, h, r):
    return rr(cx - w / 2, cy - h / 2, w, h, r)

def sq(s, cx=CX, cy=CY):
    return rc(cx, cy, s, s, s * RF)


# ---------------------------------------------------------------- easing
def bez(x1, y1, x2, y2):
    def f(t):
        if t <= 0: return 0.0
        if t >= 1: return 1.0
        lo, hi = 0.0, 1.0
        for _ in range(48):
            u = (lo + hi) / 2
            if 3 * (1 - u) ** 2 * u * x1 + 3 * (1 - u) * u * u * x2 + u ** 3 < t: lo = u
            else: hi = u
        u = (lo + hi) / 2
        return 3 * (1 - u) ** 2 * u * y1 + 3 * (1 - u) * u * u * y2 + u ** 3
    return f

IN_OUT = bez(.65, 0, .35, 1)        # cubic in-out
OUT = bez(.33, 1, .68, 1)           # cubic out
OUT_EXPO = bez(.16, 1, .3, 1)
IN = bez(.32, 0, .67, 0)            # cubic in

def spring(w, z=1.0):
    """Step response of a damped spring (t in seconds). z=1 critically damped: no overshoot."""
    def f(t):
        if t <= 0: return 0.0
        if z >= 1: return 1 - (1 + w * t) * math.exp(-w * t)
        wd = w * math.sqrt(1 - z * z)
        return 1 - math.exp(-z * w * t) * (math.cos(wd * t) + z * w / wd * math.sin(wd * t))
    return f

def ph(t, a, b, ease=lambda x: x):
    return 0.0 if t <= a else 1.0 if t >= b else ease((t - a) / (b - a))

def sp(t, a, f):
    v = f(t - a) if t > a else 0.0
    return 1.0 if (t - a) > .25 and abs(v - 1) < .0015 else v

def lerp(a, b, p):
    return a + (b - a) * p


# ---------------------------------------------------------------- timeline -> SMIL
class TL:
    def __init__(self, end, loop):
        self.end, self.loop = end, loop
        self.frames = int(round((end + 1.8 if loop else end) * FPS))
        self.cyc = self.frames / FPS

    def a(self, attr, fn, kind=None, raw=False):
        ts = [i / FPS for i in range(self.frames + 1)]
        vals = [fn(t if raw else min(t, self.end)) for t in ts]
        last = len(vals) - 1
        keep = [0] + [i for i in range(1, last) if not (vals[i - 1] == vals[i] == vals[i + 1])] + [last]
        kt = ";".join("1" if i == last else f"{ts[i] / self.cyc:.5f}" for i in keep)
        vs = ";".join(vals[i] for i in keep)
        tag, typ = ("animateTransform", f' type="{kind}"') if kind else ("animate", "")
        timing = 'repeatCount="indefinite"' if self.loop else 'fill="freeze"'
        return (f'<{tag} attributeName="{attr}"{typ} dur="{n(self.cyc, 4)}s" {timing} '
                f'calcMode="linear" keyTimes="{kt}" values="{vs}"/>')

    def master(self):
        if not self.loop:
            return ""
        e = self.end
        return self.a("opacity", lambda t: n(1 - ph(t, e + 1.2, e + 1.5, IN_OUT), 3), raw=True)


def about(tl, px, py, inner, scale=None, rotate=None, opacity=None, translate=None):
    """Animate a group around a pivot point."""
    an = ""
    if scale: an += tl.a("transform", scale, "scale")
    if rotate: an += tl.a("transform", rotate, "rotate")
    if translate: an += tl.a("transform", translate, "translate")
    if opacity: an += tl.a("opacity", opacity)
    op0 = f' opacity="{opacity(0)}"' if opacity else ""
    return (f'<g transform="translate({n(px)} {n(py)})"><g{op0}>{an}'
            f'<g transform="translate({n(-px)} {n(-py)})">{inner}</g></g></g>')

def intro(tl, inner):
    return about(tl, CX, CY, inner,
                 scale=lambda t: n(lerp(.84, 1, ph(t, 0, .42, OUT_EXPO)), 4),
                 opacity=lambda t: n(ph(t, 0, .2, OUT), 3))

def letter(i, fill=PAPER):
    return LETTERS[WORD[i]](fill)[1]

def place(i, inner):
    return f'<g transform="translate({n(TX + OFF[i])} {n(TY)})">{inner}</g>'

def path(fill, fn, tl, evenodd=True, extra=""):
    rule = ' fill-rule="evenodd"' if evenodd else ""
    return f'<path fill="{fill}"{rule} d="{fn(0)}"{extra}>{tl.a("d", fn)}</path>'

def body_fn(k_fn, w0=T_OUT, h0=T_OUT, r0=T_OUT * RF):
    """Outer block: squircle -> badge, driven by a progress function (may overshoot past 1)."""
    def f(t):
        k = k_fn(t)
        return rc(CX, CY, lerp(w0, W, k), lerp(h0, H, k), lerp(r0, BADGE_R, min(k, 1)))
    return f

def doc(tl, name, note, defs, body):
    vw, vh = W + 2 * MARGIN, H + 2 * MARGIN
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-MARGIN} {-MARGIN} {n(vw)} {n(vh)}" '
            f'width="{n(vw)}" height="{n(vh)}">\n'
            f'  <!-- target logo motion, take: {name}. {note} {"Loops for review." if tl.loop else "Plays once; reload to replay."} -->\n'
            f'  <defs>{defs}</defs>\n  <g>{tl.master()}{body}</g>\n</svg>\n')


# ---------------------------------------------------------------- take 1: clean
def take_clean(loop):
    """The gap seals while the block is already stretching; letters rise from behind a hidden line."""
    tl = TL(1.95, loop)
    stretch = bez(.6, 0, .1, 1)
    k_fn = lambda t: ph(t, .60, 1.32, stretch)
    outer = body_fn(k_fn)

    def mark(t):
        s = ph(t, .30, .80, IN_OUT)
        hole, cen = (lerp(T_HOLE, 83, s), lerp(T_CEN, 83, s)) if s < 1 else (0, 0)
        return outer(t) + sq(hole) + sq(cen)

    defs = (f'<clipPath id="body"><path d="{outer(0)}">{tl.a("d", outer)}</path></clipPath>'
            f'<clipPath id="line"><rect x="0" y="0" width="{W}" height="152"/></clipPath>')
    rise = spring(15)
    letters = ""
    for i in range(len(WORD)):
        t0 = 1.0 + DIST[i] * .0009
        f = lambda t, t0=t0: f"0 {n(lerp(136, 0, sp(t, t0, rise)), 1)}"
        letters += place(i, f'<g transform="translate(0 136)">{tl.a("transform", f, "translate")}{letter(i)}</g>')
    body = intro(tl, path(INK, mark, tl)) + f'<g clip-path="url(#body)"><g clip-path="url(#line)">{letters}</g></g>'
    return doc(tl, "clean", "Gap seals, block stretches in the same breath, letters rise from a hidden baseline.", defs, body)


# ---------------------------------------------------------------- take 2: iris
def take_iris(loop):
    """Spins shut like a camera aperture, squashes, snaps out into the badge; letters pop from the center."""
    tl = TL(2.0, loop)
    squash = lambda t: ph(t, .62, .84, IN_OUT)
    release = spring(15, .8)                      # ~1.5% overshoot on the snap, then settles
    k_rel = lambda t: sp(t, .84, release)

    def outer(t):
        a, k = squash(t), k_rel(t)
        w = lerp(lerp(T_OUT, 132, a), W, k)
        h = lerp(lerp(T_OUT, 160, a), H, k)
        r = lerp(lerp(T_OUT * RF, 50, a), BADGE_R, min(k, 1))
        return rc(CX, CY, w, h, r)

    def mark(t):
        s = ph(t, .20, .78, bez(.5, 0, .3, 1))
        hole = lerp(T_HOLE, T_CEN, s) if s < 1 else 0
        cen = T_CEN if s < 1 else 0
        return outer(t) + sq(hole) + sq(cen)

    spin = lambda t: n(-90 * (1 - ph(t, .08, .84, IN_OUT)), 2)
    mark_g = about(tl, CX, CY, path(INK, mark, tl), rotate=spin)
    defs = f'<clipPath id="body"><path d="{outer(0)}">{tl.a("d", outer)}</path></clipPath>'
    pop = spring(17, .72)
    letters = ""
    for i in range(len(WORD)):
        t0 = .98 + DIST[i] * .0011
        letters += place(i, about(tl, WID[i] / 2, 100, letter(i),
                                  scale=lambda t, t0=t0: n(lerp(.3, 1, sp(t, t0, pop)), 4),
                                  opacity=lambda t, t0=t0: n(ph(t, t0, t0 + .1), 3)))
    body = intro(tl, mark_g) + f'<g clip-path="url(#body)">{letters}</g>'
    return doc(tl, "iris", "Aperture spin, squash, snap. The one take with a tiny overshoot on purpose.", defs, body)


# ---------------------------------------------------------------- take 3: split
def take_split(loop):
    """The white ring divides like a cell into the bowls of a, g and e; stems, tail and aperture grow in."""
    tl = TL(1.95, loop)
    k_fn = lambda t: ph(t, .42, 1.15, bez(.62, 0, .18, 1))
    outer = body_fn(k_fn)
    bulge = lambda t: 12 * ph(t, .24, .44, IN_OUT)

    xa, xg, xe = TX + OFF[1], TX + OFF[3], TX + OFF[4]
    bowls = [  # (outer x,y,w,h,r), (inner x,y,w,h,r)
        ((xa, TY + 26, 70, 74, 30), (xa + 24, TY + 48, 22, 30, 10)),
        ((xg, TY + 26, 70, 70, 30), (xg + 24, TY + 46, 22, 28, 10)),
        ((xe, TY + 26, 72, 74, 30), (xe + 22, TY + 44, 28, 12, 6)),
    ]

    def bowl_fn(o, ins):
        ocx, ocy = o[0] + o[2] / 2, o[1] + o[3] / 2
        icx, icy = ins[0] + ins[2] / 2, ins[1] + ins[3] / 2
        dx = ocx - CX
        def f(t):
            p = ph(t, .40, 1.12, IN_OUT)
            b = bulge(t) * (1 - p)
            smear = math.sin(math.pi * p)
            sw, sh = .1 * abs(dx) * smear, .04 * abs(dx) * smear     # stretch along the travel
            outer_d = rc(lerp(CX, ocx, p), lerp(CY, ocy, p), lerp(T_HOLE + b, o[2], p) + sw,
                         lerp(T_HOLE, o[3], p) - sh, lerp(T_HOLE * RF, o[4], p))
            inner_d = rc(lerp(CX, icx, p), lerp(CY, icy, p), lerp(T_CEN + b * .6, ins[2], p) + sw * .6,
                         lerp(T_CEN, ins[3], p) - sh * .6, lerp(T_CEN * RF, ins[4], p))
            return outer_d + inner_d
        return f

    grow = spring(16)
    # a: stem grows up from the baseline
    stem_x, base = xa + 50, TY + 100
    stem = lambda t: rr(stem_x, base - 74 * sp(t, .98, grow), 24, 74 * sp(t, .98, grow), 0)
    # g: stem + tail drawn downward by a growing clip
    g_hook = f'<path fill="{PAPER}" d="M50 26 H74 V104 Q74 130 46 130 H6 V110 H44 Q50 110 50 104 Z"/>'  # g stem + tail (letters.py)
    hook_clip_h = lambda t: n(112 * ph(t, 1.0, 1.4, OUT), 1)
    # e: the aperture is cut in from the eye outward
    cut = lambda t: rr(xe + 22, TY + 72, 60 * ph(t, 1.02, 1.34, OUT), 10, 0)
    # t, r, t spring up from the baseline
    up = spring(17, .78)
    pops = ""
    for i, t0 in ((0, 1.04), (2, .98), (5, 1.08)):
        pops += place(i, about(tl, WID[i] / 2, 100, letter(i),
                               scale=lambda t, t0=t0: f"{n(lerp(.7, 1, sp(t, t0, up)), 4)} {n(sp(t, t0, up), 4)}",
                               opacity=lambda t, t0=t0: n(ph(t, t0 + .02, t0 + .12), 3)))

    defs = (f'<clipPath id="body"><path d="{outer(0)}">{tl.a("d", outer)}</path></clipPath>'
            f'<clipPath id="hook"><rect x="{n(xg - 4)}" y="{n(TY + 24)}" width="84" height="0">'
            f'{tl.a("height", hook_clip_h)}</rect></clipPath>')
    white = "".join(path(PAPER, bowl_fn(o, i), tl) for o, i in bowls)
    white += path(PAPER, stem, tl, evenodd=False)
    white += f'<g clip-path="url(#hook)"><g transform="translate({n(xg)} {n(TY)})">{g_hook}</g></g>'
    white += path(INK, cut, tl, evenodd=False)
    white += pops
    mark = path(INK, outer, tl, evenodd=False) + f'<g clip-path="url(#body)">{white}</g>'
    return doc(tl, "split", "The ring divides into the bowls of a, g and e.", defs, intro(tl, mark))


# ---------------------------------------------------------------- take 4: dive
def take_dive(loop):
    """Fly into the target: the rings rush past the camera, the center grows into the badge."""
    tl = TL(2.0, loop)
    ring = f'<path fill="{INK}" fill-rule="evenodd" d="{sq(T_OUT)}{sq(T_HOLE)}"/>'
    ring_g = about(tl, CX, CY, ring,
                   scale=lambda t: n(1 + 7 * ph(t, .36, 1.02, IN), 4),
                   opacity=lambda t: n(1 - ph(t, .72, .98, IN_OUT), 3))
    center = body_fn(lambda t: ph(t, .40, 1.2, bez(.7, 0, .12, 1)), T_CEN, T_CEN, T_CEN * RF)
    defs = f'<clipPath id="body"><path d="{center(0)}">{tl.a("d", center)}</path></clipPath>'
    land = spring(15)
    letters = ""
    for i in range(len(WORD)):
        t0 = 1.0 + DIST[i] * .001
        letters += place(i, about(tl, WID[i] / 2, 67, letter(i),
                                  scale=lambda t, t0=t0: n(lerp(1.55, 1, sp(t, t0, land)), 4),
                                  opacity=lambda t, t0=t0: n(ph(t, t0, t0 + .14, OUT), 3)))
    body = intro(tl, path(INK, center, tl, evenodd=False) + ring_g) + f'<g clip-path="url(#body)">{letters}</g>'
    return doc(tl, "dive", "The rings fly past the camera; the bullseye becomes the badge.", defs, body)


# ---------------------------------------------------------------- take 5: type
def take_type(loop):
    """The ring squeezes into a text cursor, which types the word and blinks out."""
    gaps = [.10, .125, .09, .13, .10, .115]
    t_start = 1.12
    tk = [t_start + sum(gaps[:i]) for i in range(len(WORD))]
    t_end_type = tk[-1]
    tl = TL(t_end_type + 1.05, loop)
    outer = body_fn(lambda t: ph(t, .48, 1.08, bez(.62, 0, .18, 1)))
    CW, CH, CR, CYT = 10, 118, 3, 26

    def caret_x(t):
        x = lerp(CX - CW / 2, TX - 15, ph(t, .66, 1.06, IN_OUT))
        for k in range(len(WORD)):
            x = lerp(x, TX + OFF[k] + WID[k] + 5, ph(t, tk[k], tk[k] + .07, OUT))
        return x

    def caret(t):
        m = ph(t, .26, .70, IN_OUT)
        x = caret_x(t)
        ccx, ccy = x + CW / 2, CYT + CH / 2
        o = rc(lerp(CX, ccx, m), lerp(CY, ccy, m), lerp(T_HOLE, CW, m), lerp(T_HOLE, CH, m), lerp(T_HOLE * RF, CR, m))
        s = lerp(T_CEN, 0, m)
        i = rc(lerp(CX, ccx, m), lerp(CY, ccy, m), s, s, s * RF)
        return o + i

    def blink(t):
        d = t - t_end_type
        return "1" if d < .40 or .64 <= d < .88 else "0"

    letters = ""
    for k in range(len(WORD)):
        t0 = tk[k]
        letters += place(k, about(tl, 0, 0, letter(k),
                                  translate=lambda t, t0=t0: f"0 {n(lerp(9, 0, ph(t, t0, t0 + .18, OUT_EXPO)), 2)}",
                                  opacity=lambda t, t0=t0: n(ph(t, t0, t0 + .05), 3)))
    defs = f'<clipPath id="body"><path d="{outer(0)}">{tl.a("d", outer)}</path></clipPath>'
    cursor = f'<g>{tl.a("opacity", blink)}{path(PAPER, caret, tl)}</g>'
    mark = path(INK, outer, tl, evenodd=False) + f'<g clip-path="url(#body)">{cursor}{letters}</g>'
    return doc(tl, "type", "The ring becomes a cursor and types the word.", defs, intro(tl, mark))


TAKES = [("1-clean", take_clean), ("2-iris", take_iris), ("3-split", take_split), ("4-dive", take_dive), ("5-type", take_type)]

if __name__ == "__main__":
    OUTDIR.mkdir(exist_ok=True)
    for name, fn in TAKES:
        for loop in (False, True):
            f = OUTDIR / f"take-{name}{'-loop' if loop else ''}.svg"
            f.write_text(fn(loop), encoding="utf-8")
            print(f"{f.name:28s} {f.stat().st_size // 1024:4d} KB")

"""Builds app.html (the browser shell prototype) from app.template.html.
Inlines the drawn wordmark (badge), the clock digits (docs/brand/letters.py) and the logo's
Split animation (docs/brand/motion.py),
so the page needs no fonts and no images of its own. Run:  python build.py
"""
import pathlib, sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / "docs" / "brand"))
from letters import word, DIGITS  # noqa: E402
import motion  # noqa: E402


def badge():
    # each call to word() gets fresh mask ids, so two badges can share the page
    wm, w = word("target", "currentColor")
    return f'<svg viewBox="-2 2 {w + 4} 130" role="img" aria-label="target">{wm}</svg>'


glyphs = "".join(f'<g id="g{c}">{DIGITS[c]("currentColor")}</g>' for c in "0123456789")
glyphs += f'<g id="gc">{DIGITS[":"]("currentColor")}</g>'

# the logo is motion.py's Split take, bare and paused; the page scrubs it. 30 fps keyframes are plenty
# because the page interpolates between them. Colors become classes so the page can theme it.
motion.FPS = 30
logo = (motion.take_split(False, bare=True, pre="lg-")
        .replace('fill="#111"', 'class="k"').replace('fill="#fff"', 'class="p"'))
assert "#111" not in logo and "#fff" not in logo

html = (HERE / "app.template.html").read_text(encoding="utf-8")
html = html.replace("__BADGE2__", badge()).replace("__BADGE__", badge()).replace("__GLYPHS__", glyphs).replace("__LOGO__", logo)
(HERE / "app.html").write_text(html, encoding="utf-8")
print(f"app.html written ({len(html) // 1024} KB)")

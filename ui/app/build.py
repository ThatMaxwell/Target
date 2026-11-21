"""Builds app.html (the browser shell prototype) from app.template.html.
Inlines the drawn wordmark (badge) and the drawn clock digits from docs/brand/letters.py,
so the page needs no fonts and no images of its own. Run:  python build.py
"""
import pathlib, sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / "docs" / "brand"))
from letters import word, DIGITS  # noqa: E402


def badge():
    # each call to word() gets fresh mask ids, so two badges can share the page
    wm, w = word("target", "currentColor")
    return f'<svg viewBox="-2 2 {w + 4} 130" role="img" aria-label="target">{wm}</svg>'


glyphs = "".join(f'<g id="g{c}">{DIGITS[c]("currentColor")}</g>' for c in "0123456789")
glyphs += f'<g id="gc">{DIGITS[":"]("currentColor")}</g>'

html = (HERE / "app.template.html").read_text(encoding="utf-8")
html = html.replace("__BADGE2__", badge()).replace("__BADGE__", badge()).replace("__GLYPHS__", glyphs)
(HERE / "app.html").write_text(html, encoding="utf-8")
print(f"app.html written ({len(html) // 1024} KB)")

"""Builds card.html (the Target Plus subscription card) from card.template.html.
Inlines the thick drawn wordmark from docs/brand/letters.py. Run:  python build.py
"""
import pathlib, sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / "docs" / "brand"))
from letters import word  # noqa: E402

wm, w = word("target", "currentColor")
# a thick plus in the same stroke (24) as the letters, centred on the x-height (26..100)
px = w + 14
plus = (f'<rect fill="currentColor" x="{px}" y="51" width="62" height="24"/>'
        f'<rect fill="currentColor" x="{px + 19}" y="32" width="24" height="62"/>')
mark = f'<svg viewBox="-2 2 {px + 66} 130" aria-hidden="true">{wm}{plus}</svg>'
html = (HERE / "card.template.html").read_text(encoding="utf-8").replace("__WORD__", mark)
(HERE / "card.html").write_text(html, encoding="utf-8")
print(f"card.html written ({len(html) // 1024} KB)")

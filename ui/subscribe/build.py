"""Builds card.html (the Target Plus subscription card) from card.template.html.
Inlines the thick target badge from docs/brand/letters.py. Run:  python build.py
"""
import pathlib, sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / "docs" / "brand"))
from letters import word  # noqa: E402

# the same thick badge the app uses (ui/app/build.py), reused as the plan's name
wm, w = word("target", "currentColor")
badge = f'<svg viewBox="-2 2 {w + 4} 130" aria-hidden="true">{wm}</svg>'
html = (HERE / "card.template.html").read_text(encoding="utf-8").replace("__BADGE__", badge)
(HERE / "card.html").write_text(html, encoding="utf-8")
print(f"card.html written ({len(html) // 1024} KB)")

"""Builds card.html (the Target Plus subscription card) from card.template.html.
Inlines the brand black badge (docs/brand/logos/24-badge-black.svg) plus a thick +. Run:  python build.py
"""
import pathlib, re, sys

HERE = pathlib.Path(__file__).parent

# the brand's black badge (docs/brand/logos/24-badge-black.svg, made by docs/brand/gen.py), used as-is,
# followed by a thick plus in the letters' own stroke (24), centred on the x-height
src = (HERE.parents[1] / "docs" / "brand" / "logos" / "24-badge-black.svg").read_text(encoding="utf-8")
W, H = (float(v) for v in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', src).groups()[:2])
inner = re.sub(r"<!--.*?-->", "", src.split(">", 1)[1].rsplit("</svg>", 1)[0], flags=re.S).strip()
px, cy = W + 18, 18 + 63              # badge text sits at y+18; x-height 26..100 has its middle at 63
plus = (f'<g class="plus"><rect x="{px}" y="{cy - 12}" width="62" height="24"/>'
        f'<rect x="{px + 19}" y="{cy - 31}" width="24" height="62"/></g>')
badge = f'<svg viewBox="0 0 {px + 62} {H}" aria-hidden="true">{inner}{plus}</svg>'
html = (HERE / "card.template.html").read_text(encoding="utf-8").replace("__BADGE__", badge)
(HERE / "card.html").write_text(html, encoding="utf-8")
print(f"card.html written ({len(html) // 1024} KB)")

"""Builds index.html: a self-contained preview of every logo concept (SVGs embedded as data URIs).
Run from this folder:  python build-preview.py"""
import base64, json, pathlib
here = pathlib.Path(__file__).parent
# [file, name, note, wide, keep_colors_on_dark]
sections = [
 ["Round 3: icons", "App-icon ideas beyond the tab shape. Tab is also a key on every keyboard, so 18 and 19 use that.", [
  ["18-icon-tab-key.svg","Tab key","The Tab key symbol: an arrow that hits a wall. The name's second meaning.",0,0],
  ["19-icon-keycap.svg","Keycap","The actual Tab keycap: label bottom-left, arrow top-right. On the yellow accent.",0,1],
  ["14-icon-wordmark.svg","Wordmark tile","The wordmark oversized and cropped by the tile.",0,0],
  ["15-icon-big-t.svg","Big t","One giant t, tail always visible. With the tail cropped it read as a cross.",0,0],
  ["16-icon-wide-tab.svg","Wide tab tile","The wide tab (08) shrunk onto a tile, on its strip.",0,0],
  ["17-icon-stack.svg","Stack","A stack of tabs: many open, one in front.",0,0],
  ["20-icon-address.svg","Address bar","An address bar with a t and a blinking caret.",0,0],
 ]],
 ["Round 2: out of the tombstone", "Round 1 read as a gravestone: a tall slab with a rounded top and one carved letter. Round 2 keeps tabs wide, on a strip, or part of a window.", [
  ["08-wide-tab.svg","Wide tab","Real browser proportions: wide, on the strip, title and close button.",1,0],
  ["09-strip.svg","Tab strip","Two tabs on a strip; the active one is ours. Low and wide.",0,0],
  ["10-window.svg","Window","A window body with one tab at the top left. Verdict: it reads as a folder icon. Dead end.",0,0],
  ["12-icon-color.svg","Icon with accent","The window mark on one accent color. Tests the 'brand color in one place' rule.",0,1],
  ["13-startup-window.svg","Startup: window","Body rises, the tab pops out of its top edge, the t lifts in. Loops here.",0,0],
  ["11-hero-window.svg","As material: window","A giant window rising from the screen bottom, wordmark cropped by the edge.",1,0],
 ]],
 ["Round 1", "Kept for comparison. The wordmark and the hero crop still hold up; the tall tab marks are the tombstones.", [
  ["05-wordmark.svg","Wordmark","Heavy and tight. Round bowls, single-story a, same stroke as the t.",1,0],
  ["01-tab.svg","Tab","Tall tab with a heavy t pushed left.",0,0],
  ["02-tab-flared.svg","Flared tab","Real tab silhouette with the t cut out.",0,0],
  ["03-t.svg","The t","The letter alone, drawn by hand.",0,0],
  ["04-app-icon.svg","App icon","A white tab rising from the bottom of a black tile.",0,0],
  ["07-startup.svg","Startup: strip","Strip draws out, tab rises, t lifts in.",0,0],
  ["06-hero.svg","As material","Giant tab from the screen edge, wordmark cropped.",1,0],
 ]],
]
svg = {}
for _, _, items in sections:
    for f, *_ in items:
        svg[f] = "data:image/svg+xml;base64," + base64.b64encode((here / f).read_bytes()).decode()
page = (here / "preview-template.html").read_text(encoding="utf-8")
page = page.replace("__SVG__", json.dumps(svg)).replace("__SECTIONS__", json.dumps(sections))
(here / "index.html").write_text(page, encoding="utf-8")
print("index.html built with", len(svg), "concepts")

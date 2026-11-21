# Design Study: Thick, Minimal Marks

What we're aiming for: the minimalism of **Search's** logo, plus the way **mini** uses its mark as a design material. Builds on [design-principles.md](design-principles.md).

---

## 1. Teardown: Search

A black capsule (pill) with a white, heavy "S" sitting at the left end.

- **One letter, one shape, two colors.** Nothing else. No gradient, no shading, no icon metaphor.
- **The shape means something.** A pill with a circle-ish form at one end reads as a **toggle switch**, an "on" button for the web. The container isn't just a frame; it's part of the idea.
- **The letter is heavy enough to hold its own** against a solid black field. A thin letter would disappear.
- **Asymmetric placement.** The S hugs the left end instead of sitting centered, and the empty right side gives the mark direction and motion.
- **Survives 16 px.** One heavy glyph on a solid shape is the most legible thing you can put in a favicon or tab.

## 2. Teardown: mini

App icon: an orange rounded square with a heavy lowercase "m" in white, pushed to the bottom right. Website hero: the wordmark "mini" in giant white letters inside a black panel.

- **The mark is a material, not a sticker.** On the site, the wordmark *is* the hero. It's blown up until it's a graphic, not a label.
- **The container comes from the UI.** The black hero panel has big rounded corners only at the bottom, and there's a grabber bar underneath: it's a **sheet** that's been pulled down. The logo lives inside a real interface element.
- **The icon letter is pushed off-center** (bottom right), the same move Search makes. It feels placed, not centered by default.
- **Heavy, wide, tight type everywhere.** The headline "Design controls, done differently." is set very bold with tight negative tracking and a tight line height. It feels like the logo's voice.
- **Black does the heavy lifting.** The selected toolbar button is black; the others are pale gray. The brand color appears in exactly one place (the icon), so it stays special.
- **Copy is short and specific.** One idea, two lines, no fluff.

## 3. Why a thick logo pays off

A heavy, simple mark can be used in ways a detailed one can't:

| Use | How |
|---|---|
| **Hero supergraphic** | Scale the mark or wordmark to fill a screen or panel, like mini. |
| **Cropping** | Let it bleed off the edge. A heavy letter stays recognizable even when only half is visible. Brand systems like NLB's "supersize logo" and AO's "supersign" make this a formal rule. |
| **Container = UI** | The logo's shape (pill, square) becomes a button, a tab, a toggle, the new-tab page frame. |
| **Loading and startup** | Simple shapes animate cleanly: fill, slide, morph. Detailed marks turn to mush in motion. |
| **Favicon and tab** | Works at 16 px with no special small version. |
| **One color anywhere** | Prints, embroiders, goes on a sticker, inverts for dark mode. |
| **Pattern** | Repeated, it makes a texture for backgrounds, merch, loading states. |

## 4. Rules for our mark (once the new name exists)

1. **One heavy letterform** (or a very short wordmark) on **one solid shape**. Two colors at most.
2. **The container must mean something in a browser**: a tab, the address bar's capsule, a window, a toggle. Search took the toggle; we should find our own.
3. **Place the letter on purpose.** Off-center, hugging an edge, or cut by the frame. Never centered just because that's the default.
4. **Heavy enough to crop.** Test: hide half of it. If you can still tell what it is, it's thick enough.
5. **Black first.** A brand color, if any, is used in one place only.
6. **Test at 16, 32, 64 and 1600 px**, in light and dark, still and animated.
7. **Draw the letter; don't type it.** A logo from a stock font is the fastest way to look generic. Start from a typeface, then adjust terminals, counters and joins by hand.

## 4b. Lessons from the Tab logo rounds

- **The tombstone trap.** A tall slab with a rounded top and one letter on it reads as a gravestone. Round 1 fell into it. Keep tab shapes **wide and low** (real tab proportions are about 3:1 or wider), or show them **on the strip** next to other tabs.
- **The cross trap.** A heavy t with its tail hidden or cropped is a cross, and a cross on a rounded slab is a gravestone. That's most likely the real reason round 1 felt creepy. **The t's tail must always be visible.**
- **The folder trap.** A body with a small tab at the top left reads as a folder icon, not a browser.
- **Context is what makes a shape read as a tab**: the strip line under it, flared feet, a title and a close ×. The wide tab with the wordmark and × (concept 08) was the first one that reads instantly as "browser tab".
- **The wordmark is the strongest asset so far.** It holds up alone, cropped, and at hero scale.

## 5. Type direction

Heavy, slightly wide grotesk; tight tracking for display sizes; normal tracking for UI text.

- **Constraint: we're open source**, so the UI font should be under the SIL Open Font License (free to ship). Commercial faces like Monument Extended (Pangram Pangram) or Gravity (Dinamo) are fine for the *logo drawing* only if licensed, never bundled.
- **OFL candidates to test:** Archivo (has expanded widths up to Black), Unbounded (wide, heavy), Hanken Grotesk, Familjen Grotesk.
- **Avoid:** Inter and Geist as the display face (the strongest "AI-made" tell, see design-principles.md).
- **Display setting:** heavy weight, tracking around −2% to −4%, line height around 0.9–1.0. Like mini's headline: tight but never touching.

## 6. What carries over from the cube work

Cubit is retired as a name, but the cube concepts in [logo/](logo/index.html) stay as reference. The lesson that carries over: the **solid, single-ink** versions (02 Flat, 06 Front-on) were the strongest because they were the thickest. The new mark should start from there.

## Sources
- [How to be creative with a single letter logo (Tailor Brands)](https://www.tailorbrands.com/blog/single-letter-logo)
- [Designing minimalist logos (Piktochart)](https://piktochart.com/blog/designing-minimalist-logos/)
- [Best monogram logo designs (DesignRush)](https://www.designrush.com/best-designs/logo/trends/best-monogram-logo-designs)
- [Outside the box: clipping the logo (A List Apart)](https://alistapart.com/blog/post/outside-the-box/)
- [NLB supersize logo](https://nlb.si/brand/communication-identity/basic-image-elements/supersize-logo)
- [AO supersign](https://www.aofoundation.org/brand/basic-elements/ao-supersign)
- [Oversized type as structure (Contra)](https://contra.com/p/UOZRmmNv-big-hero-6-how-type-becomes-the-superhero)
- [Monument Wide (Pangram Pangram)](https://pangrampangram.com/products/monument-wide)
- [The best extended typefaces (Pangram Pangram)](https://pangrampangram.com/blogs/journal/extended-typefaces)
- [Gravity (Dinamo)](https://abcdinamo.com/newsletter/the-return-of-gravity-the-font-drama-continues)

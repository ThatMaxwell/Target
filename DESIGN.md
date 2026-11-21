# DESIGN.md

The design contract for this browser. Agents (and people) read this before building any UI, and check work against it before showing it.
Background research: [docs/design-principles.md](docs/design-principles.md), [docs/design-study.md](docs/design-study.md).

## Working name: Target
**Legal caution:** Target Corp's bullseye is a legally *famous* mark (one ruling found 96% of Americans recognize it), and famous marks are protected outside their own category. Adobe also sells "Adobe Target". Get a trademark lawyer's opinion before any public launch.
**Visual rule that follows:** never use red as a brand color. Ring/target marks are being explored at the founder's request (2026-11-21): prefer rounded-square rings (they match our letter bowls), keep them black, and treat round red-and-white bullseyes as off limits.

## Direction
**Precision, weight, calm.** A heavy, chunky wordmark used as material (mini-style). Black and white only. The brand idea is **lock-on**: focus brackets and a crosshair that snap onto what matters.

- **Mark system:** chunky lowercase wordmark with squarish bowls (rounded rectangles, not circles); focus brackets ⌜ ⌟; a four-bar crosshair with an open center.
- **Signature interaction:** brackets *lock on* to the thing you're about to act on (focus, hover on tiles, the selected result). Scale 1.08 → 1, opacity 0 → 1, 150 ms ease-out.
- **Color:** black and white only: ink `#111`, paper `#fff`, warm grays (`#f4f4f2`, `#ebebe7`, `#dcdcd7`). **No accent color, anywhere** (founder's call, 2026-11-21).
- **Type:** Archivo (OFL), heavy and slightly wide for display, tight tracking (−3% to −4%), line height 0.9–1.0. UI text at 13.5–15 px, weight 500–650.
- **Shape:** radii 8 / 12 / 20. Pills only for the address bar, toasts and badges.
- **Motion:** 110 press · 150 fast · 220 base · 320 slow. Ease-out for everything, **no overshoot** (the anti-slop detector flags bouncy springs); quick ease-in for things that leave. Animate transform and opacity only. Respect reduced motion.

## Banned (the AI-slop tells)
- Inter, Geist, Roboto as display type. Cream + serif "tasteful default".
- Any accent color (yellow included), purple/indigo, purple-to-blue gradients, gradient text, neon glow.
- Glassmorphism, frosted cards, decorative blur (the command bar scrim blur is the only exception).
- Three-up feature-card rows, icon-in-a-circle feature grids, testimonial carousels.
- Colored left-border stripes on cards, badges floating over hero images, eyebrow kickers above every heading.
- Emoji as icons. Mixed icon sets. Icons must be one set, one stroke weight (2.2).
- Puffy or stacked shadows. At most one subtle layer (`0 1px 2px rgba(0,0,0,.06)`); separate floating things with a border instead.
- Placeholder copy ("Lorem", "John Doe", "Unlock your potential"). Copy must be about *this* browser.
- Fake charts, decorative gauges, stat tiles with made-up numbers.
- Anything centered by default. Place things on purpose.

## Cropping rules (learned the hard way)
- **The t's tail always shows.** Without it, a heavy t is a cross (and on a rounded slab, a gravestone).
- **The g's descender always shows.** Without it, target reads "tarqet".
- Crop the wordmark from the right or top if it has to bleed; never from the bottom.

## Before showing any UI
1. Run `npx -y @gessobuild/anti-slop check <file> --json`, then `fix --write` on the *template*, then resolve the rest. Opt-outs (`data-slop-allow`) only on the inner element, only for real browser-chrome nesting.
2. Check light and dark, 375 px wide and desktop, reduced motion.
3. Check every interactive element has hover, press and focus states.
4. Check there is no accent color: black, white and grays only.

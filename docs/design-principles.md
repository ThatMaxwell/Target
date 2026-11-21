# TBP Design Principles

Research notes, turned into rules for building the browser. Design and feel come first.

## 1. What makes it look "AI-made" (never do these)

- **Default fonts.** Inter or Geist as the display face is the strongest single tell.
- **Default palettes.** Indigo or purple accents, purple-to-blue gradients, neon glow nobody asked for.
- **Default component kits.** The stock shadcn/Tailwind look, untouched.
- **Decoration for its own sake.** Colored left-border stripes on cards, gradient-clipped headlines, puffy shadows, badges floating over everything.
- **Emoji as icons.** One consistent icon set, drawn at one stroke weight.
- **Generic copy.** If a line could sit on a competitor's site, it isn't about us. No "John Doe" placeholders.
- **Swapping one default for another.** Cream backgrounds and a serif are the 2026 "tasteful default". Picking that isn't taste either.

## 2. What to do instead

- **Decide the system before building.** Type scale, spacing scale, radius scale, color tokens, and motion tokens get written down once and used everywhere.
- **One priority per screen.** Every surface has one thing that matters most.
- **Remove first.** Start by cutting what isn't needed. A browser's UI is chrome around someone else's content, so less is more.
- **A point of view.** Arc's designers said a browser should have opinions, not just be a window. TBP's point of view is the black cube: dense, solid, quiet, precise.
- **Consistency beats cleverness.** Inconsistent UI and confusing navigation top every list of what users hate.
- **Audit everything.** Every screen gets a slop check (the `anti-slop` skill) before it ships.

## 3. Motion and feel

| Interaction | Rule |
|---|---|
| Press feedback | 100–160 ms |
| Buttons, toggles, small UI | 200–250 ms |
| Anything else in the UI | under 300 ms. If it feels slow, shorten it before changing the curve. |
| Default easing | ease-out (fast start reads as responsive). Never linear for UI. |
| Gestures, drags, anything interruptible | springs, set as duration + bounce, low bounce |
| What gets animated | `transform` and `opacity` only (GPU). Never layout properties. |
| Reduced motion | respect the OS setting everywhere |

- **Delight without intrusion.** Users loved Arc's surprise animations because they were rare and playful. Keep the rare ones rare.
- **Motion explains.** A tab should move to where it went. A panel should come from where it lives.
- **Perceived speed counts.** Instant feedback, then finish the work. Never block input during an animation.
- **Judge by feel.** Tune every animation live, on real hardware.

## 4. Lessons from the market (Nov 2026)

- **Arc shuts down on December 22, 2026.** Its users feel abandoned and keep asking for it to be open-sourced. Many moved to Zen or Vivaldi. This is TBP's opening: open source means it can't be taken away.
- **Arc's weakness was its learning curve.** Power has to be discoverable, and the defaults have to work for someone who has never heard of the browser.
- **Forced AI annoys people.** Dia's pivot drew a backlash. TBP's AI stays optional, off by default, and never in the way.

## Sources
- [How to de-slopify your designs (UX Collective)](https://uxdesign.cc/how-to-de-slopify-your-designs-4c40c57c1dc9)
- [7 signs a UI has been vibe coded (Fountain Institute)](https://www.thefountaininstitute.com/blog/signs-vibe-coded-ui)
- [Spot the slop: fixing AI defaults](https://world.hey.com/kostac/spot-the-slop-a-ui-designer-s-guide-to-fixing-ai-defaults-4c448c9c)
- [Unslop UI playbook](https://claudecodehq.com/playbooks/unslop-ui)
- [Emil Kowalski: great animations](https://emilkowal.ski/ui/great-animations)
- [NN/g: animation duration](https://nngroup.com/articles/animation-duration)
- [To spring or not to spring](https://www.mintlify.com/raphaelsalaja/userinterface-wiki/animation/to-spring-or-not-to-spring)
- [Arc browser review (UX Collective)](https://uxdesign.cc/why-the-arc-browser-is-the-chrome-replacement-ive-been-waiting-for-1e0a05da9fc9)
- [UX analysis: Arc, Opera, Edge (LogRocket)](https://blog.logrocket.com/ux-design/ux-analysis-arc-opera-edge/)
- [Arc sunsets December 22 (TechCrunch)](https://techcrunch.com/2026/10/22/arc-browser-sunsets-december-22-as-the-browser-company-doubles-down-on-dia/)
- [Arc sunset confirmed (AlternativeTo)](https://alternativeto.net/news/2026/10/the-browser-company-confirms-arc-browser-sunset-directs-users-to-ai-powered-successor-dia/)
- [Common UI design mistakes (Toptal)](https://www.toptal.com/designers/ui/most-common-ui-design-mistakes)

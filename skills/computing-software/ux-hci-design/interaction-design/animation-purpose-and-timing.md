---
id: computing-software.ux-hci-design.interaction-design.animation-purpose-and-timing
name: animation-purpose-and-timing
category: computing-software
field: ux-hci-design
product: interaction-design
tags: [ui-animation-timing, motion-easing]
level: practitioner
status: docs-checked
description: "Use animation to show causality and continuity, with short durations, easing curves and reduced-motion fallbacks."
sources:
  - https://www.nngroup.com/articles/animation-duration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Animation guidelines
- NN/g: the duration of most animations should be in the range of 100-500 ms, depending on complexity and how far the element travels; look for the shortest time that works.
- Objects appearing or entering the screen usually need a subtly longer duration than objects disappearing or exiting.
- Completely linear motion looks unnatural; use easing (ease-in starts slowly and speeds up, ease-out slows at the end, or both).
- Provide a reduced-motion alternative (for example a fade instead of a slide) for users who ask for less motion.

## Verify
- [ ] No animation blocks interaction; reduced-motion setting is respected.
## Checked
2026-11-02. Confirmed against the NN/g article "Executing UX Animations: Duration and Motion Characteristics": duration range, entry vs exit, easing. Removed: the claim that ease-out is for entering and ease-in for leaving, `transform`/`opacity` performance advice and the `prefers-reduced-motion` media query name (not on the page); the Material motion page returned no readable text.
Method: documentation only; no commands were run.

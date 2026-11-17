---
id: creative-arts.design-for-form-and-experience.interaction-design.applying-fitts-law
name: applying-fitts-law
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [fitts-law, laws-of-ux, target-size, pointing-devices, touch-targets, motor-accuracy, ui-ergonomics]
level: practitioner
status: draft
description: "Apply Fitts's law: make frequent targets large and close, use screen edges and corners, enlarge touch targets, add spacing and respect thumb reach to cut pointing time."
sources:
  - "Paul Fitts, The information capacity of the human motor system in controlling the amplitude of movement (1954)"
  - "Jon Yablonski, Laws of UX (lawsofux.com/fittss-law)"
  - "WCAG 2.2 SC 2.5.8 Target Size (Minimum) and 2.5.5 Target Size (w3.org/TR/WCAG22)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fitts's law

**Law:** time to hit a target grows with distance and shrinks with target size: T = a + b log2(D/W + 1).

## Design rules
1. **Make important and frequent targets large.** Minimum target sizes: WCAG 2.2 AA at least **24x24 CSS px** (SC 2.5.8) with spacing; AAA 44x44 (2.5.5); Apple 44x44 pt; Material 48x48 dp. The clickable area may exceed the visible glyph (padding).
2. **Reduce distance:** put the next likely action near the pointer or cursor (contextual menus, inline actions, a primary button near the form end).
3. **Use screen edges and corners** on desktop: the cursor stops there (infinitely deep targets): menu bars at the top edge, docks at the bottom, Windows Start at the corner.
4. **Group and size by frequency;** keep destructive actions apart from frequent ones (spacing at least 8 px) to avoid slips.
5. **Touch:** thumb reach; place frequent actions in the lower half of a phone; avoid tiny close icons at the far top corners; mind accidental taps near system gestures and edges.
6. **Hit area vs visual size:** extend with transparent padding or a pseudo-element; keep tap areas from overlapping.
7. **Avoid moving targets** and animated shifts under the cursor (layout shifts cause misclicks).
8. Sliders, drag handles and scrollbars need generous grab zones.

## Testing
Measure target sizes in design (Figma measurement or Stark), run a touch test with thumbs on real devices; watch mis-tap rates and time on task.

## Verify
- [ ] All interactive targets meet minimum size and spacing.
- [ ] Frequent actions are large and close; destructive ones separated.
- [ ] No layout shift under the pointer on load.

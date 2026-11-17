---
id: creative-arts.animation.vector-graphics.line-cleanup-and-inbetween-passes
name: line-cleanup-and-inbetween-passes
category: creative-arts
field: animation
product: vector-graphics
tags: [line-cleanup, clean-up, inbetweening, ink-and-paint, model-sheet, line-art, on-model]
level: practitioner
status: draft
description: "Run a clean-up pass on rough animation: key, breakdown and inbetween workflow, on-model line quality, line weight rules, closed shapes and handoff to ink and paint."
sources:
  - https://docs.toonboom.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Line cleanup and inbetween clean-up passes

Rough animation is loose and expressive; **clean-up** turns it into on-model final linework ready for colour. Inbetweens fill the in-between poses.

## Workflow
1. **Keys** (extreme poses) are drawn first by the animator, then **breakdowns** and **inbetweens** fill the timing; the assistant or clean-up artist is responsible for consistent final lines.
2. Check each rough against the **model sheet** for proportions, shapes and details.
3. Clean up with a single continuous, confident line per contour; avoid sketchy double lines.
4. Keep **line weight** rules from the model sheet: heavy outer silhouette, thinner interior lines (`variable-width-strokes.md`).
5. **Close shapes**: where colour will go, lines must meet at their ends so that the paint does not leak (`gap-closing-and-paint-bucket-fills.md`).
6. Check **inbetweens** against the keys with onion skin and flipping, correcting volume and spacing.
7. Hand over a clean drawing set with consistent layer names and one drawing per frame or hold.

## Software support
- In vector tools like Toon Boom Harmony, clean-up may happen with the Pencil, Brush, Eraser, Cutter and Contour Editor, and Smooth edit tools on top of roughs on a separate layer (see the Harmony drawing tools documentation).
- With scans, tidy and threshold first, then vectorise (`potrace-vectorisation.md`).

## Review
- Flip the drawings fast: lumps and flicker in line quality or volume stand out.
- Compare to the model sheet in a split screen.

## Verify
- [ ] No gaps in lines where colour will be applied.
- [ ] Consistent line weight and no stray strokes.
- [ ] Inbetweens flip smoothly from key to key.

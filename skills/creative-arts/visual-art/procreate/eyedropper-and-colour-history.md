---
id: creative-arts.visual-art.procreate.eyedropper-and-colour-history
name: eyedropper-and-colour-history
category: creative-arts
field: visual-art
product: procreate
tags: [visual-art, procreate, procreate-colour, eyedropper, colour-history, colour-picker, eyedropper-gesture, sample-colour, recent-colours]
level: intro
status: draft
description: "Pick colours fast in Procreate: eyedropper gestures and delay, sampling the canvas vs a single layer, the previous/current colour circle, and History in the colour panel."
sources: ["https://procreate.com/handbook/procreate/colors/colors-interface/", "https://procreate.com/handbook/procreate/interface-gestures/gestures/", "https://procreate.com/handbook"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Eyedropper and colour history

**Goal:** sample and return to colours quickly while painting (Procreate Handbook,
Colors interface; Gestures).

## Eyedropper
- Default: **touch and hold** a finger on the canvas, or tap the **square button** on
  the sidebar then touch the canvas. A loupe shows the new colour (top half) and
  previous colour (bottom half).
- Set gestures and delay in Actions > Prefs > Gesture controls > Eyedropper (e.g.
  "□ + Apple Pencil", touch-and-hold delay 0.2-0.4 s).
- It samples the **visible composite** of the canvas, not just the current layer;
  to sample one layer's colour, hide others or check the layer's own colour.

## Previous colour
- The colour circle (top right) shows the current colour; in the Colours panel the
  top-right swatch shows current and previous. Tap the previous to swap back
  (useful when alternating two colours).

## Colour History
- In the Colours panel (Disc/Classic/Harmony/Value), **History** shows recently
  used colours (recent versions); tap to reuse. Clear it from the panel.

## Painting workflow
- When painting with blends, re-sample frequently from the canvas to keep
  transitions coherent (painterly technique common in digital painting).
- Sample then adjust slightly (lighter/cooler) rather than picking new colours from
  scratch.

## Gotchas
- Sampling anti-aliased edges: picks in-between colours.
- Multiply/overlay layers change composite colour; the sample includes them.

## Verify
- [ ] Eyedropper gesture fast and not triggering accidentally.
- [ ] Previous/history used to return to colours.

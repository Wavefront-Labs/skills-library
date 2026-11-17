---
id: creative-arts.visual-art.procreate.transform-warp-and-liquify
name: transform-warp-and-liquify
category: creative-arts
field: visual-art
product: procreate
tags: [visual-art, procreate, liquify, procreate-transform, warp, distort, transform-tool, mesh-warp, interpolation]
level: practitioner
status: draft
description: "Move, scale, distort, warp and liquify in Procreate: Transform modes, snapping, interpolation, and Liquify tools, with notes on quality loss."
sources: ["https://procreate.com/handbook"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Transform, warp and liquify in Procreate

**Goal:** reshape a layer or selection without repeatedly degrading it.

## Transform (arrow icon)
- Modes at the bottom of the screen: **Uniform** (keeps proportions), **Freeform**, **Distort** (move corners for perspective), **Warp** (bend with a grid or mesh).
- **Snapping** and **Magnetics** help align to canvas edges and centre.
- **Interpolation** (bottom bar, with options such as nearest neighbour, bilinear and bicubic) affects how pixels resample; use nearest neighbour for pixel art, bicubic for smooth paintings.
- Commit with the arrow icon again; repeated transforms resample the pixels each time, so make one combined move where possible.

## Liquify (Adjustments > Liquify)
- Tools: Push, Twirl, Pinch, Expand, Crystals, Edge, Reconstruct (names per the Handbook).
- Sliders for Size, Pressure, Distortion and Momentum set the brush behaviour; apply on the current layer or active selection.
- Use Reconstruct to undo part of a Liquify smear selectively, leaving other areas.

## Workflow for painted figures
1. Duplicate the layer, hide the original.
2. Use Liquify at low pressure to fix proportions (jaw, limbs), then Transform for global scale.
3. Merge or flatten only after checking edges and any line weight changes.

## Gotchas
- Large scale-ups blur; paint or sharpen afterwards.
- Warp on a layer with text or vector-like crispness will soften.
- Liquify on a flattened image also drags the background; isolate subjects on layers first.

## Verify
- [ ] Edges look clean after a transform with no stair-stepping or blur.
- [ ] An untouched duplicate remains for comparison.

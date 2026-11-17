---
id: creative-arts.graphic-design.adobe-illustrator.blob-brush-and-eraser
name: blob-brush-and-eraser
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, ai-brushes, blob-brush, eraser-tool, pressure-sensitivity, merge-only-with-selection]
level: practitioner
status: draft
description: "Draw filled vector shapes like ink with the Blob Brush and refine them with the Eraser: pressure settings, merge behaviour, fidelity and cleanup."
sources:
  - https://helpx.adobe.com/illustrator/using/painting-brushes.html
  - https://helpx.adobe.com/illustrator/using/erasing-artwork.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Blob Brush and Eraser drawing

**Goal:** paint-like drawing that produces clean filled paths (not stroked paths).

## Blob Brush (Shift+B)
- Every stroke becomes a **filled compound shape**; overlapping strokes of the same colour merge.
- Double-click the tool for options:
  - **Keep Selected** / **Merge Only with Selection** - control what merges.
  - **Fidelity**: Accurate (more anchors) to Smooth. Smooth for inking.
  - Size, Angle, Roundness with **Pressure** / Tilt variation for a tablet.
- `[` and `]` change size.
- Different fill colour = separate shape (no merge).

## Eraser (Shift+E)
- Removes from any unlocked filled shapes under the cursor; Alt/Opt-drag erases a rectangle.
- Double-click for size/pressure. Select objects first to erase only them.

## Clean-up
- Object > Path > **Simplify** to reduce anchors; Smooth tool for wobbly edges.
- Shape Builder to merge or split areas.
- Convert Brush strokes made with the Paintbrush to Blob-style fills via Object > Expand Appearance.

## Gotchas
- Blob Brush picks up the current stroke colour as fill when no fill is set - check swatches.
- Merging with existing art requires same fill and no stroke/appearance on that art.

## Verify
- [ ] Outline view (Ctrl/Cmd+Y) shows filled shapes, not overlapping strokes.
- [ ] Anchor count reasonable after Simplify.

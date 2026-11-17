---
id: creative-arts.visual-art.procreate.reference-layer-and-colordrop-fill
name: reference-layer-and-colordrop-fill
category: creative-arts
field: visual-art
product: procreate
tags: [visual-art, procreate, reference-layer, colordrop, colour-drop, procreate-fill, flat-colours, line-art-fill, threshold]
level: practitioner
status: draft
description: "Flat-colour line art fast in Procreate with a Reference layer and ColorDrop, setting the fill threshold and closing gaps so fills do not leak."
sources: ["https://procreate.com/handbook"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reference layer and ColorDrop fill

**Goal:** fill line art on separate layers without painting inside the lines by hand.

## Steps
1. Put your line art on its own layer. Add a new empty layer under it for colour.
2. On the line art layer, open the layer options (tap the layer) and choose **Reference**. The layer is now the boundary Procreate reads when filling, even though you fill another layer.
3. Select the empty colour layer. Drag a colour from the Color disc (or swatch) into a closed area. That is **ColorDrop**.
4. Without lifting, hold still and drag left or right to change the **threshold**. Higher thresholds fill more tolerantly across soft edges and anti-aliased gaps; lower is stricter. Lift to commit.
5. If the fill leaks into neighbouring areas, close the gap on the line art or lower the threshold; re-do the fill.
6. For leftover edge pixels, use a layer set to **Alpha Lock**, or lower the threshold to avoid halos; see `creative-arts.visual-art.procreate.procreate-masks-clipping-and-alpha-lock`.

## Gotchas
- Only one layer is the Reference layer per canvas at a time; Reference reads its content, not the layer you drop on.
- ColorDrop respects selections: a selection limits where it fills.
- Anti-aliased line art leaves a light fringe between fill and lines; extend fills under the line art to hide it.

## Verify
- [ ] Fill reaches the line art edge without gaps or leaks.
- [ ] Colour sits on its own layer so it can be changed later.

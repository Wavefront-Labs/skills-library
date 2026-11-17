---
id: creative-arts.graphic-design.adobe-photoshop.pen-paths-for-product-cutouts
name: pen-paths-for-product-cutouts
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-selections, photoshop-pen-path, clipping-path-product, clipping-path, paths-panel, e-commerce-cutout, packshot, vector-mask-from-path, path-to-selection]
level: practitioner
status: draft
description: "Cut out hard-edged products in Photoshop with pen paths: placement inside the edge, saved paths, vector or pixel masks, and clipping paths for suppliers."
sources:
  - https://helpx.adobe.com/photoshop/using/drawing-pen-tools.html
  - https://helpx.adobe.com/photoshop/using/managing-paths.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pen paths for product cut-outs

**Goal:** perfectly smooth, crisp product edges that AI selection tools cannot match.

## Draw the path
1. Pen tool (P), mode **Path** in the Options bar. Zoom to 200-300%.
2. Place anchor points **1-2 px inside** the product edge so no background fringe survives.
3. Click-drag for curves; points at the extremes of curves, few points overall (same rules as
   Illustrator: see the pen tool skill). Alt/Option-click the last point to break the handle at corners.
4. Close the path; subtract holes (handle loops, gaps) with **Exclude Overlapping Shapes** or
   drawing additional subpaths with Subtract Front Shape.
5. **Save the path** in the Paths panel (double-click "Work Path" and name it) - work paths are
   overwritten by the next path.

## Use the path
- **Vector mask:** with the path selected, Layer > Vector Mask > Current Path (or Ctrl/Cmd+click
  the mask button). Crisp at any size, editable. Feather in mask Properties (0.3-0.5 px) to match
  the photo's natural edge softness.
- **Pixel mask:** Ctrl/Cmd+Enter loads the path as a selection, then add a layer mask. Feather 0.5 px.
- Combine: path for the body, Select and Mask for a soft element (a fluffy toy's fur, steam).

## Clipping paths for print/e-commerce suppliers
Some workflows (retail catalogues, retouching studios, Amazon-style suppliers) require the path
inside a JPEG/TIFF: Paths panel menu > **Clipping Path**, choose the path, Flatness blank. Save as
TIFF or JPEG; InDesign can use it via Object > Clipping Path > Options (Type: Photoshop Path).

## Shadows and reflections
Keep the original shadow on a separate layer (Multiply) or rebuild it (see contact shadow skill) -
pure cut-outs floating on white look fake.

## Gotchas
- Path drawn exactly on the edge picks up a 1 px halo of background.
- Transparent products (glass): path the outline, then keep the background inside with a
  separate mask at partial opacity, or reshoot on white.

## Verify
- [ ] Named path saved in the Paths panel.
- [ ] Cut-out on black and white at 200%: no fringe, no lumpy curves.
- [ ] Clipping path set if the client spec requires it.

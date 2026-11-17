---
id: creative-arts.graphic-design.adobe-photoshop.vector-masks
name: vector-masks
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-masking, layer-mask, vector-mask, shape-masks, resolution-independent, combine-masks, rasterize-vector-mask]
level: practitioner
status: draft
description: "Use Photoshop vector masks for crisp, resolution-independent edges: create from paths, edit with path tools, combine with pixel masks, feather."
sources:
  - https://helpx.adobe.com/photoshop/using/masking-layers.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Vector masks

**Goal:** mask edges that stay perfectly sharp at any size and remain editable as paths.

## Create
- Draw a path with the Pen or a Shape tool in **Path** mode, then Layer > Vector Mask >
  **Current Path**.
- Or **Ctrl/Cmd+click the Add Mask button**: adds a vector mask (if a pixel mask already
  exists, a plain click adds the vector mask as the second mask).
- Layer > Vector Mask > Reveal All / Hide All gives an empty one to draw into.

## Edit
- Click the vector mask thumbnail; edit with Direct Selection (A) and Path Selection tools;
  add shapes with Pen/Shape tools using path operations (Combine, Subtract, Intersect, Exclude).
- Ctrl/Cmd+T transforms the mask path only.
- Properties panel: **Density** and **Feather** (non-destructive softening, e.g. 0.5 px to match photo softness).
- Unlink (click the chain) to move the layer content independently of the mask.

## Pixel mask + vector mask together
A layer can have both: e.g. vector mask for the hard silhouette of a product, pixel mask
painted for a soft shadow fade. Both apply (intersection of visible areas).

## When to use which
| | Vector mask | Pixel (layer) mask |
|---|---|---|
| Edges | crisp, geometric, product outlines, UI shapes | soft, hair, gradients, painted |
| Scaling | lossless at any size | resampled |
| Editing | path tools | brushes, filters, adjustments |
Rasterise (Layer > Rasterize > Vector Mask) when you need to paint into it - one-way.

## Gotchas
- Vector masks export as vector in Photoshop PDF but raster in JPEG/PNG (fine).
- A vector mask's hard edge can look artificially sharp against a photo; add feather 0.3-1 px.
- Shape layers already are fill layers with vector masks; to mask an image with a shape, clip
  it to the shape layer instead (see clipping masks skill).

## Verify
- [ ] Edges crisp at 200%+ zoom and after scaling the layer up.
- [ ] Feather matches the softness of the rest of the image.

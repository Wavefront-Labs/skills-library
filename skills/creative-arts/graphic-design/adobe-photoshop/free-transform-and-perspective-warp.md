---
id: creative-arts.graphic-design.adobe-photoshop.free-transform-and-perspective-warp
name: free-transform-and-perspective-warp
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-transform, free-transform, perspective-warp, warp, distort, skew, interpolation, smart-objects, non-destructive]
level: practitioner
status: draft
description: "Scale, rotate, distort, warp and perspective-warp layers in Photoshop without degrading them: smart objects first, correct modifier keys, interpolation and Perspective Warp planes."
sources:
  - https://helpx.adobe.com/photoshop/using/transforming-objects.html
  - https://helpx.adobe.com/photoshop/using/perspective-warp.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Free transform and perspective warp

**Goal:** reshape elements as many times as needed without the pixels going soft.

## Convert to a smart object first
Right-click the layer > Convert to Smart Object. Every transform on a smart object is
re-calculated from the original pixels, so scaling down then up again loses nothing.
Transforms on a normal pixel layer resample each time and blur cumulatively.

## Free Transform (Ctrl/Cmd+T)
- Since Photoshop 2019, dragging a corner scales **proportionally** by default; hold Shift
  to scale non-proportionally (toggle the link icon in the Options bar to change this).
- **Alt/Option** scales from the centre (or the reference point).
- **Ctrl/Cmd+drag a corner** = distort that corner only. Ctrl/Cmd+Shift+drag a side = skew.
- Right-click inside for Rotate 90, Flip, Perspective, Warp.
- Type exact values in the Options bar (W/H %, angle) for repeatable work.
- **Interpolation** (Options bar): Bicubic Automatic is right for most; Nearest Neighbor for
  pixel art or hard-edged UI icons.
- Repeat last transform on another layer: Ctrl/Cmd+Shift+T. Duplicate and repeat:
  Ctrl/Cmd+Alt/Option+Shift+T (step-and-repeat patterns).

## Warp (Edit > Transform > Warp)
Use presets (Arc, Flag, Bulge) or the custom grid (split 3x3, 4x4, 5x5 in the Options bar)
to wrap a label onto a curved bottle or fold a flag. Add split lines where the surface
bends. On smart objects the warp stays editable.

## Perspective Warp (Edit > Perspective Warp)
For changing the perspective of an object that already has perspective (a building, a box).
1. **Layout mode:** draw quads that match each plane of the object (e.g. two walls of a
   building); edges snap together when shared.
2. **Warp mode:** drag the pins; Shift+click an edge to keep it straight; use the
   automatic straighten buttons for verticals/horizontals.
3. Commit; on a smart object it becomes a smart filter you can re-open.

## Gotchas
- Transforming a layer with a layer mask: the mask moves with it only if linked (chain icon).
- Upscaling a raster source beyond 100% softens it no matter what; use vector or a larger source.
- Perspective Warp needs GPU enabled (Preferences > Performance).

## Verify
- [ ] Layer is a smart object; reopening the transform shows the original handles.
- [ ] Edges sharp at 100% after transforms; verticals in perspective work are vertical.

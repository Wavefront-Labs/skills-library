---
id: creative-arts.graphic-design.adobe-photoshop.canvas-size-and-crop-tool
name: canvas-size-and-crop-tool
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-document-setup, canvas-size, perspective-crop, crop-tool, content-aware-crop, straighten, delete-cropped-pixels, aspect-ratio-crop]
level: practitioner
status: draft
description: "Change canvas and crop in Photoshop correctly: Canvas Size anchors, crop ratios, non-destructive cropping, straightening, content-aware crop and Perspective Crop."
sources:
  - https://helpx.adobe.com/photoshop/using/crop-straighten-photos.html
  - https://helpx.adobe.com/photoshop/using/adjust-perspective-crop-tool.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Canvas size and the crop tools

**Goal:** the canvas you need, cropped to the exact ratio, without throwing away pixels you may want back.

## Canvas Size (Image > Canvas Size, Alt+Ctrl+C / Opt+Cmd+C)
- Adds or removes canvas without scaling content. Tick **Relative** and enter the amount to add
  (e.g. 6 mm width and height for 3 mm bleed each side).
- **Anchor** grid chooses which side grows. Canvas extension colour applies to Background layers;
  normal layers get transparency.
- Fill new space afterwards with Content-Aware Fill or Generative Expand if needed.

## Crop tool (C)
- Options bar: ratio preset (1:1, 4:5, 16:9) or **W x H x Resolution** (crops and resamples to an
  exact size in one go - useful for fixed-size deliverables).
- **Delete Cropped Pixels: OFF** keeps the cropped area hidden, so you can re-crop later
  (works on layers, not on a locked Background). Turn ON only for the final flattened delivery.
- **Straighten:** click the level icon and draw along the horizon; or drag outside the crop box to rotate.
- **Content-Aware** (Options bar): fills the transparent corners created by rotating or by
  extending the crop outside the image. Check fills for repetition.
- Overlay (O to cycle): rule of thirds, golden ratio, grid. Shift+O flips golden spiral.
- Enter commits, Esc cancels. X swaps portrait/landscape.

## Perspective Crop tool (under Crop)
For photographing artwork, signs or documents at an angle: click the four corners of the
rectangle that should be square, adjust, commit - it crops and corrects perspective. Enter W/H
to output a known aspect (e.g. the painting's real proportions).

## Gotchas
- Cropping a document with smart objects does not crop their contents - fine and non-destructive.
- W x H x Resolution crop resamples: do it once, from the original.
- Crop on artboard documents crops artboards differently - use the Artboard tool to resize instead.

## Verify
- [ ] Final canvas matches the required ratio/size (Image Size check).
- [ ] Horizon straight; no unfilled transparent corners.
- [ ] Working file keeps cropped pixels (Delete Cropped Pixels off) until final.

---
id: creative-arts.graphic-design.adobe-illustrator.clipping-masks-and-draw-inside
name: clipping-masks-and-draw-inside
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, illustrator-clipping-mask, clipping-mask, draw-inside, clip-group, layer-clipping-mask, isolation-mode, compound-path]
level: practitioner
status: draft
description: "Hide artwork outside a shape in Illustrator with clipping masks and Draw Inside: object and layer masks, compound clipping paths, editing in isolation and clean release."
sources:
  - https://helpx.adobe.com/illustrator/using/clipping-masks.html
  - https://helpx.adobe.com/illustrator/using/drawing-modes.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Clipping masks and Draw Inside

**Goal:** artwork visible only inside a shape (image in a circle, pattern in type, illustration cropped
to a frame) without destroying the hidden parts.

## Object clipping mask
1. Place the clipping shape on **top** of the artwork to be clipped (it must be a single path, compound
   path or live type).
2. Select the shape and the artwork, Object > Clipping Mask > **Make** (Ctrl/Cmd+7).
3. The result is a **clip group**; the clipping path loses its fill and stroke (re-add them in the
   Appearance panel after targeting the clip path, or put a copy on top for a stroke).
4. Edit: double-click into isolation mode, or Object > Clipping Mask > **Edit Mask/Contents**.
5. Release: Object > Clipping Mask > **Release** (Ctrl/Cmd+Alt/Option+7).

## Several shapes as one mask
- Combine them first: Object > **Compound Path > Make** (Ctrl/Cmd+8). Otherwise only the top shape clips.
- Type as mask: live text can be the clipping path directly; outline only if needed for output.

## Layer clipping mask
- Layers panel: select the layer, then click **Make/Release Clipping Mask**. The top object of the layer
  clips everything in that layer. Useful for cropping an entire illustration to an artboard-sized
  rectangle while still drawing freely.

## Draw Inside mode
- Select one shape, press **Shift+D** to cycle to Draw Inside (or the drawing modes button at the bottom
  of the toolbar). New strokes, pasted objects (Edit > Paste Inside... behaviour) and placed images go
  inside the shape, creating a clip group automatically. Shift+D back to Draw Normal when done.
- Ideal for brush shading inside a character shape or texturing a flat area.

## Gotchas
- Hidden artwork still exists: large hidden images keep file size; crop images in Photoshop or use
  Object > **Crop Image** for embedded/linked rasters when the full image is not needed.
- Clip groups confuse Pathfinder and Shape Builder; release or expand first.
- Masked objects can still affect bounds in some exports (older SVG, asset export); check bounding boxes.

## Verify
- [ ] Only the intended area shows; hidden art is recoverable by Release.
- [ ] Exported files have correct bounds and no unexpected hidden data.

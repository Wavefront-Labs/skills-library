---
id: creative-arts.visual-art.procreate.procreate-masks-clipping-and-alpha-lock
name: procreate-masks-clipping-and-alpha-lock
category: creative-arts
field: visual-art
product: procreate
tags: [visual-art, procreate, procreate-layers, procreate-masks, layer-mask, clipping-mask, alpha-lock, layer-options, non-destructive, ipad]
level: intro
status: draft
description: "Use Procreate's three masking tools: Alpha Lock (two-finger swipe), Clipping Mask and Layer Mask, which to use when, and how to keep colours and shading editable."
sources: ["https://procreate.com/handbook/procreate/layers/layers-mask/", "https://procreate.com/handbook/procreate/layers/layers-options/", "https://procreate.com/handbook"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Procreate masks, clipping and alpha lock

**Goal:** paint inside shapes and hide/reveal parts of layers without erasing
(Procreate Handbook, Layers: Mask and Layer options).

## Alpha Lock
- Locks the layer's transparent pixels: you can only paint where pixels already exist.
- Toggle: **two-finger swipe right** on the layer in the Layers panel, or tap the
  layer > Alpha Lock. A checkerboard appears in the thumbnail.
- Use: recolouring a flat shape, adding texture to a filled area.
- Destructive: paint replaces pixels on that layer.

## Clipping Mask
- A layer clipped to the layer below shows only where the lower layer has pixels.
- Tap the upper layer > **Clipping Mask**; multiple clipped layers can stack on one base.
- Use: shading, highlights and textures over flats, each on its own editable layer.
- Non-destructive: the base layer remains untouched; delete or change opacity freely.

## Layer Mask
- Tap a layer > **Mask**: adds a linked greyscale mask above it.
  Paint **black** to hide, **white** to reveal, greys for partial transparency.
- Use: hiding part of a layer or soft fades while keeping all pixels recoverable.

## Choosing
| Task | Tool |
|------|------|
| Quick recolour of a flat | Alpha Lock |
| Shading and lighting on separate layers | Clipping Mask |
| Hide/fade part of a layer reversibly | Layer Mask |

## Gotchas
- Painting on the wrong thumbnail (mask vs layer): check which is highlighted.
- Merging a clipped layer down bakes it into the base.
- Layer count limits on large canvases (see canvas setup skill): clipping layers
  count toward the limit.

## Verify
- [ ] Shading layers clipped, not painted directly on flats.
- [ ] Masks used instead of erasing where change is likely.

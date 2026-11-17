---
id: creative-arts.design-for-form-and-experience.figma.image-fills-and-masks-in-figma
name: image-fills-and-masks-in-figma
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [image-fills, masks, figma-masks, image-adjustments, crop-image, fill-modes, mask-types, figma]
level: practitioner
status: docs-checked
description: "Use image fills and masks in Figma: fill, fit, crop and tile modes, image adjustment sliders, mask groups and the alpha, vector and luminance mask types."
sources:
  - https://help.figma.com/hc/en-us/articles/360041098433-Adjust-the-properties-of-an-image
  - https://help.figma.com/hc/en-us/articles/360040450253-Masks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Image fills and masks

## Image fills
- Fill modes: **Fill** (covers the whole layer, may clip), **Fit** (whole image stays visible, layer may not be fully covered), **Crop** (choose which part of the image shows) and **Tile** (repeats the image as a pattern).
- **Adjustments:** Exposure, Contrast, Saturation, Temperature, Tint, Highlights and Shadows. They are non-destructive and can be changed or reversed at any time.
- For responsive cards, pick the fill mode per image slot and check it at the sizes the layout will take (`creative-arts.design-for-form-and-experience.figma.auto-layout-wrap-min-max-and-grid`).

## Masks
- Select the layers and choose **Use as mask** (More options menu or right sidebar; Windows `Ctrl Alt M`, Mac `Control Command M`). Figma makes a mask group from the selected layers.
- The mask is the layer positioned **below** the layers it masks on the z-axis. It affects the sibling layers above it until another mask, the parent frame or group, or a frame or component with clip content enabled.
- Any layer can be a mask: vectors, text, images with transparency, groups.
- **Mask types** (dropdown in the Mask section of the right sidebar; default Alpha): **Alpha** (opacity decides visibility; blurs, shadows and semi-transparent fills work), **Vector** (ignores opacity; any area above 0% opacity defines the outline and becomes fully opaque), **Luminance** (brighter areas reveal more; black `#000000` reveals nothing).
- **Release a mask:** select it and use the sidebar icon, right-click **Remove mask**, or press the same shortcut. Hidden portions reappear; masks are non-destructive.
- Masks and masked layers are siblings, so they move and resize independently. Turn on **View > Mask outlines** to see them outlined in green.

## Verify
- [ ] Fill mode chosen for each image slot.
- [ ] Mask type matches the effect wanted (soft edge: Alpha; hard outline: Vector; brightness: Luminance).

## Checked
2026-11-01. Confirmed against the Adjust the properties of an image and Masks Help Center articles: fill modes, adjustment slider names, non-destructive adjustments, Use as mask shortcut, mask placement below masked layers, mask types, release methods, mask outlines. Removed (not stated by those pages): 4096 px resolution limit, Replace image and placeholder components, Release mask by double-click, "top shape is the mask" (the page says below), reveal and frosted-glass recipes, auto layout and file-size claims, the alt-text claim and two unread cited pages.
Method: documentation only; no commands were run.

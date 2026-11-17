---
id: creative-arts.animation.blender.comp-scale-transform-crop
name: comp-scale-transform-crop
category: creative-arts
field: animation
product: blender
tags: [blender, compositor, scale-transform-nodes, scale-node, transform-node, crop-node, translate-node]
level: practitioner
status: docs-checked
description: "Fit plates to the frame in the compositor: Scale Space modes and Frame Type, Transform and Translate sampling, Extension, Crop with Alpha Crop, and avoiding repeated resampling."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/transform/scale.html
  - https://docs.blender.org/manual/en/latest/compositing/types/transform/transform.html
  - https://docs.blender.org/manual/en/latest/compositing/types/transform/translate.html
  - https://docs.blender.org/manual/en/latest/compositing/types/transform/crop.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# comp-scale-transform-crop

Goal: fit plates and elements to the render frame without losing sharpness.

## Scale node (Transform category)

**Space**:
- **Relative**: percentage values relative to the input image (X 0.5, Y 0.5 gives half width and height).
- **Absolute**: size in pixels.
- **Scene Size**: sizes the image to the final render resolution, so rendering at 1080p with a 50 percent render percentage gives a 1080p image with the content scaled down 50 percent and the rest alpha.
- **Render Size**: uses the image dimensions set in the Render panel, with **Frame Type**: **Stretch** (distorts to fit), **Fit** (bigger axis fits) or **Crop** (cuts to the render aspect ratio). Use it for plates whose resolution differs from the render.

X and Y are only available for Relative and Absolute.

## Transform and Translate

- **Transform**: X, Y, **Angle** (positive is counter-clockwise) and **Scale** in one node, combining Scale, Translate and Rotate.
- **Translate**: X and Y offset; can also add a 2D camera shake.
- Both have sampling options: filter or **Interpolation** (Nearest, Bilinear, Bicubic, Anisotropic) and **Extension X/Y** (Clip fills with transparency, Extend repeats the border pixel, Repeat tiles the image). Nearest suits pixel art; Bicubic suits photographic images.
- A separate **Rotate** node exists.

## Crop node

Inputs: **X**, **Y** (lower-left corner of the region), **Width**, **Height**, and **Alpha Crop**. With Alpha Crop on, the image keeps its resolution and the outside becomes transparent; off, the image is resized to the region. With the node active and the Active Node gizmo enabled, the region can be adjusted interactively.

## Gotchas

- Every resample can soften the image. Prefer one Transform node over chained Scale, Rotate and Translate.
- To combine two images of different sizes, scale the second to match the first; most nodes output at the size of their top image input.

## Verify

Place a resolution chart through the transform and compare against the original at 100 percent. Edges should stay sharp enough for the delivery.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch).
Confirmed: Scale Space modes and Frame Types, Scene Size example, Transform X/Y/Angle/Scale, Translate, sampling Interpolation and Extension options, Crop X/Y/Width/Height and Alpha Crop. Removed the Relative/Wrapping options of Translate and the Crop Relative/Up/Down options, which 5.2 does not have, and the 4.2+ domain remark.
Method: documentation only; no commands were run.

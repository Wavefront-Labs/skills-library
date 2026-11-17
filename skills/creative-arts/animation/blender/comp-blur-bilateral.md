---
id: creative-arts.animation.blender.comp-blur-bilateral
name: comp-blur-bilateral
category: creative-arts
field: animation
product: blender
tags: [blender, blur-node, bilateral-blur, blur-types, compositor]
level: practitioner
status: verified
description: "Choose the right compositor blur: Blur node types, Size input, Extend Bounds and Separable, and Bilateral Blur with a Determinator input for edge-preserving smoothing."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/filter/blur/blur.html
  - https://docs.blender.org/manual/en/latest/compositing/types/filter/blur/bilateral_blur.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---
# comp-blur-bilateral

Goal: blur that looks right and does not leak across edges when it should not.

## Blur node (Filter category)

Inputs: **Image**, **Size** (optional; multiplied with the X and Y blur radius, and accepts a value image to control the radius with a mask, best mapped between 0 and 1) and **Type**.
- **Type**: Flat (uniform), Tent (linear falloff, preserves highs and lows better), Quadratic (similar to Gaussian, a little faster, slightly worse looking), Cubic and Mitch (preserve highs but give an almost out-of-focus blur while smoothing sharp edges), Gaussian (best looking, slowest), Fast Gaussian (an approximation of Gaussian), Catmull-Rom (keeps sharp contrast edges crisp).
- **Extend Bounds**: lets the blurred image extend past its original dimensions.
- **Separable**: faster approximation that blurs horizontally and vertically independently.
- Python: `filter_type` is `FLAT`, `TENT`, `QUAD`, `CUBIC`, `GAUSS` (default), `FAST_GAUSS`, `CATROM` or `MITCH`. In 4.5.14 the node inputs are Image, Size (a 2D vector), Extend Bounds and Separable (on by default).

## Bilateral Blur node (Filter category)

A high-quality adaptive blur that keeps sharp edges. Inputs:
- **Image**: with only this connected, edges are taken from the image itself.
- **Determinator**: if connected, defines the edges and borders for the blur. Useful when the source is too noisy but normals combined with the Z-buffer still give exact object borders.
- **Size**: blur size in pixels.
- **Threshold** (default 0.1): pixels join the blur area when the average difference between their determinator and the centre pixel's is below this value.
Uses named in the manual: smoothing noisy render passes (for example ray-traced ambient occlusion), blurry reflections and refractions, soft shadows and non-photorealistic effects.

## Choosing

| Need | Use |
|---|---|
| Soften a matte | Blur, Gaussian, small |
| Glow or haze layer | Fast Gaussian, large |
| Depth-based blur | Defocus (see comp-defocus-bokeh), or a mask into Blur Size |
| Edge-preserving clean | Bilateral Blur |

## Verify

Blur a high-contrast edge and zoom in: the transition should be smooth with no stepping, and the Bilateral version should keep object outlines.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch).
Confirmed: Blur node Size input, Type list and descriptions, Extend Bounds and Separable; Bilateral Blur Image, Determinator, Size and Threshold inputs and uses. Removed Relative size, Variable Size, Bokeh and Gamma options, the Iterations, Color Sigma and Space Sigma settings, performance claims and the premultiplied-blur claim, none of which the 5.2 pages state.
Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): CompositorNodeBlur sockets Image, Size, Extend Bounds, Separable and filter_type items (default GAUSS); CompositorNodeBilateralblur sockets Image, Determinator, Size, Threshold 0.1. The 4.5.14 nodes still carry legacy properties (Variable Size, Relative, Bokeh, Gamma, Iterations, Color Sigma, Space Sigma) that the 5.2 pages no longer describe. Not run (confirmed from the manual only): the descriptions of each filter type and the Bilateral Blur use cases.

Method: manual text and shipped UI scripts confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.

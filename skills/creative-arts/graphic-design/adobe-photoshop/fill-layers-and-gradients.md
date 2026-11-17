---
id: creative-arts.graphic-design.adobe-photoshop.fill-layers-and-gradients
name: fill-layers-and-gradients
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-layers, fill-layers, gradient-fill-layer, solid-color-layer, pattern-fill, live-gradients, dither, banding, gradient-tool]
level: practitioner
status: draft
description: "Use Photoshop fill layers (solid, gradient, pattern) and live gradients non-destructively, with masks and dithering to prevent banding."
sources:
  - https://helpx.adobe.com/photoshop/using/gradient-fills.html
  - https://helpx.adobe.com/photoshop/using/fill-stroke-selections-layers.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fill layers and gradients

**Goal:** backgrounds, overlays and colour washes that stay editable - change colour in two clicks.

## Fill layers (Layer > New Fill Layer, or the half-moon button)
- **Solid Color:** a colour with a built-in mask. Double-click the thumbnail to change colour.
  Use for backgrounds, colour blocks, and colour overlays clipped to objects (with a blend mode).
- **Gradient:** editable gradient with style (linear, radial, angle, reflected, diamond), angle,
  scale, Reverse, **Dither** and Align with Layer. Drag on canvas while the dialog is open to move it.
- **Pattern:** tiled pattern with scale and angle; link with layer.
With an active selection, the fill layer's mask takes its shape.

## Live gradients (Photoshop 2023+)
The Gradient tool (G) now creates an editable gradient fill layer with on-canvas stops: drag
handles, click to add stops, set stop colour and opacity in Properties. Switch to **Classic
gradient** in the Options bar for the old pixel-painting behaviour (e.g. painting gradients into masks).

## Masks and fades
- Paint the fill layer's mask with a black-to-white gradient to fade a colour wash.
- Gradient map adjustment (different tool) remaps tones to colours - for duotone looks.

## Banding
Smooth gradients across large areas band (visible steps), especially in 8-bit, on dark colours,
and after JPEG compression.
- Tick **Dither** on gradient fills.
- Work in 16-bit for large subtle gradients, then convert to 8-bit (Photoshop dithers on conversion).
- Add 1-2% noise (Filter > Noise > Add Noise, Gaussian, Monochromatic) on a merged copy for print or web.
- Check banding at 100% on a good screen, and on the final export.

## Gotchas
- Gradients between complementary colours pass through grey ("dead zone") - add a middle stop
  or choose the interpolation method (Perceptual/Linear/Classic in newer versions).
- Fill layers in CMYK documents: pick colours with the printer's gamut in mind.

## Verify
- [ ] Backgrounds are fill layers, not painted pixels.
- [ ] No visible banding in the exported file.

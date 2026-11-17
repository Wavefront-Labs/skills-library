---
id: creative-arts.animation.blender.comp-filter-sharpen
name: comp-filter-sharpen
category: creative-arts
field: animation
product: blender
tags: [blender, filter-sharpen, soften, edge-detect, sharpen, compositor]
level: practitioner
status: docs-checked
description: "Use the compositor Filter node: Soften, Box and Diamond Sharpen, Laplace, Sobel, Prewitt, Kirsch and Shadow, with Factor masks, and sharpening limits."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/filter/filter.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# comp-filter-sharpen

Goal: small convolution effects: sharpening, softening, edge mattes.

## Node (Filter > Filter)

Inputs: **Image**, **Factor** (amount of influence), **Type**:
- **Soften**: slightly blurs the image.
- **Box Sharpen**: increases contrast, especially at edges.
- **Diamond Sharpen**: less aggressive than Box Sharpen, with fewer sharpening artefacts.
- **Laplace**: edge highlighting, susceptible to highlighting visual noise.
- **Sobel**: creates a negative image that highlights edges.
- **Prewitt**: similar results to Sobel.
- **Kirsch**: better blending than Sobel or Prewitt when approaching an edge.
- **Shadow**: relief or emboss effect, darkening outside edges.

Connect a matte to Factor to apply locally.

## Uses

- Final sharpening: Box or Diamond Sharpen at a low factor, after scaling to the output size.
- Edge mattes: an edge filter on a depth or normal pass, then threshold the result (Map Range or Color Ramp), for outlines or edge-only grading.
- Soften: take the CG edge off sharp renders to match softer plates.

## Gotchas

- Sharpening raises noise. Sharpen after denoising and mask out smooth areas.
- Box Sharpen can show halos at high-contrast edges; lower the factor or use Diamond Sharpen.
- Kernels work on pixels, so judge the result at 100 percent size rather than at reduced preview resolution.

## Verify

Compare a 100 percent crop with and without the filter. Detail should look crisper without bright or dark halos at edges.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch).
Confirmed: the Filter node has Image, Factor and Type inputs and the nine types with their described behaviour. Removed the unconfirmed 0.1 to 0.3 factor and the preview-resolution strength claim.
Method: documentation only; no commands were run.

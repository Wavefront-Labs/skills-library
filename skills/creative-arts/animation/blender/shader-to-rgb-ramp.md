---
id: creative-arts.animation.blender.shader-to-rgb-ramp
name: shader-to-rgb-ramp
category: creative-arts
field: animation
product: blender
tags: [blender, shader-to-rgb-ramp, color-ramp-banding, shader-to-rgb, cel-shading, eevee, npr]
level: practitioner
status: docs-checked
description: "Build toon light bands in EEVEE with Shader to RGB into a Constant Color Ramp: band count, stop placement, normalising light, tinting and keeping bands stable."
sources:
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/color/shader_to_rgb.html
  - https://docs.blender.org/manual/en/5.2/render/layers/passes.html
  - https://docs.blender.org/manual/en/5.2/interface/controls/templates/color_ramp.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# shader-to-rgb-ramp

Goal: crisp two- or three-tone shading driven by the real scene lights.

## Core graph (EEVEE)

```
Diffuse BSDF (Color white) -> Shader to RGB -> Color Ramp (Constant) -> Mix (Multiply, Fac 1) A
                                                    Base colour / texture -> Mix B -> Emission (Strength 1) -> Output
```
- The Shader to RGB node is EEVEE only. Its Shader input takes any BSDF or Emission; outputs are **Color** (surface colour from BSDFs and lighting) and **Alpha** (from Transparent BSDFs).
- Feed a **white** Diffuse BSDF so the ramp reads light intensity only; apply the albedo afterwards by multiplying. This keeps one ramp for all colours.
- Output through Emission (or directly into the Material Output Surface) so the result is not lit a second time.

## Band setup

- Color Ramp *Interpolation: Constant* for hard bands; Ease or Linear with stops close together for soft edges.
- Two tones: a shadow stop and a light stop. Three tones: add a mid stop and a highlight stop.
- For hue-shifted shadows put coloured stops on the ramp instead of grey, then Multiply.

## Normalise the light

The ramp position depends on light strength, so different light powers give different bands. Keep a fixed key light, or insert Map Range or Math Divide between Shader to RGB and the ramp to rescale. With coloured lights put an RGB to BW node before the ramp.

## Gotchas

- The node breaks the physically based pipeline: results are unpredictable with ambient occlusion, contact shadows, soft shadows and screen space refraction. Effects that need multiple samples to converge may not give a smooth result from noisy input.
- Any BSDF upstream of Shader to RGB is invisible to Screen Space Reflection, Subsurface Scattering, and the Alpha Clip and Alpha Hashed blend modes.
- It does not give expected results in render passes; it only works correctly in the Combined pass.
- Multiple lights add up: rim and fill lights can push areas into the highlight band.

## Verify

Rotate the key light: the terminator moves as one crisp edge; swap base colours and the band positions stay identical.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch, docs.blender.org manual en/5.2). Confirmed against color/shader_to_rgb (EEVEE Only, inputs, outputs, PBR and effect limitations, upstream BSDFs invisible to SSR, SSS and Alpha Clip/Hashed) and the render passes page (only correct in the Combined pass). Removed the claims that Cycles renders it black, that it forces blended evaluation, the View Transform Standard advice, shadow bias and jitter settings, light-linking advice and the numeric stop positions.

Method: documentation only; no commands were run.

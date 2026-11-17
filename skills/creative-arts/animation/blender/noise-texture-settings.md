---
id: creative-arts.animation.blender.noise-texture-settings
name: noise-texture-settings
category: creative-arts
field: animation
product: blender
tags: [blender, procedural-texturing, noise-texture, noise-texture-settings, noise-detail, noise-roughness, lacunarity]
level: practitioner
status: docs-checked
description: "Control the Blender Noise Texture: dimensions, scale, detail, roughness, lacunarity, distortion, normalize and W animation for organic variation."
sources:
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/textures/noise.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# noise-texture-settings

## Inputs

- **Dimensions**: 1D (uses W), 2D and 3D (use Vector; 2D ignores Z), 4D (Vector plus W as the fourth dimension). Higher dimensions cost more render time.
- **Scale**: scale of the base octave. **Detail**: number of octaves; a fractional part blends between octaves (2.5 is a 50% blend of 2 and 3).
- **Roughness**: blends between smoother noise and rougher noise with sharper peaks.
- **Lacunarity**: difference in scale between consecutive octaves; larger values give larger scale for higher octaves.
- **Distortion**: amount of distortion.
- **Type**: fBM, Multifractal, Hybrid Multifractal, Ridged Multifractal, Hetero Terrain (with **Offset** and **Gain**); see musgrave-fractal.
- **Normalize** (fBM only): keeps output within 0 to 1; when off the range is at most -(Detail + 1) to Detail + 1 (smaller if Roughness < 1).

## Outputs

**Factor** (value of the fractal noise) and **Color** (a different fractal noise in each component, usable as a vector to distort other textures).

## Recipes

- Roughness breakup: Noise Factor -> Map Range into a narrow roughness range.
- Domain warping: mix Noise Color into the coordinates (small factor) -> feed another texture's Vector. The Wave Texture's own Distortion works this way.

## Gotchas

- Noise sampled at whole-number multiples of 1/Scale always evaluates to 0.5 (for example objects on an integer grid); change Scale, add an offset to the coordinates, or use a higher dimension. For random values per object use the White Noise Texture.
- Slightly tilted flat surfaces can show banding; rotate the coordinates by an arbitrary amount.

## Verify

Preview Factor through an Emission shader: feature size matches Scale on a reference object.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch, docs.blender.org manual en/5.2). Confirmed against textures/noise: dimension behaviour, fractional Detail, Roughness, Lacunarity, Distortion, Type list, Normalize on fBM only with its range, outputs, and the whole-number 0.5 and banding notes. Removed the Detail 0-15 range, the wrong 'Lacunarity 4.0+' note, the default values, the 'W without sliding' remark, the Node Wrangler preview and the numeric recipe values.

Method: documentation only; no commands were run.

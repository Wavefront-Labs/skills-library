---
id: creative-arts.animation.blender.wave-texture
name: wave-texture
category: creative-arts
field: animation
product: blender
tags: [blender, procedural-texturing, wave-texture, bands, rings]
level: practitioner
status: docs-checked
description: "Build stripes and rings with the Blender Wave Texture: bands vs rings, direction, sine/saw/triangle profiles, distortion, detail and phase offset."
sources:
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/textures/wave.html
  - https://docs.blender.org/api/current/bpy.types.ShaderNodeTexWave.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# wave-texture

## Settings

- **Type**: Bands (straight stripes) or Rings (concentric).
- **Bands Direction**: X, Y, Z, Diagonal. **Rings Direction**: X, Y, Z, Spherical (rings propagate outward from a single point).
- **Wave Profile**: Sine, Saw, Triangle (Python API enum SIN, SAW, TRI; the manual page lists only Saw and Sine).
- Inputs: **Scale**, **Distortion**, **Detail** (distortion noise detail), **Detail Scale** (scale of distortion noise), **Roughness**, **Phase Offset** (position of the wave along the bands direction; animate it to scroll stripes). The Vector input defaults to Generated coordinates.
- Outputs: **Color** and **Factor**.
- Distortion, Detail, Detail Scale and Roughness correspond to the Noise Texture's inputs; the built-in distortion uses the Noise Texture Color output.

## Recipes

- Wood grain: Rings with Distortion, coordinates scaled along the grain -> Color Ramp of light and dark wood (procedural-wood).
- Marble: Bands Diagonal with Distortion and Detail -> Color Ramp for veins.
- Scrolling warning stripes: Bands with Saw profile, Phase Offset driven by the frame.
- Corrugated metal: Bands with Sine profile -> Bump Height.

## Verify

Preview: increasing Scale increases the number of bands; rings radiate from where the coordinate origin sits.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch, docs.blender.org manual en/5.2). Confirmed against textures/wave and the Python API page for ShaderNodeTexWave: type, directions, profiles (Sine, Saw, Triangle), input names (Roughness, not Detail Roughness), Phase Offset, outputs. Removed the numeric Distortion/Detail recipe values and the distortion-balance and Mapping Location claims.

Method: documentation only; no commands were run.

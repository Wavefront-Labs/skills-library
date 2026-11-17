---
id: creative-arts.animation.blender.eevee-volumetrics
name: eevee-volumetrics
category: creative-arts
field: animation
product: blender
tags: [blender, eevee, eevee-volumetrics, volume-resolution, volumetrics]
level: practitioner
status: docs-checked
description: "Tune EEVEE volumetrics render settings: resolution, steps, distribution, max depth and custom start/end range, with the documented limits."
sources:
  - https://docs.blender.org/manual/en/latest/render/eevee/render_settings/volumes.html
  - https://docs.blender.org/api/current/bpy.types.SceneEEVEE.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# eevee-volumetrics

Goal: smooth, stable volumetrics (fog, god rays, smoke) in EEVEE.

## Render Properties > Volumes

EEVEE simulates volumetric scattering by evaluating all volume objects inside the view frustum, using several 3D textures with high video memory usage. Resolution and Steps set the texture dimensions.

- **Resolution**: quality of the volumetric effects. Higher resolution uses more memory (the API description says so; the manual page sentence is worded the other way round, so judge by memory use on your GPU).
- **Steps**: number of steps to compute volumetric effects, distributed along the view depth; higher uses more video memory and gives more quality.
- **Distribution**: blend between linear and exponential sample distribution; higher values put more samples near the camera.
- **Max Depth**: maximum surface intersection count for the accurate volume intersection method; exceeding it creates artifacts (higher count uses more VRAM). The per-material Intersection setting (Fast or Accurate) chooses the method.
- **Custom Range** (Start, End): by default EEVEE computes the best depth range automatically. In some cases (a World volume shader, many volume objects) that is sub-optimal and noisy; Custom Range restricts computation to a range along camera depth to increase precision.
- Clamp (Light Paths > Clamping > Volume): see eevee-sampling-clamp. Volumetric Shadows and their Steps live in the Shadows panel (see eevee-volume-shadows).

## Limitations (from the manual)

Only single scattering; volumes are rendered for camera rays only (not in reflections, refractions or probes); volume shadowing only works within volumes and inside the view frustum.

## Workflow

1. Set Custom Range to where the fog actually is.
2. Raise Steps for banding along the view direction, and Resolution for blocky shafts, watching GPU memory.
3. Check edges for stability across a few frames at final samples.

## Verify

Render a shaft of light through a window into fog; look for banding along the beam and unstable edges across a few frames.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (EEVEE Volumes, Limitations) and SceneEEVEE properties in the 5.2 source. Confirmed: Resolution, Steps, Distribution, Max Depth, Custom Range, limitations. Noted: the manual's Resolution sentence conflicts with the API text; the API text is used. Removed unconfirmed: tile ratios 1:4 to 1:16 as volume options, missing-behind-transparency advice, Cycles recommendation for smoke.
Method: documentation only; no commands were run.

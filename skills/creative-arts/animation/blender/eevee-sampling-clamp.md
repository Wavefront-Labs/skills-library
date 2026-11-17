---
id: creative-arts.animation.blender.eevee-sampling-clamp
name: eevee-sampling-clamp
category: creative-arts
field: animation
product: blender
tags: [blender, eevee, eevee-sampling-clamp, eevee-samples, eevee-clamp, samples]
level: practitioner
status: docs-checked
description: "Set EEVEE render and viewport samples, temporal reprojection, jittered viewport shadows, and surface/volume direct and indirect clamping plus light intensity scaling."
sources:
  - https://docs.blender.org/manual/en/latest/render/eevee/render_settings/sampling.html
  - https://docs.blender.org/manual/en/latest/render/eevee/render_settings/light_paths.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# eevee-sampling-clamp

Goal: enough EEVEE samples to resolve soft effects, and clamping to control fireflies.

## Render Properties > Sampling

EEVEE uses Temporal Anti-Aliasing (TAA), which is sample based: more samples reduce aliasing at a cost in performance.

- **Viewport > Samples**: samples in the 3D viewport; 0 resamples continuously.
- **Viewport > Temporal Reprojection**: reduces noise while moving the viewport or during animation playback; can leave some ghosting.
- **Viewport > Jittered Shadows**: enables jittered shadows in the viewport (always enabled for final renders; also affects transparent shadows).
- **Render > Samples**: samples in the final render (Python `scene.eevee.taa_render_samples`).

Soft effects (jittered shadows, depth of field jitter, motion blur steps, raytracing noise) are averaged over these samples, so raise samples before pushing individual effect quality. When motion blur uses several steps, the sample count is rounded up to a multiple of the steps (see eevee-motion-blur).

## Clamping (Render Properties > Light Paths > Clamping)

- **Surface Direct Light**: limits the maximum light intensity a surface can reflect; reduces aliasing noise and fireflies at the cost of accuracy. 0.0 disables clamping.
- **Surface Indirect Light**: limits intensity reflected using ray tracing and light probes; also limits world lighting, since it counts as indirect light.
- **Volume Direct / Indirect Light**: the same for volume lighting.
- Lower values have a greater effect than higher ones; clamping also dims intentionally bright highlights, so balance firefly reduction against desired brightness.

## Intensity (Render Properties > Light Paths > Intensity)

**Direct Light** and **Indirect Light** scale the contribution of direct lighting and of indirect lighting (ray tracing, light probes, world lighting). They do not change ray depth, sampling or performance, and the indirect scale is applied after clamping.

## Verify

Render one frame at three sample counts and keep the lowest where shadow edges, depth of field and motion blur look smooth in a 100% crop. Compare crops before and after clamping for lost highlights.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (EEVEE Sampling, Light Paths). Confirmed: viewport/render samples, Temporal Reprojection, Jittered Shadows, clamp options and 0.0 disable, Intensity controls. Removed unconfirmed: default sample counts (16/64), sample recommendations, suggested clamp values, the command-line example and render-time linearity claim.
Method: documentation only; no commands were run.

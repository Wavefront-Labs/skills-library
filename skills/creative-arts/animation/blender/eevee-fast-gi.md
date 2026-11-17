---
id: creative-arts.animation.blender.eevee-fast-gi
name: eevee-fast-gi
category: creative-arts
field: animation
product: blender
tags: [blender, eevee, eevee-fast-gi, horizon-scan, ambient-occlusion, fast-gi]
level: practitioner
status: docs-checked
description: "Use EEVEE Fast GI Approximation: threshold, Ambient Occlusion vs Global Illumination method, resolution, rays, steps, precision, distance, thickness and limits."
sources:
  - https://docs.blender.org/manual/en/latest/render/eevee/render_settings/raytracing.html
  - https://docs.blender.org/api/current/bpy.types.RaytraceEEVEE.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# eevee-fast-gi

Goal: screen-space contact shadows and short-range bounce light in EEVEE for rough surfaces, as a cheaper fallback to ray tracing.

## Render Properties > Raytracing > Fast GI Approximation

Fast GI Approximation is a fallback to the ray-tracing pipeline for BSDFs with high roughness. It gives less noisy output and captures bounce lighting more efficiently than individually traced rays. It is currently a screen-space effect and inherits the screen-space limitations.

- **Threshold**: maximum roughness a BSDF can have to use ray tracing; rougher BSDFs progressively use Fast GI. A value of 1 raytraces every surface and disables Fast GI.
- **Method**: *Ambient Occlusion* (uses scene intersections to shadow the distant lighting from light probes; the fastest) or *Global Illumination* (takes light bouncing off surrounding objects into account).
- **Resolution**: resolution at which Fast GI is computed (the options run from 1:1 down to 1:16). Lower is faster and uses less memory but is blurrier.
- **Rays**: GI rays per pixel at that resolution; higher reduces noise.
- **Steps**: screen samples per GI ray; higher reduces noise and raises quality. With more steps the Thickness values can be lowered without losing much bounce energy.
- **Precision**: higher increases intersection precision and performance cost.
- **Distance**: if non-zero, the maximum distance at which other surfaces contribute.
- **Thickness Near**: geometric thickness of surfaces; reduces light leaking and missing contact occlusion, with effectiveness falling off with distance from the shading point. **Far**: angular thickness; reduces energy loss and missing occlusion of far geometry, but very thin objects block or reflect too much light at high values.
- **Bias**: biases the shading normal to reduce self-intersection artifacts.

## Limits

- Screen space only: off-screen or hidden occluders do not count (see eevee-film-overscan for edge handling).
- When Raytracing is disabled, EEVEE uses a faster pipeline based on pre-filtered light probes.

## Verify

Toggle Fast GI (and compare the two Methods) on a frame with a character against a wall. Contact darkening should appear without a dark halo outline; adjust Thickness and Distance if halos appear.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (EEVEE Raytracing) and RaytraceEEVEE/SceneEEVEE properties in the 5.2 source. Confirmed: Fast GI is a high-roughness fallback and screen-space, Threshold, Method, Resolution (1:1 to 1:16), Rays, Steps, Precision, Distance, Thickness Near/Far, Bias. Corrected: resolution range was given as 1:1 to 1:4; the setting is "Threshold" not "Max Roughness". Removed unconfirmed: version gate, EEVEE Legacy AO comparison, typical distance values.
Method: documentation only; no commands were run.

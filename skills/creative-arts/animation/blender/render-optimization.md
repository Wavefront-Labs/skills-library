---
id: creative-arts.animation.blender.render-optimization
name: render-optimization
category: creative-arts
field: animation
product: blender
tags: [blender, eevee-next, render-optimization, samples, taa, denoise, shadows, simplify, lod, render-layers, batch, headless, amd, hip, caching, performance]
level: advanced
status: docs-checked
description: "Fast, clean EEVEE renders in Blender: samples, shadow and volume cost, Simplify, culling, denoise node, passes and Cryptomatte."
sources:
  - https://docs.blender.org/manual/en/latest/render/eevee/render_settings/sampling.html
  - https://docs.blender.org/manual/en/latest/render/eevee/render_settings/volumes.html
  - https://docs.blender.org/manual/en/latest/render/eevee/render_settings/performance.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/simplify.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/performance.html
  - https://docs.blender.org/manual/en/latest/render/layers/passes.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Render optimization for EEVEE (Blender)

Goal: keep a series of shots rendering fast and clean without re-render churn. The principle: spend samples and memory where the image has noise or detail, and structure passes so a note means recomposing, not re-rendering. Device setup and headless flags live in `rendering-amd-hip.md`; this skill is the settings layer.

## 1. Samples and TAA

EEVEE uses Temporal Anti-Aliasing, which is sample based: more samples reduce aliasing at a performance cost. *Render > Sampling* has separate Viewport and Render sample counts; a viewport count of zero resamples continuously. Temporal Reprojection reduces noise while moving the viewport or playing back, and can leave ghosting.

Measure before cranking: render a hero frame at two sample counts and compare. If you cannot see the difference, ship the lower one. Flat, low-noise looks gain mostly on edge aliasing.

## 2. Shadows, lights and volumes

- Shadow **Rays** per light: higher values reduce shadow sampling noise. **Steps** per ray: higher gives softer shadows at higher cost. **Resolution** is a percentage of shadow map size. Jittered shadows are always enabled for final renders.
- **Volumetric Shadows** is described as very computationally expensive with limitations; enable only when needed.
- **Light Threshold** (Advanced): a minimum intensity for a light to contribute, used to compute a cut-off distance; lower values improve performance, and Custom Distance overrides it.
- **Volumes** use several 3D textures with high video memory usage. Resolution and Steps tune the texture dimensions; Distribution blends linear and exponential sampling (higher values put more samples near the camera). The Custom Range (Start/End) restricts computation along camera depth and can improve precision, especially with world volume shaders or many volume objects.
- **Performance panel:** Shadow Pool and Light Probes Volume Pool sizes trade scene capacity against GPU memory; increasing Shadow Pool can fix the "Shadow buffer full" error. Anisotropic Filtering sharpens textures at grazing angles with a small performance impact.

## 3. Denoising in the compositor

The Denoise compositor node can run on CPU, GPU or Auto (Performance > Compositor > Denoise Nodes). Quality can follow the scene with separate Preview and Final settings (High, Balanced, Fast). Passes for edge-preserving denoise include Denoising Albedo and Denoising Normal. Prefer denoising only the noisy pass rather than the whole frame, so crisp edges are not smeared.

## 4. Simplify and culling

*Render > Simplify* has Max Subdivision (cap on Subdivision Surface modifier levels), Child Particles (show a subset), Texture Size Limit (scales textures down to no larger than the chosen size) and, in the viewport, Volume Resolution and Normals. Culling: Camera Cull (by frustum with a Margin) and Distance Cull (by distance from the active camera). Use these per shot by camera distance rather than one global setting.

## 5. Passes and re-render churn

A pass is intermediate render information extracted as a separate image. Render the passes you compose with (for example Emission, Mist, Normal, Cryptomatte) so a note on one element is a compositor change.
- Mist gives a cleaner depth cue than Depth when depth of field or motion blur are on (the Depth pass is noisy then).
- Cryptomatte makes object, material or asset masks; it works with transparency and, in Cycles, motion blur and depth of field. Levels is the maximum objects per pixel; the Render Layers node outputs half as many Cryptomatte images.
- Split characters, set and FX across view layers so a note re-renders one layer. Keep an ungraded intermediate image sequence so grade changes never need a re-render.

## 6. Batch and determinism

- Render in shot chunks and skip frames whose output file already exists, so a relaunched batch only fills gaps.
- Bake simulations and caches before the render job so chunks do not re-simulate.
- Persistent Data is documented under Cycles performance settings; do not assume it applies to EEVEE.

## 7. Find the cost before cutting

Toggle each feature (volumes, shadows, samples, textures) off in turn and time one frame; cut the biggest first.

## Checked

2026-11-09. Confirmed against the EEVEE Sampling, Volumes and Performance pages, Cycles Simplify and Performance pages, and the Render Passes page: all settings and behaviours above. Removed (not on the cited pages): the 87-shot series figures, the specific cost ranking, motion-blur advice, light linking, multilayer EXR advice, SSR and raytracing guidance, sample counts such as 16 vs 32, hardware specifics, and links to unchecked sibling skills' details.
Method: documentation only; no commands were run.

## Verify

1. Hero frame at two sample counts compared; the lower one ships if indistinguishable.
2. A note on one element re-renders a single view layer or only the compositor.
3. A killed and relaunched batch skips finished frames.
4. For any slow shot you can name the top cost from a toggle-and-time test.

See also: `rendering-amd-hip.md`, `blendercraft-headless.md`, `compositing-grade.md`.

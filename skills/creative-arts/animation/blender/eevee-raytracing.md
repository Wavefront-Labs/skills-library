---
id: creative-arts.animation.blender.eevee-raytracing
name: eevee-raytracing
category: creative-arts
field: animation
product: blender
tags: [blender, eevee, eevee-next, eevee-raytracing, screen-trace, raytrace-resolution, reflections]
level: practitioner
status: verified
description: "Configure EEVEE raytracing: Light Probe vs Screen-Trace method, resolution, screen-trace precision and thickness, backfaces, denoising stages, and documented limitations."
sources:
  - https://docs.blender.org/manual/en/latest/render/eevee/render_settings/raytracing.html
  - https://docs.blender.org/manual/en/latest/render/eevee/limitations/limitations.html
  - https://docs.blender.org/api/current/bpy.types.RaytraceEEVEE.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# eevee-raytracing

Goal: get EEVEE reflections and refractions that hold up, at a cost you can afford.

## Render Properties > Raytracing

The ray-tracing pipeline aims to increase the accuracy of surface indirect lighting by generating a ray from each BSDF and finding its intersection with the scene. When it is disabled, EEVEE uses a faster pipeline based on pre-filtered light probes (more visually stable, less accurate).

- **Method**:
  - *Light Probe*: uses light probe spheres and planes to find intersections; the lowest tracing cost but relies on manually placed probes.
  - *Screen-Trace*: traces rays against the screen depth buffer and falls back to light probes if a ray exits the view.
- **Resolution**: resolution at which tracing is done; lower options are faster and use less memory but give blurrier results.
- **Screen Tracing** (only with Screen-Trace):
  - *Precision*: higher improves intersection accuracy and reduces artifacts, but decreases the maximum tracing distance and costs more.
  - *Thickness*: thickness assumed for depth-buffer surfaces. Higher can reduce missed intersections but may stretch reflections and increase flicker; lower is more accurate but rays may miss thin surfaces.
  - *Backface* (with Radiance Scale; not present in Blender 4.5.14, so check your version): treats rays hitting back sides as valid hits, which can reduce light leaking with screen-space GI; Radiance Scale controls how much front-face lighting is reused for those hits.
- **Denoising**: *Spatial Reuse* (reuses rays from neighbour pixels, can introduce light leaks), *Temporal Accumulation* (reprojects the last results; removes fireflies but introduces colour bias; useful for viewport stability or faster convergence), *Bilateral Filter* (blurs the resolved output). Denoising helps stability but can over-blur the result.
- **Fast GI Approximation** takes over for rough BSDFs above the Threshold; see eevee-fast-gi.

## Limitations (from the manual)

- Screen-space effects only see what is inside the view, and only the front-most depth layer.
- Blended materials are not compatible with raytracing; blended and raytrace-refraction materials do not appear in the reflections of dithered materials.
- Only one refraction event is correctly modelled; the Thickness workflow can approximate a second.
- Only dithered materials that do not use Raytraced Transmission can be refracted.
- Light probe planes only work with the Screen-Trace method.

## Workflow

1. Enable Raytracing, pick Screen-Trace for contact reflections, and keep Resolution as high as time allows for finals.
2. Add sphere probes (see eevee-sphere-plane-probes) so rays that leave the screen fall back to something sensible.
3. Use Film > Overscan (see eevee-film-overscan) for edge dropout.
4. Set material Thickness and Raytraced Transmission for refraction (see eevee-material-render-method).

## Verify

Toggle Raytracing on a frame with a glossy floor and a nearby object; contact reflections should appear with Screen-Trace on.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (EEVEE Raytracing, Limitations). Confirmed: Method options, Resolution, Screen Tracing Precision/Thickness/Backface, Denoising stages, Fast GI relation, limitations list. Removed unconfirmed: version gate, typical settings (Max Roughness values, sample counts), artifact-cause guesses, advice to turn all denoise stages on.
Run check, 2026-11-01, Blender 4.5.14 LTS headless (EEVEE Next): `scene.eevee.use_raytracing` and `ray_tracing_method` with items PROBE and SCREEN; `ray_tracing_options` has `resolution_scale` (items 1, 2, 4, 8, 16), `screen_trace_quality` (precision), `screen_trace_thickness`, `trace_max_roughness`, `use_denoise`, `denoise_spatial`, `denoise_temporal`, `denoise_bilateral`; Fast GI has `use_fast_gi` and `fast_gi_*` properties; `use_overscan` and `overscan_size` exist. Unrun: all rendered behaviour and limitations, Backface and Radiance Scale (not in 4.5.14), UI wording.

Method: documentation checked against the manual and API pages; the code was run headless in Blender 4.5.14.

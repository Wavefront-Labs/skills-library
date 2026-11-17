---
id: creative-arts.animation.blender.eevee-shadows
name: eevee-shadows
category: creative-arts
field: animation
product: blender
tags: [blender, eevee, eevee-next, eevee-shadows, shadow-rays, jittered-shadows, virtual-shadow-maps]
level: practitioner
status: verified
description: "Tune EEVEE virtual shadow maps: render shadow rays and steps, per-light jitter, filter and resolution limit, shadow pool memory, and fixing light leaks."
sources:
  - https://docs.blender.org/manual/en/latest/render/eevee/render_settings/sampling.html
  - https://docs.blender.org/manual/en/latest/render/eevee/light_settings.html
  - https://docs.blender.org/manual/en/latest/render/eevee/limitations/limitations.html
  - https://docs.blender.org/manual/en/latest/render/eevee/render_settings/performance.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# eevee-shadows

Goal: soft, stable, artefact-free shadows in EEVEE.

EEVEE uses Virtual Shadow Mapping (resolution only where needed, with an efficient caching mechanism) together with Shadow Map Raytracing. It is compatible with any material Render Method.

## Render Properties > Shadows

- **Rays**: rays traced per light; higher reduces the noise from random shadow sampling.
- **Steps**: shadow map samples per shadow ray; higher gives softer shadows at higher cost.
- **Volumetric Shadows** (with **Steps**): approximates light absorption of surrounding volume objects; very expensive and with limitations.
- **Resolution**: resolution percentage of shadow maps.
- **Advanced > Light Threshold**: minimum light intensity for a light to contribute; used to compute the distance at which the light's influence is cut off. Lower values improve performance. A light's **Custom Distance** overrides it.
- **Performance > Memory > Shadow Pool**: a bigger pool allows more shadows but may not fit GPU memory and decreases performance; increasing it may fix the "Shadow buffer full" error.

## Per light (Light Properties > Shadow)

- **Jitter**: jittered soft shadows to increase shadow precision; high performance impact because the shadow map cannot be cached and is updated every sample. Not visible in the viewport unless Jittered Shadows is enabled in Sampling (final renders always jitter).
- **Overblur**: shadow tracing on each jittered sample to reduce undersampling artifacts; anything above zero is blurrier and not physically correct.
- **Filter**: blurs shadow aliasing using PCF with a circular kernel; values above 1 px increase the chance of light leaking.
- **Resolution Limit**: minimum size of a shadow map pixel; higher values use less memory and speed up heavy scenes at the cost of quality, and raise the chance of leaking. **Absolute Resolution Limit** limits it at 1 unit from the light origin instead of relative to the shadowed pixel (not available for sun lights); the manual gives resolution_limit = 2 * sqrt(2) / resolution.

## Fixes (from the manual)

- "Shadow buffer full": raise the Shadow Pool or the Resolution Limit on some lights; otherwise disable shadow casting on some lights.
- Light leaking from overlapping casters: lower the Steps, enable Jitter, or reduce the light shape size.
- Thin objects (walls without thickness) can leak on the shadowed side: give them thickness or lower the Resolution Limit.

## Verify

Render a character standing on a floor with a sun and an area light. The contact shadow under the feet should have no gap and the penumbra should widen with distance.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (EEVEE Sampling/Shadows, Light settings, Performance, Limitations). Confirmed: Rays, Steps, Volumetric Shadows, Resolution, Light Threshold, Shadow Pool, per-light Jitter/Overblur/Filter/Resolution Limit/Absolute Resolution Limit and the documented fixes. Removed unconfirmed: sizes for the pool, recommended ray counts, shimmer advice, a separate "Volume Shadows" panel.
Run check, 2026-11-01, Blender 4.5.14 LTS headless (EEVEE Next): `scene.eevee` has `shadow_ray_count` (default 1), `shadow_step_count` (6), `use_volumetric_shadows` with `volumetric_shadow_samples` (16), `shadow_resolution_scale` (1.0), `light_threshold` (0.01), `shadow_pool_size` (enum 16 to 1024, default 512), `use_shadows`, `use_shadow_jitter_viewport`; lights have `use_shadow_jitter`, `shadow_jitter_overblur`, `shadow_filter_radius` (1.0), `shadow_maximum_resolution`, `use_absolute_resolution` and `use_custom_distance`; the sun light type has no `use_absolute_resolution`. Unrun: every rendering effect described (leaking, jitter caching, overblur, filter, the resolution-limit formula, shadow buffer full error), UI panel names.

Method: documentation checked against the manual and API pages; the code was run headless in Blender 4.5.14.

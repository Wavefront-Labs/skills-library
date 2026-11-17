---
id: creative-arts.animation.blender.light-shadow-settings
name: light-shadow-settings
category: creative-arts
field: animation
product: blender
tags: [blender, lights, light-shadow-settings, soft-shadows, shadow-jitter, shadow-resolution, eevee]
level: practitioner
status: docs-checked
description: "Tune Blender light shadows: Cycles cast shadow and ray visibility, EEVEE virtual shadow maps, jitter, resolution limit and shadow ray steps."
sources:
  - https://docs.blender.org/manual/en/latest/render/lights/light_object.html
  - https://docs.blender.org/manual/en/latest/render/eevee/light_settings.html
  - https://docs.blender.org/manual/en/latest/render/eevee/render_settings/sampling.html
  - https://docs.blender.org/manual/en/latest/render/eevee/render_settings/performance.html
  - https://docs.blender.org/manual/en/latest/render/cycles/light_settings.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# light-shadow-settings

## Cycles

- Larger lights (Radius / Size / Angle) give softer shadows.
- Light > Settings > **Cast Shadow** off: light is not blocked by objects in between, which can speed up rendering.
- Object > Visibility > Ray Visibility > **Shadow** off: the object stops casting shadows.
- Light linking / shadow linking for per-object control (see `creative-arts.animation.blender.shadow-linking-setup`).

## EEVEE

EEVEE uses Virtual Shadow Mapping together with Shadow Map Raytracing. Per light (Light > Shadow):
- **Jitter**: jittered soft shadows to increase precision. High performance impact, because the shadow map cannot be cached. **Overblur** applies shadow tracing to each jittered sample to reduce under-sampling; values above zero are blurrier and not physically correct.
- **Filter**: blurs shadow aliasing with percentage closer filtering; values above 1 px raise the chance of light leaking.
- **Resolution Limit**: minimum size of a shadow map pixel; higher values use less memory and speed up heavy scenes at the cost of shadow quality and more light leaking. **Absolute Resolution Limit** does not exist for Sun lights.

Scene (Render > Sampling > Shadows):
- **Rays**: number of rays traced per light; more reduces noise. **Steps**: shadow map samples per shadow ray; more gives softer shadows at higher cost.
- **Volumetric Shadows** and **Resolution** (percentage of shadow map resolution).
- **Light Threshold** (Sampling > Advanced): minimum intensity for a light to contribute; used to compute the cut-off distance, lower values improve performance. A light's *Custom Distance* overrides it.
- **Shadow Pool** (Render > Performance > Memory).

## Gotchas

- Error "Shadow buffer full": increase the Shadow Pool size or the Resolution Limit on some lights; otherwise disable shadow casting on some lights.
- Jitter can reduce light-leaking artifacts caused by large lights and shadow map raytracing.
- In the viewport, jittered shadows are only shown when *Jittered Shadows* is enabled in the render sampling settings; final renders always use them.

## Verify

Compare EEVEE and Cycles shots of the same contact (foot on floor): penumbra and contact darkness should match closely after tuning.

## Checked

2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch) and the 5.2 source UI scripts. Confirmed: Cast Shadow and the Shadow ray visibility toggle (Cycles light settings and Cycles object pages); EEVEE Jitter, Overblur, Filter, Resolution Limit, Absolute Resolution Limit, Shadow buffer full tips, Custom Distance (EEVEE light settings page); Rays, Steps, Volumetric Shadows, Resolution, Light Threshold, Jittered Shadows (EEVEE Sampling page); Shadow Pool under Performance > Memory (EEVEE Performance page). Removed unsupported claims (4.2 version gate, contact-shadow history, thicker walls, sun pool waste).

Method: documentation only; no commands were run.

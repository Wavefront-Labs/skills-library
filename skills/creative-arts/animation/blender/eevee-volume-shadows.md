---
id: creative-arts.animation.blender.eevee-volume-shadows
name: eevee-volume-shadows
category: creative-arts
field: animation
product: blender
tags: [blender, eevee-volume-shadows, volumetric-shadows, eevee, eevee-volumetrics, volume-lighting, god-rays]
level: practitioner
status: docs-checked
description: "Light volumes in EEVEE: volumetric shadows and steps, light Volume Scatter influence, volumes render settings, and the documented single-scattering limitations."
sources:
  - https://docs.blender.org/manual/en/latest/render/eevee/render_settings/volumes.html
  - https://docs.blender.org/manual/en/latest/render/eevee/render_settings/sampling.html
  - https://docs.blender.org/manual/en/latest/render/eevee/light_settings.html
  - https://docs.blender.org/manual/en/latest/render/eevee/limitations/limitations.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# eevee-volume-shadows

Goal: god rays and self-shadowed smoke in EEVEE that stay stable in animation.

## Render Properties > Volumes

EEVEE evaluates all volume objects inside the view frustum using 3D textures with high video memory use. Settings (see eevee-volumetrics for the full list): **Resolution**, **Steps** (distributed along the view depth), **Distribution** (blend between linear and exponential; higher puts more samples near the camera), **Max Depth** (intersection count for the accurate volume intersection method; artifacts if exceeded) and **Custom Range** Start/End to restrict computation to a depth range, which increases precision (useful with a World volume shader or many volume objects).

## Volumetric shadows (Render Properties > Shadows)

**Volumetric Shadows** approximates light absorption by surrounding volume objects, making volumes more opaque to light. It is very computationally expensive and has limitations; **Steps** sets the number of steps used to compute it.

## Lights

Light Properties > Influence has a **Volume Scatter** multiplier (volume light intensity). Values other than 1.0 break PBR rules but are meant for artistic control, for example setting a fill light's Volume Scatter to 0 so it does not lift the fog. Shadow settings on the light affect the shafts.

## Limitations (from the manual)

- Only single scattering is supported.
- Volumetrics render only for camera rays; they do not appear in reflections, refractions or probes.
- Volumetric shadowing only works inside volumetrics (volumes do not cast shadows on solid objects) and only for volumes inside the view frustum.

## Workflow

- Prefer a bounded volume object over a World volume when you want control; a World volume or many volumes benefits from Custom Range.
- Tune Steps and Resolution together, and check shafts across a short camera move for shimmer.

## Verify

Shafts from a spot light should be visible through a window frame without shimmering across a short camera move; setting that light's Volume Scatter to 0 should remove its shaft.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (EEVEE Volumes, Shadows/Sampling, Light settings, Limitations). Confirmed: volumes settings, Volumetric Shadows and Steps, Volume Scatter influence, single-scattering limitations. Removed unconfirmed: tile-size values 2/4/8/16, anisotropy suggestion, "Custom Volume factor", leak and banding fixes, small-object claim.
Method: documentation only; no commands were run.

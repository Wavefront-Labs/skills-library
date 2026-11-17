---
id: creative-arts.animation.blender.volume-scatter-absorption
name: volume-scatter-absorption
category: creative-arts
field: animation
product: blender
tags: [blender, volume-scatter-absorption, volume-scatter, volume-absorption, volumetrics, cycles, eevee]
level: practitioner
status: docs-checked
description: "Use Volume Scatter and Volume Absorption nodes: density, colour, anisotropy and phase functions, combining them, and choosing them over Principled Volume for fog, haze or liquids."
sources:
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/volume_scatter.html
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/volume_absorption.html
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/volume_principled.html
  - https://docs.blender.org/manual/en/5.2/render/eevee/material_settings.html
  - https://docs.blender.org/manual/en/5.2/render/cycles/render_settings/light_paths.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# volume-scatter-absorption

Goal: participating media built from the two primitive volume closures. Both output **Volume**, which goes to the Volume input of the Material or World Output node.

## Volume Absorption

Absorbs light as it passes through the volume: water and coloured glass.
- **Color**: colour of the volume. **Density**: density of the absorption effect.

Coloured glass trick: a white Glass BSDF on Surface plus Volume Absorption on Volume, so colour depends on thickness.

## Volume Scatter

Scatters light: fog, and with Absorption, smoke.
- **Color**: scattering coefficients per colour channel. **Density**.
- **Phase** property: Henyey-Greenstein; Fournier-Forand (underwater), Draine (interstellar dust), Rayleigh (particles smaller than the wavelength, as in sky scattering) and Mie (larger particles, as in cloud and fog), all four Cycles only.
- Phase-specific inputs: **Anisotropy** (Henyey-Greenstein and Draine; backward versus forward scattering), **IOR** and **Backscatter** (Fournier-Forand), **Alpha** (Draine; blends Henyey-Greenstein at 0 and Cornette and Shanks at 1), **Diameter** (Mie, in micrometres).
- Phase functions can be combined with a Mix Shader.

## Combining

Add Shader (Scatter + Absorption) into Material Output > Volume. The Principled Volume node bundles scattering, absorption and blackbody emission into one node; use the primitives when you want separate control.

## Gotchas

- EEVEE's Material Settings > Volume **Intersection** option: Fast treats every face as a medium interface and is correct for manifold geometry with no inner parts; Accurate handles inner parts at a significant memory cost.
- Cycles Light Paths > Volume sets the maximum volume scattering bounces; thick scattering media can look dark with too few.
- See `creative-arts.animation.blender.eevee-volumetrics` for EEVEE volume settings.

## Verify

A cube of Scatter shows a light shaft from a spot lamp; adding Absorption with a tint colours and darkens the transmitted light with thickness.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch, docs.blender.org manual en/5.2). Confirmed against shader/volume_scatter (phase list, per-phase inputs, Cycles-only markers), shader/volume_absorption, shader/volume_principled, EEVEE material settings (volume Intersection) and Cycles light paths (volume bounces). Removed the unconfirmed Beer-Lambert statement, per-metre density units, the 100 m fog example and 0.001-0.02 values, the 0.3-0.8 anisotropy advice and the froxel remark.

Method: documentation only; no commands were run.

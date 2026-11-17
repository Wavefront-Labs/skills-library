---
id: creative-arts.animation.blender.volume-clouds
name: volume-clouds
category: creative-arts
field: animation
product: blender
tags: [blender, volume-clouds, procedural-clouds, volumetrics, principled-volume, cycles, noise-texture]
level: advanced
status: docs-checked
description: "Build procedural clouds in Blender with Principled Volume: density from texture nodes, anisotropy, Cycles volume bounces, and OpenVDB cloud volume objects."
sources:
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/volume_principled.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/light_paths.html
  - https://docs.blender.org/manual/en/latest/modeling/volumes/introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# volume-clouds

Goal: soft, bright-edged cumulus or stylised clouds without simulation.

## Shader-driven cloud
Put a Principled Volume material (Volume input of the Material Output) on a container mesh scaled to the cloud bounds. Drive **Density** from texture nodes (for example a Noise Texture fed by Texture Coordinate Object), shaping edges with Map Range or Color Ramp nodes so density falls to zero inside the container; otherwise the box boundary shows. Set **Color** white and **Anisotropy** to a forward-scattering (positive) value for brighter rims when backlit; **Absorption Color** tints shadows.

## Volume objects
OpenVDB data (for example the Walt Disney Animation Studios cloud data set shown in the manual) imports as a Volume object, rendered by default with Principled Volume using grids `density`, `color` and `temperature`. In Blender, sparse VDB volumes are still rendered as dense volumes, so large caches cost memory and time.

## Render settings (Cycles)
- Light Paths > **Volume** bounces: maximum number of volume scattering bounces; the default is 0 (no multiple scattering), so raise it for clouds, trading render time for brightness and softness.
- Render Properties > Volumes: default null-scattering algorithm, or the **Biased** option with Step Rate and Max Steps (see volume-step-rate).
- Material Settings > Volume: Sampling Method and Interpolation (Cubic for denser volumes).

## Gotchas
- Non-uniform object scale stretches coordinate-based noise; apply the scale or compensate in the shader.
- High density combined with many bounces is costly; reduce density and compensate with brighter lighting.

## Verify
A backlit render shows bright rims and denser cores; a frontlit render shows soft white shapes with no visible box edges.

## Checked
Date: 2026-10-27. Documentation: Blender manual (Principled Volume, Cycles Light Paths and Volumes, Volume introduction), branch blender-v5.2-release; Volume bounces default from the Cycles add-on properties.py on the Blender main branch. Confirmed: Principled Volume input names and meanings, Volume bounces default and meaning, Biased option, default grids, dense rendering limitation. Removed unconfirmed claims: specific Noise Texture, Map Range and anisotropy values, light strengths, bounce counts, step rates, denoiser remarks and Geometry Nodes cloud recipes (node names not verified for the current release).
Method: documentation only; no commands were run.

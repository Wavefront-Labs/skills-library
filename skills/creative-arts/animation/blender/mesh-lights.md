---
id: creative-arts.animation.blender.mesh-lights
name: mesh-lights
category: creative-arts
field: animation
product: blender
tags: [blender, lighting, mesh-lights, emissive-mesh, emission, emission-sampling]
level: practitioner
status: docs-checked
description: "Light with emissive meshes in Blender: emission strength, Cycles emission sampling mode, noise from small emitters, EEVEE behaviour and practical lights."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/material_settings.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/emission.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/sampling.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# mesh-lights

## Setup

A material with an **Emission** shader. Per the manual, Strength 1.0 makes the object appear exactly the Color input ('shadeless'); the colour of a light also affects how bright it appears.

## Cycles Emission Sampling

Material Properties > Settings > **Emission Sampling** only matters if the material has an emissive node:
- **None**: the surface is not used as a light for sampling.
- **Auto**: decided automatically from emission intensity.
- **Front** / **Back**: only that side acts as a light (Front suits closed meshes whose interior is not visible).
- **Front and Back**: both sides.

**Light Tree** (Render Properties > Sampling > Lights) samples lights more effectively considering distance and estimated intensity, which can reduce noise at some cost per sample. It does not account for custom falloff, ray visibility or complex shader node setups including textures.

## When to use

- Shaped lights such as neon tubes, LED strips, screens and lampshades.
- Practicals: a real light inside plus an emissive bulb mesh; set Emission Sampling to None on the bulb if it should only appear glowing.

## Verify

Neon sign render: the light pool on the wall matches the sign colour; with Emission Sampling set to None the direct light from the sign disappears, proving the setting.

## Checked
2026-10-27, Blender 5.2 manual (blender-v5.2-release RST) render/cycles/material_settings (Emission Sampling options and effect), render/shader_nodes/shader/emission (Strength 1.0 gives the object the same colour as the input), render/cycles/render_settings/sampling (Light Tree). Removed unconfirmed version gates, EEVEE behaviour, firefly and pass claims.
Method: documentation only; no commands were run.

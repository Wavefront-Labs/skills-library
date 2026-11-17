---
id: creative-arts.animation.blender.ies-lights
name: ies-lights
category: creative-arts
field: animation
product: blender
tags: [blender, lights, ies-lights, ies-texture, ies-profile, light-nodes, photometric]
level: practitioner
status: docs-checked
description: "Apply manufacturer IES photometric profiles to Blender lights with the IES Texture node in Cycles, set strength correctly and avoid common pitfalls."
sources:
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/textures/ies.html
  - https://docs.blender.org/manual/en/latest/render/cycles/light_settings.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/output/light.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# ies-lights

## Setup (Cycles only)

1. Add a light (a Point light is the usual choice).
2. In the light's Nodes panel (or the Shader Editor in Light context) add **Texture > IES Texture**.
3. Mode **Internal** (an IES file embedded in a text data-block in the blend-file, for easy distribution) or **External** (a file on disk; keep the path relative when the project moves).
4. Connect the IES Texture **Factor** output to Emission **Strength** (the manual's typical use). Leave the Vector input empty: it defaults to the normal.

## Strength

- The node has a Strength input that multiplies the light strength. IES files store the directional intensity distribution of a light source.
- The Factor can also be multiplied with a Math node to dim without editing power.

## Sources of profiles

Download from manufacturer websites or IES library sites. Check the licence for commercial work.

## Gotchas

- Light shader nodes are supported by Cycles only (see the Light Output node page), so the IES node has no effect in EEVEE.
- An External file path breaks on render farms unless it is relative and shipped with the .blend (or use Internal mode).

## Verify

Light next to a wall renders the characteristic pattern of the profile; swapping profiles changes it.

## Checked

2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch) and the 5.2 source UI scripts. Confirmed: IES Texture inputs (Vector defaults to the normal, Strength), Mode Internal/External, Factor output and typical use (IES Texture page); light node trees and Cycles-only limitation (Cycles light settings and Light Output pages). Removed unsupported claims about the Use Nodes checkbox, spot size clipping, radius ranges, light orientation, candela handling and named manufacturers.

Method: documentation only; no commands were run.

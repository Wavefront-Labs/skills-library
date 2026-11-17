---
id: creative-arts.animation.blender.light-nodes-falloff
name: light-nodes-falloff
category: creative-arts
field: animation
product: blender
tags: [blender, lighting, light-nodes, light-falloff, light-node-tree, cycles]
level: practitioner
status: docs-checked
description: "Use node trees on Blender lights (Cycles): Emission and Light Output nodes, Light Falloff node (quadratic/linear/constant, smooth), textures and IES."
sources:
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/color/light_falloff.html
  - https://docs.blender.org/manual/en/latest/render/cycles/light_settings.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/output/light.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/input/light_path.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# light-nodes-falloff

Goal: non-physical falloff, colour/strength variation and projected patterns from lights.

## Enable
In Cycles a light is defined by shader nodes: Light properties > **Nodes** panel (Surface), or the Shader Editor in Light context. An Emission shader (Color, Strength) is connected to the **Light Output** node; only emission-based shading contributes to lighting. The 5.2 Cycles light panels have no Use Nodes checkbox. The basic Light settings (Power and the others) are applied on top of the light output node.

## Light Falloff node
Cycles only. Inputs Strength and **Smooth** (smooths intensity near the light, which avoids harsh highlights and reduces GI noise; 0.0 is no smoothing, maximum light strength is strength/smooth). Outputs:
- **Quadratic**: corresponds to reality; leaves strength unmodified if Smooth is 0.
- **Linear**: slower decrease in intensity over distance.
- **Constant**: distance has no influence on intensity.
Wire the chosen output into Emission Strength.

## Patterns
Use Texture nodes to vary light colour or intensity across the light surface, or drive intensity and colour with Math nodes or animation, for patterned lights and flicker. IES profiles use the IES Texture node (see `creative-arts.animation.blender.ies-lights`).

## Other tricks
- Light Path node: *Is Camera Ray*, *Is Glossy Ray* and the other ray outputs change contribution per ray type.
- Several Light Output nodes can target All, Cycles or EEVEE (the node's *Target* property).

## Gotchas
- Light shader nodes are supported by Cycles only; the 5.2 EEVEE light panel has no Nodes panel.
- Linear or Constant falloff may add more light with every global illumination bounce, making the image extremely bright when many bounces are used.
- Light Power is applied on top of the node strength, so keep one of them at 1 to avoid confusion.

## Verify
Render a corridor with Quadratic vs Linear falloff: Linear lights reach further down the hall.

## Checked

2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch) and the 5.2 source UI scripts. Confirmed: Light shader nodes, Emission to Light Output, basic settings applied on top, Cycles-only limitation (Cycles light settings and Light Output pages); Light Falloff inputs, outputs, Smooth maths and GI warning (Light Falloff page); Light Path ray outputs (Light Path page); no Use Nodes checkbox and a Nodes panel only in the Cycles panels (ui.py, properties_data_light.py). Removed unsupported gobo projection recipe and the Object Info randomisation tip.

Method: documentation only; no commands were run.

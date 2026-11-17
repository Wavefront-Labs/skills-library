---
id: creative-arts.animation.blender.light-nodes
name: light-nodes
category: creative-arts
field: animation
product: blender
tags: [blender, lights, light-nodes, light-falloff, light-node-tree, cycles]
level: practitioner
status: docs-checked
description: "Build Cycles light node trees in the Shader Editor Light context: Emission into Light Output, Light Falloff node, IES Texture, textured lights and Temperature."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/light_settings.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/color/light_falloff.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/textures/ies.html
  - https://docs.blender.org/manual/en/latest/render/lights/light_object.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# light-nodes

## Where light nodes live

In Cycles a light can be defined with shader nodes. Select a light object and set the **Shader Editor** to the **Light** context. By default a light has an **Emission** shader connected to a **Light Output** node; only shader nodes connected to Light Output affect the light. The basic Light settings (Power, colour, etc.) are applied on top of the light output node. Limits: this is Cycles only (EEVEE uses simplified light models and ignores light node trees), and only Emission-based shading contributes to lighting; other BSDFs have no effect on lights.

The light settings can also be edited in Shader Editor > Sidebar > Options.

## Light Falloff node (Cycles only)

- Inputs **Strength** (strength before falloff modification) and **Smooth** (smooths intensity near the light to avoid harsh highlights and reduce GI noise; 0 means no smoothing; maximum light strength becomes strength / smooth).
- Outputs **Quadratic** (physically correct; leaves strength unmodified when Smooth is 0), **Linear** (slower decrease over distance) and **Constant** (distance has no influence). Plug the chosen output into the Emission Strength.
- The manual warns that Linear or Constant falloff can add more light with every global-illumination bounce, so scenes with many bounces can become extremely bright.

## Textured and photometric lights

- Texture nodes can vary light colour or intensity across the light surface, and math nodes or animation can drive them (flicker, colour changes).
- **IES Texture**: matches real-world lights from IES files; Mode Internal (text data-block in the .blend) or External (file on disk); the Factor output goes to the Emission Strength.
- Colour temperature: the light has a **Temperature** setting (blackbody, Kelvin) in the common Light settings, so a Blackbody node is not needed for plain colour temperature.

## Gotchas

- Constant falloff lights the whole scene evenly; contain it with light linking (select the light, open the Shading panel in Object properties, create a light linking collection and drag objects onto it).
- Node light looks only appear in Cycles, so Material Preview and EEVEE differ from the Cycles result.

## Verify

Swap Quadratic for Linear: distant walls brighten relative to near ones.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release): render/cycles/light_settings.rst (Nodes section: Light context, Emission to Light Output, limitations), render/shader_nodes/color/light_falloff.rst, render/shader_nodes/textures/ies.rst, render/lights/light_object.rst (Temperature, Shader Editor Sidebar Options), render/lights/light_linking.rst. Fixed: the old "Use Nodes" button in Light properties is not in the current manual; Power-ignored and "hundreds" strength claims removed (not documented); Blackbody Kelvin examples removed. Method: documentation only; no commands were run.

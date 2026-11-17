---
id: creative-arts.animation.blender.gobos-cookies
name: gobos-cookies
category: creative-arts
field: animation
product: blender
tags: [blender, lighting, gobos-cookies, gobo, cookie, light-nodes, projected-texture]
level: practitioner
status: docs-checked
description: "Project patterns from lights in Blender: physical gobo cards with alpha, Cycles light node image projection on spots, and EEVEE-compatible approaches."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/light_settings.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/sampling.html
  - https://docs.blender.org/manual/en/latest/render/lights/light_object.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# gobos-cookies

## Method 1: physical gobo

Place a card with a cutout (window frame, leaves, blinds) between the light and the subject so it casts the pattern as a shadow. Works with any renderer; shadow sharpness follows the light's size (see spot-shape-blend for Radius).

## Method 2: textures in light nodes (Cycles)

In Cycles a light is defined by shader nodes: set the Shader Editor to the **Light** context with a light object selected. The Emission shader (Color, Strength) must connect to the **Light Output** node. Per the manual you can use Texture nodes to vary light colour or intensity across the light surface, mix several Emission shaders, or drive values with math nodes or animation. This allows patterned lights, colour projections and animated flicker.

## Gotchas

- The manual notes the light tree does not account for custom falloff, ray visibility or complex shader node setups including textures, which can increase noise.
- Test with an asymmetric image (an arrow) to catch flipped projection.

## Verify

The arrow test image appears upright on the target wall.

## Checked
2026-10-27, Blender 5.2 manual (blender-v5.2-release RST) render/cycles/light_settings (Nodes: Light context in the Shader Editor, Emission shader, Light Output node, texture nodes can vary colour/intensity across the light) and render/cycles/render_settings/sampling (Light Tree limitation with textures and complex node setups). Removed unconfirmed Use Nodes toggle, projection node recipe, EEVEE statements and material settings.
Method: documentation only; no commands were run.

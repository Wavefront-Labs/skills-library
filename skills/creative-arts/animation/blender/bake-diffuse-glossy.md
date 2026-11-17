---
id: creative-arts.animation.blender.bake-diffuse-glossy
name: bake-diffuse-glossy
category: creative-arts
field: animation
product: blender
tags: [blender, bake-diffuse-glossy, bake-diffuse, bake-roughness, bake-emit, bake-normal, texture-baking, cycles-bake]
level: practitioner
status: docs-checked
description: "Bake individual material channels in Cycles: Diffuse colour only, Glossy, Roughness, Emit and Normal maps, contribution toggles, tangent space and channel swizzle."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/baking.html
  - https://projects.blender.org/blender/blender/src/branch/blender-v5.2-release/intern/cycles/blender/addon/ui.py
  - https://projects.blender.org/blender/blender/src/branch/blender-v5.2-release/source/blender/makesrna/intern/rna_scene.cc
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# bake-diffuse-glossy

Goal: flatten procedural materials into PBR texture sets (base colour, roughness, normal, emission) for export.

## Per-channel bake types

| Map | Bake Type | Settings | Image |
|---|---|---|---|
| Base colour | Diffuse | Contributions: *Color* only (untick Direct, Indirect) | sRGB |
| Roughness | Roughness | none | Non-Color |
| Emission | Emit | none | sRGB or float |
| Normal | Normal | Space Tangent, Swizzle +X +Y +Z | Non-Color |
| Glossy colour | Glossy | *Color* only | sRGB |
| Lit diffuse | Diffuse | Direct + Indirect + Color | sRGB |

With only *Color* selected you get the pass colour, a surface property independent of sampling. Without *Color* you get direct and/or indirect contributions in gray-scale.

## Metallic and other inputs

There is no Metallic bake type. Common trick: temporarily plug the Metallic value (or any scalar) into an **Emission** shader connected to the Material Output, bake *Emit*, then restore the material. Same for AO masks, curvature or custom masks.

## Normal maps

- *Space*: *Tangent* is the default and usually right, because the map then works for animated objects too. *Object* normals are independent of object transformation but depend on deformation. The Normal Map setting on the image texture must match the bake space.
- *Swizzle R, G, B* choose the axis baked into each channel; the defaults are +X +Y +Z. If the target engine expects an inverted green channel, set G to -Y (or flip G in the engine).
- From a high poly: *Selected to Active* with a cage or extrusion (`creative-arts.animation.blender.bake-cage`).

## Gotchas

- A Principled BSDF *Base Color* bake needs the Diffuse bake with *Color* only; leaving Direct or Indirect on bakes lighting into the map.
- Bake Type Normal bakes to an RGB image; keep that image Non-Color.

## Verify

Rebuild a simple material using only the baked maps and compare with the procedural original side by side in Material Preview: matching colour, roughness response and normal detail.

## Checked

2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch) and the 5.2 source UI scripts. Confirmed: Bake type list (no Metallic), Color/Direct/Indirect behaviour, Normal Space Object/Tangent (default Tangent) and Swizzle R/G/B (baking page); -Y swizzle option (rna_scene.cc). Removed unsupported claims about metals baking black, mixed shaders and engine names.

Method: documentation only; no commands were run.

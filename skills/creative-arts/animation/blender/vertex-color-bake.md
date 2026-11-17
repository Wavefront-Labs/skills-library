---
id: creative-arts.animation.blender.vertex-color-bake
name: vertex-color-bake
category: creative-arts
field: animation
product: blender
tags: [blender, texture-baking, vertex-color-bake, bake-to-vertex-colors, cycles-bake, color-attributes, bake-to-color-attributes, active-color-bake]
level: practitioner
status: docs-checked
description: "Bake lighting, AO or materials to color attributes in Blender Cycles: Active Color Attribute target, setup, density limits and uses."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/baking.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/properties/object_data.html
  - https://projects.blender.org/blender/blender/src/branch/blender-v5.2-release/source/blender/editors/object/object_bake_api.cc
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# vertex-color-bake

Goal: store baked AO/lighting/material colour per vertex (no UVs or textures needed).

## Steps
1. Render engine **Cycles**.
2. Object Data > Color Attributes: add one (*Domain*: Vertex stores one colour per vertex, Face Corner one per corner of each face) and make it **active**.
3. Render Properties > Bake: Bake Type (Ambient Occlusion, Combined, Diffuse with Color only, Emit...).
4. Output > **Target: Active Color Attribute**.
5. Bake. The result is written into the active color attribute of the active mesh object.

The active object must be a mesh: other object types have no Color Attributes.

## Density
Each vertex (or face corner) stores one value, so bake detail follows mesh density. Subdivide the target or use the Face Corner domain to separate hard edges.

## Uses
- Game engines: AO/lightmaps in vertex colour multiplied in the shader.
- Masks for shaders without UVs (Geometry Nodes generated meshes).

## Gotchas
- No active color attribute: the bake stops with the error "No active color attribute to bake to".
- Byte Color is RGBA with 8-bit precision; use a float Color attribute for lighting bakes with values above 1.
- Cycles uses the render settings (samples, bounces) for baking, so raise samples for a clean AO.

## Verify
Display the attribute (for example with an Attribute node in a material) and compare against a texture bake of the same type.

## Checked

2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch) and the 5.2 source UI scripts. Confirmed: Target Active Color Attribute and mesh-only restriction (baking page); Domain Vertex/Face Corner and Byte Color 8-bit precision (Object Data page); the "No active color attribute to bake to" error (object_bake_api.cc). Removed unsupported claims about modifiers, denoising and density examples.

Method: documentation only; no commands were run.

---
id: creative-arts.animation.blender.generated-object-coords
name: generated-object-coords
category: creative-arts
field: animation
product: blender
tags: [blender, procedural-texturing, texture-coordinate, generated-object-coords, generated-coordinates, object-coordinates]
level: practitioner
status: docs-checked
description: "Pick the right Blender texture coordinate: Generated, Object (with empty), UV, Normal, Camera, Window, Reflection, and from-instancer coordinates."
sources:
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/input/texture_coordinate.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# generated-object-coords

## Outputs (Texture Coordinate node)

- **Generated**: automatic coordinates from the vertex positions of the undeformed mesh, ranging 0 to 1 over its bounding box; they stick to the surface under animation. Texture nodes with an unconnected Vector input use Generated coordinates.
- **Object**: coordinates from an object (the **Object** field). Often an empty, to place a texture at a point on the surface; the object can be animated to move a texture through a surface.
- **UV**: the active render UV map; use the UV Map node to pick another.
- **Normal**: object-space normal (texture stays fixed on the object as it transforms); also usable on point and spot lights.
- **Camera**: position in camera space. **Window**: shading point location on screen, 0 to 1 left to right and bottom to top (well suited to blending two objects). **Reflection**: reflection vector direction (for environment maps).
- **From Instancer** (Cycles only): for objects instanced from vertices or faces, use the instancer's coordinates. Affects only Generated and UV, and UV only works when instanced from particles or faces.

## Choosing

- Painted or baked textures: UV.
- Procedural on a deforming character: Generated sticks to the surface under animation.
- Moving or projected patterns: Object with an empty.

## Gotchas

- Generated is tied to the bounding box, so a long thin object gets a stretched pattern.
- Some texture nodes show precision issues with certain vector inputs.

## Verify

Scale an object non-uniformly and compare the same texture driven by Generated and by Object coordinates to pick the behaviour you want.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch, docs.blender.org manual en/5.2). Confirmed against input/texture_coordinate and textures/checker, gradient (Generated default): output definitions, Object field, Window range, From Instancer limits (Cycles only, Generated and UV only). Removed the unsupported claims that Object coordinates keep scale under non-uniform scaling, that Generated uses pre-modifier bounds, and the rest-position advice.

Method: documentation only; no commands were run.

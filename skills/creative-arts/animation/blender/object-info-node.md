---
id: creative-arts.animation.blender.object-info-node
name: object-info-node
category: creative-arts
field: animation
product: blender
tags: [blender, shader, object-info-node, object-info, geometry-input-node, attribute-node, random-per-island]
level: practitioner
status: docs-checked
description: "Read per-object and per-geometry data in Blender shaders: Object Info random and colour, Attribute node, Geometry pointiness, random per island."
sources:
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/input/object_info.html
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/input/attribute.html
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/input/geometry.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# object-info-node

## Object Info

Outputs **Location** (world space), **Color** (Object Properties > Viewport Display colour), **Alpha** (that colour's alpha), **Object Index** (Object Properties > Relations > Pass Index), **Material Index** (Material > Settings > Pass Index), **Random** (a float from 0 to 1, unique to each object instance). Works in material shading nodes only, not light or world nodes. Use Random -> Color Ramp for per-instance variation of scattered rocks or leaves.

## Attribute node

- **Attribute Type**: Geometry (mesh attributes), Object (custom property name or RNA path, looked up on the object then its mesh; the `color` attribute gives the Viewport Display colour unless overridden), Instancer (particle system settings, then Geometry Nodes instance attributes, then the instancer object), View Layer (view layer, scene, then world).
- Name = the attribute or property name; outputs Color, Vector, Factor, Alpha.

## Geometry node

Position, Normal, Tangent, True Normal, Incoming, Parametric, **Backfacing** (1.0 when viewed from the back), **Pointiness** (Cycles only; per-vertex curvature approximation, lighter = convex, for dirt and wear maps), **Random per Island** (Cycles only; a random value per connected island, useful for planks, leaves or multi-spline curves). Vector outputs are in world space.

## Recipes

- Per-plank wood variation: Random per Island -> Mapping Location offset.
- Geometry Nodes-driven colour: Store Named Attribute in the node group, then an Attribute node with the same name.
- Backfacing -> Mix: a different inside colour for single-sided leaves.

## Gotchas

- A missing Object or View Layer attribute outputs 0 on every socket, including Alpha.

## Verify

Scatter several instances: each shows a different tint through Object Info Random.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch, docs.blender.org manual en/5.2). Confirmed against input/object_info, input/attribute and input/geometry: output names and meanings, Random range and per-instance behaviour, material-only limitation, attribute types and lookup order, Backfacing, Pointiness and Random per Island (Cycles only). Removed the keyable-colour remark, the claim that Random derives from the object name, and the Pointiness topology remark.

Method: documentation only; no commands were run.

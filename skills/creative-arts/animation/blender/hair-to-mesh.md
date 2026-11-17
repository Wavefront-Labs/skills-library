---
id: creative-arts.animation.blender.hair-to-mesh
name: hair-to-mesh
category: creative-arts
field: animation
product: blender
tags: [blender, hair, hair-curves, hair-to-mesh, hair-cards, curve-to-mesh]
level: practitioner
status: docs-checked
description: "Convert Blender Curves hair to mesh strands or cards with Geometry Nodes: Resample Curve, Curve to Mesh with a profile, tilt, radius and UVs from Spline Parameter."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/curve/operations/curve_to_mesh.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/curve/read/spline_parameter.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/curve/operations/resample_curve.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/curve/write/set_curve_tilt.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/attribute/store_named_attribute.html
  - https://docs.blender.org/manual/en/latest/scene_layout/object/editing/convert.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# hair-to-mesh

## Curves hair to mesh with Geometry Nodes
1. Prepare one curve per strand or card (guides or grooming result).
2. **Resample Curve** (Mode Count, Length or Evaluated) to a uniform point count.
3. **Curve to Mesh** (inputs Curve, Profile Curve, Scale, Fill Caps): with no Profile Curve the result is a chain of edges; a profile such as a **Curve Line** extrudes along each curve to make a flat card.
4. Orient and taper cards with **Set Curve Tilt** and **Set Curve Radius**.
5. UVs: **Spline Parameter** Factor (portion of length at each control point) can drive a coordinate along the strand; write it with **Store Named Attribute** (choose Data Type and Domain, give the target UV map name).
6. Apply the modifier, or use Object > Convert > Mesh on a result that is a curve object.

## Notes
- Curve to Mesh transfers attributes and tags sharp edges from the profile curve.
- Fill Caps closes the ends of a cyclic profile with n-gons.
- Spline Parameter values are per control point, so resample first to get one control point per evaluated point.

## Gotchas
- Object > Convert > Mesh is documented for curve, metaball, surface and text objects; for a Curves hair object use the Curve to Mesh node in a modifier.
- Texture atlas baking, engine alpha handling and LOD decisions are outside the Blender manual; check your engine's documentation.

## Verify
Inspect the resulting mesh in Edit mode: UVs run root to tip and cards face the intended direction.

## Checked

2026-10-27, Blender 5.2 manual (projects.blender.org blender-manual, branch blender-v5.2-release RST) and Python API docs. Confirmed node names, inputs and behaviour for Resample Curve, Curve to Mesh, Curve Line, Set Curve Tilt, Spline Parameter and Store Named Attribute, and the scope of Object > Convert > Mesh. Removed the 8-12 point count, atlas baking, normal transfer, engine alpha sorting and LOD claims, none of which the manual covers.
Method: documentation only; no commands were run.

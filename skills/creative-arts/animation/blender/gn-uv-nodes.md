---
id: creative-arts.animation.blender.gn-uv-nodes
name: gn-uv-nodes
category: creative-arts
field: animation
product: blender
tags: [blender, geometry-nodes, gn-uv-nodes, uv-unwrap-node, pack-islands-node, uv-maps, store-named-attribute, procedural-uv]
level: practitioner
status: verified
description: "Give procedural Geometry Nodes meshes usable UVs: UV Unwrap node with seams, Pack UV Islands, storing as a Face Corner 2D Vector UV map, and Curve to Mesh UV tricks."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/mesh/uv/uv_unwrap.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/mesh/uv/pack_uv_islands.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/attribute/store_named_attribute.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# gn-uv-nodes

Goal: textures work on geometry that is generated in nodes and changes topology.

## UV Unwrap node

- Inputs: **Selection** (faces taking part), **Seam** (edges where the mesh is cut), **Margin**, **Fill Holes**, **Method** (Angle Based, or Conformal using LSCM, which suits simpler objects).
- The node implicitly packs the islands when done and does no aspect ratio correction (do it with Vector Math).
- Seams procedurally: edges whose Edge Angle (radians) exceeds a threshold, or boundaries from the Extrude Mesh Side output.
- The **UV** output is 0..1 per face corner. Blender only recognises it as a UV map if it is stored with **Store Named Attribute** on the Face Corner domain with the 2D Vector data type (there is no 2D Vector socket).

## Pack UV Islands

Inputs: **UV**, **Selection** (only islands containing a selected face change), **Margin**, **Rotate** (the 4.5.14 node has only these inputs; the 5.x manual also lists a Method with Bounding Box, Convex Hull and Exact Shape plus Bottom Left and Top Right bounds, which could not be run here). Useful for texture atlases and preparing geometry for baking.

## Naming the UV map

- Name the stored attribute to match the UV map you want materials to read.
- Primitives (Grid, Cube, Cylinder) have a **UV Map** output; it must be stored with Store Named Attribute on the Face Corner domain to be accessible after the modifier is applied.

## Curve to Mesh UVs

Capture Spline Parameter *Length* on the curve and the profile curve's Factor, combine into a vector (U = profile factor, V = length), store as Face Corner 2D Vector after Curve to Mesh → tiling along tubes.

## Gotchas

- Without storing, the UV field is not recognised as a UV map.
- The UV Unwrap node leaves faces outside its *Selection* untouched.

## Verify

Use the Spreadsheet (Face Corner domain) or a checker texture in Material Preview.

## Checked

2026-10-27, against the Blender 5.3 manual (branch blender-v5.3-release). Confirmed on the UV Unwrap, Pack UV Islands, Grid, Cube and Cylinder pages: inputs, methods, implicit packing, Face Corner 2D Vector storage requirement. Removed unconfirmed claims: edge angle threshold, UV Editor display behaviour, shader and exporter UV lookup details, instance UV retention.

Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): UV Unwrap has Selection, Seam, Margin, Fill Holes and Method Angle Based or Conformal; unwrapping a plane gave UVs spanning 0..1 and storing the result with Store Named Attribute as 2D Vector on the Face Corner domain created a UV map in the evaluated mesh. A Grid UV Map output stored the same way appeared as a Face Corner UV map. Pack UV Islands in 4.5.14 has UV, Selection, Margin and Rotate only: the Method and target-region inputs are 5.x features, kept as manual-only text. Not run: seam recipes, implicit packing, aspect-ratio statement, Curve to Mesh UV recipe.

Method: manual text confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.

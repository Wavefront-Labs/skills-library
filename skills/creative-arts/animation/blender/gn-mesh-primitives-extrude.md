---
id: creative-arts.animation.blender.gn-mesh-primitives-extrude
name: gn-mesh-primitives-extrude
category: creative-arts
field: animation
product: blender
tags: [blender, geometry-nodes, gn-mesh-primitives, mesh-primitive-nodes, gn-extrude-mesh, extrude-mesh-node, scale-elements, procedural-modeling]
level: practitioner
status: verified
description: "Model procedurally with Geometry Nodes mesh primitives (Grid, Cube, Cylinder, Ico Sphere, Mesh Line/Circle) and Extrude Mesh with Top/Side outputs, plus Scale Elements."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/mesh/primitives/index.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/mesh/operations/extrude_mesh.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/mesh/operations/scale_elements.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# gn-mesh-primitives-extrude

Goal: build parametric meshes (panels, buildings, greebles) entirely in nodes.

## Primitives

- **Grid** (planar mesh on XY; Size X/Y, Vertices X/Y are vertex counts, default 3 each; a count of 1 in one direction gives a line of edges and no faces; outputs a UV Map), **Cube** (Size, Vertices X/Y/Z, default 2; 1 on every axis gives a single vertex; UV Map), **Cylinder** and **Cone** (Vertices, Side Segments, Fill Segments, Radius, Depth; *Fill Type* None, N-Gon or Triangles), **UV Sphere**, **Ico Sphere**, **Mesh Line** (*Mode* Offset or End Points; in End Points mode *Count Mode* Count or Resolution), **Mesh Circle**.
- Cylinder outputs boolean **Top**, **Side** and **Bottom** selection fields (Top/Bottom select edges when Fill Type is None); use them instead of computing selections by position.
- Use Transform Geometry for placement.

## Extrude Mesh

- **Mode**: Faces, Edges, Vertices. **Selection** field limits which elements. **Offset** (vector; default = element normal), **Offset Scale**, **Individual** (Face mode only: each face separately instead of connected regions). The node always removes the back faces of the extrusion, unlike the edit-mode tools.
- Outputs **Top** (new vertices, new edges, or moved faces, depending on mode) and **Side** (new edges, new faces, or newly generated side faces) boolean fields — chain them: extrude, then use Top as selection for the next extrude/scale (classic panel inset: Extrude Offset Scale 0 → Scale Elements 0.8 on Top → Extrude -0.02 on Top).
- Capture Normal before extruding if you need the original face direction later (see `gn-fields-attributes`).

## Scale Elements

Scales faces or edges (*Domain*) by **Scale** about a per-element **Center**, either *Uniform* or along an **Axis** (*Single Axis* mode). Connected elements scale together using their average factor and pivot. Combine it with Extrude Mesh in Individual mode.

## Recipe: random greeble panel

Grid 10x10 → Extrude Mesh (Individual, Selection = Random Value Boolean prob 0.3, Offset Scale = Random Value 0.05..0.3) → Scale Elements on Top 0.9 → Set Shade Smooth off.

## Gotchas

- With Individual off, connected selected faces extrude as regions with side faces only on the region boundary; with it on, each face is extruded separately.
- Edge extrusion may give arbitrary normals on the new faces when selected edges have zero or several connected faces; check and fix afterwards.
- The UV Map outputs must be stored with Store Named Attribute on the Face Corner domain to be accessible after applying the modifier.

## Verify

Viewer node on Top selection highlights only the cap faces; Spreadsheet face count matches expectation.

## Checked

2026-10-27, against the Blender 5.3 manual (branch blender-v5.3-release). Confirmed on the Grid, Cube, Cylinder, Mesh Line, Extrude Mesh and Scale Elements pages: socket names, fill types, Top/Side/Bottom outputs, Individual (Face mode only), UV Map storage domain. Removed unconfirmed claims: origin centring, UV outputs on other primitives, zero-length extrude advice and edit-mode shortcut comparisons.

Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): node sockets and enums read from the node types (Grid, Cube, Cylinder, Cone with Fill Type None, N-Gon, Triangles; Mesh Line Offset or End Points with Count or Resolution; Extrude Mesh Mode Faces, Edges, Vertices with Selection, Offset, Offset Scale, Individual and Top and Side outputs; Scale Elements Face or Edge domain with Uniform or Single Axis). Evaluated: a Grid with 1 vertex in X gave a 3-vertex line with 2 edges and no faces (the old text said no mesh), a Cube with 1 vertex per axis gave one vertex, a Cylinder with Fill None selected no Top or Bottom faces but 8 Top and 8 Bottom edges and 8 Side faces, a 3x3 Grid extruded with Individual on gave 25 vertices and 20 faces (4 Top, 16 Side) and with Individual off 17 vertices and 12 faces (4 Top, 8 Side), moving the new faces 0.5 along the normal. Not run (confirmed from the manual only): edge-extrusion normals, UV Map storage after applying, Viewer verification, the greeble recipe.

Method: manual text confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.

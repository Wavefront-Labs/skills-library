---
id: creative-arts.animation.blender.geometry-nodes
name: geometry-nodes
category: creative-arts
field: animation
product: blender
tags: [blender, geometry-nodes, gn, procedural, fields, instances, scattering, set-dressing, instancing, node-groups, realize-instances, proximity, noise-texture, fx-rig, trails, arrays, performance, cel, outline-safe]
level: advanced
status: docs-checked
description: "Geometry Nodes basics: fields vs instances, scattering with Distribute Points on Faces, inspection, performance and baking."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/performance.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/inspection.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/output/viewer.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/point/distribute_points_on_faces.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/instances/instance_on_points.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/input/scene/collection_info.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/baking.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# geometry-nodes

Goal: make Geometry Nodes the procedural backbone of a production: set dressing, debris, instancing, FX rigs. Shots stay light and art-directable.

## Mental model: fields and instances

1. **Fields are functions, not data.** A field such as Position, Normal or a noise output is evaluated per element at the node that consumes it, on whatever domain that node asks for. A field has no value until geometry evaluates it, and the same field can give different results on different domains. When one misbehaves, connect it to a Viewer node and read the Spreadsheet.
2. **Instances are references, not copies.** Instance on Points adds a reference to a geometry at each point: the same geometry many times without duplicating the underlying data. Attributes on the input points are available on the instance domain, so you can vary instances without touching the source.

**Realize vs keep.** Use Realize Instances only when necessary and do operations on instances before realizing them; the performance page recommends avoiding conversion to real geometry unless required.

## Scattering

Typical chain: surface mesh, Distribute Points on Faces, Instance on Points, then output.

- **Distribution Method:** Random is the fastest. Poisson Disk takes a minimum distance into account. Distance Min (Poisson Disk only) is the minimal distance between points; at its default of zero the result matches Random. Density Max (points per square metre, Poisson Disk only) is multiplied by Density, and is capped by Distance Min.
- **Selection** on Distribute Points on Faces limits which face corners receive points. Vertex weights and UV maps of the input transfer to the generated points, so a painted vertex group can drive density or selection.
- **Stable IDs:** the node writes a stable `id` attribute, consistent for remaining points when the mesh is deformed or the density changes. Random Value and Instance on Points use it.
- **Rotation output** is an XYZ Euler built from the normal; its Z axis is arbitrary because a normal cannot set all three axes. Align Rotation to Vector can build a rotation from a direction vector such as the normal.
- **Variants:** Collection Info with Separate Children outputs each child as an instance (sorted alphabetically). Enable Pick Instances on Instance on Points; Instance Index defaults to the point ID, and out-of-range values wrap around. Reset Children removes each child's transform so instances sit at their points. Renaming objects does not re-evaluate the modifier, so trigger an update manually.
- Instance on Points can instance on points in existing instances (nested instancing). To instance objects without geometry such as lights, use Object Info.

## Inspect and debug

- The Viewer node shows intermediate geometry in the Spreadsheet and Viewport. Shift-Ctrl-LMB on a node or socket connects it to the active viewer. With a field input the Geometry socket must be first; domain is chosen automatically where possible.
- Socket inspection, node warnings and timings show data from the last evaluation, and need the node connected to Group Output. Values are not logged during rendering.
- The node timings overlay is turned on in the node editor's overlays popover. It is approximate: field nodes generally do no work themselves, so their time is added to the data-flow nodes they connect to. Frame nodes show the total of their contents.
- The Named Attributes overlay warns when a named attribute may overwrite existing data.
- Do not rely on element order from nodes; it can change between Blender versions. Geometry randomization (needs Developer Extras) tests for that dependence.

## Performance

- Reduce geometry and instance counts; avoid unnecessary evaluations.
- Expensive: Boolean on dense meshes, proximity and raycast nodes on large inputs, simulation zones (evaluated every frame).
- Store reused field results with Capture Attribute; use the Selection input to limit work to needed elements.
- Group related operations into node groups, but deep nesting can hit the evaluation stack limit (adjustable in Preferences).
- Bake finished, expensive parts: the Bake node bakes any portion of the tree and simulation zones have their own baking. The blend-file must be saved before baking, and baked data is not guaranteed readable across Blender versions. Data is only written when the Bake operation runs.

## Verify

- [ ] Viewer plus Spreadsheet confirm each field evaluates on the intended domain.
- [ ] Scatter shot: re-rolling the Seed changes the layout; stable ids keep surviving points unchanged when density changes.
- [ ] Heavy scatter keeps instances unrealized.
- [ ] The timings overlay shows no single node dominating without reason.

## Checked

2026-11-09. Confirmed against the Geometry Nodes Performance, Inspection, Viewer, Distribute Points on Faces, Instance on Points, Collection Info and Baking manual pages: all behaviours above, including node timings caveats, Poisson Disk options, stable id, Pick Instances and Collection Info options, Viewer shortcut, baking caveats. Removed (not stated by the cited pages or unread): density-paint recipe, camera culling, slope masks, FX trail and ring rigs, group naming and asset library conventions, cel outline and inverted-hull guidance, Is Viewport (page was a stub), numeric offsets and ranges, and cross-skill workflow claims.
Method: documentation only; no commands were run.

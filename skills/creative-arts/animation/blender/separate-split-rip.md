---
id: creative-arts.animation.blender.separate-split-rip
name: separate-split-rip
category: creative-arts
field: animation
product: blender
tags: [blender, mesh-editing, separate-join, split-mesh, rip-tool, rip-fill, join-objects, loose-parts]
level: practitioner
status: docs-checked
description: "Break Blender meshes apart: Separate (Selection, By Material, By Loose Parts), Join, Split (Y), and Rip Vertices (V), Rip and Fill (Alt V) and Rip and Extend (Alt D)."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/separate.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/split.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/vertex/rip_vertices.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/vertex/rip_vertices_fill.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/vertex/rip_vertices_extend.html
  - https://docs.blender.org/manual/en/latest/scene_layout/object/editing/join.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# separate-split-rip

Goal: break geometry into parts or objects, or open seams, without duplicate vertices left behind by accident.

## Separate (`P` in Edit Mode, Mesh > Separate)

- **Selection**: disconnects the selected geometry and moves it into a new object.
- **By Material**: one object per material slot, for the whole mesh regardless of selection.
- **By Loose Parts**: one object per independent (disconnected) piece, for the whole mesh regardless of selection.

## Join (`Ctrl J` in Object Mode, Object > Join)

- Merges all selected objects into the active object (it must be selected); all object data is linked to it. Objects must be the same type (mesh, curve, surface or armature).
- Materials, vertex groups, UV and vertex layers are merged. Modifiers, constraints, groups and parent relationships of the joined objects are ignored and not applied to the active object.

## Split (`Y`, Mesh > Split; popover with `Alt M`)

- **Selection** cuts the mesh along the border of the selected faces so they can be moved elsewhere; it also disconnects wire edges, but on edges that are part of a face it only duplicates them.
- **Faces by Edges** cuts along the selected edges; **Faces & Edges by Vertices** cuts along all neighbouring edges of each selected vertex.
- Separate also disconnects, but moves the selection into a new object.

## Rip

- **Rip Vertices** (`V`, Vertex menu): cuts the mesh open along two neighbouring edges of each selected vertex and moves the vertices with the mouse (confirm with `LMB`/`Return`; `RMB`/`Esc` leaves them disconnected in place). With one vertex selected the cut direction follows the mouse; otherwise it follows the selected edges. It cannot rip entire faces out (use Split) and fails on several disjoint islands.
- **Rip Vertices and Fill** (`Alt V`): the same but fills the gap with new faces.
- **Rip Vertices and Extend** (`Alt D`): duplicates the outermost vertices of the selected edges and connects the copies to the originals; neighbouring faces are extended into n-gons rather than new faces being created.

## Gotchas

- Split and Rip leave coincident vertices on purpose; use Merge by Distance where you did not want that.
- Check the result: after Separate, Outliner shows the new objects; Select Linked in each shows only its part.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch, projects.blender.org/blender/blender-manual). Confirmed against the Separate, Join, Split, Rip Vertices, Rip Vertices and Fill and Rip Vertices and Extend pages: options, shortcuts, menu names, join merging rules. Corrected: Rip Edge is named Rip Vertices and Extend; modifiers of joined objects are ignored, not combined. Removed unconfirmed origin, UV-name merge, shape-key and scale remarks.
Method: documentation only; no commands were run.

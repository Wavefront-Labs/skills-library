---
id: creative-arts.animation.blender.extrude-variants
name: extrude-variants
category: creative-arts
field: animation
product: blender
tags: [blender, mesh-editing, extrude, extrude-manifold, extrude-along-normals, extrude-individual, extrude-region]
level: practitioner
status: docs-checked
description: "Pick the right Blender extrude: Region (E), Along Normals, Individual Faces, Manifold, Edges/Vertices, Repeat and Extrude to Cursor (Ctrl RMB), with their options and pitfalls."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/tools/extrude_region.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/tools/extrude_manifold.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/face/extrude_faces_normal.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/face/extrude_individual_faces.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# extrude-variants

Goal: add geometry in the right direction with clean topology, first try.

## The variants (Mesh > Extrude, `Alt E`)

The menu lists only what the current selection allows (faces, edges or vertices).

| Variant | What it does | Use |
|---|---|---|
| Extrude Region (`E`) | extrudes the selection as one; faces move along their averaged normal, axis can be locked | panels, limbs, pushes |
| Extrude Faces Along Normals | moves each vertex along its own normal; *Offset Even* makes each face move the same distance | thickening curved shells |
| Extrude Individual Faces | each face extruded separately | studs, scales, greebles |
| Extrude Manifold | like Extrude Faces but *Dissolve Orthogonal Edges* is on by default, so adjacent faces are split and removed when extruding inward | recesses and pockets without leftover faces |
| Extrude Edges / Extrude Vertices | extrude edges or vertices (vertices become edges, edges become faces) | profiles, wire paths |
| Extrude to Cursor (`Ctrl RMB`) | places a vertex at the cursor, or extrudes the selection toward it; new vertex depth is that of the 3D cursor | quick tubes, retopology strips |
| Extrude Repeat | repeats the extrusion along the view direction (Steps, Offset X/Y/Z, Scale Offset) | stairs, ribs |

The toolbar groups Extrude Region with Extrude Manifold, Extrude Along Normals, Extrude Individual and Extrude To Cursor.

## Redo panel (Along Normals)

- *Flip Normals* (check with the Face Orientation overlay), *Dissolve Orthogonal Edges* (merge new faces into surrounding flat faces, possibly making n-gons), *Offset*, *Offset Even* (toggle with `S` or hold `Alt` while extruding).

## Gotchas

- Region extrude on faces at an angle moves along an averaged normal; use Along Normals for even shells.
- Extrude to Cursor is viewport dependent: the extrusion follows the current view plane.

## Verify

Select > Select All by Trait > Interior Faces selects nothing unexpected after extruding.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch, projects.blender.org/blender/blender-manual). Confirmed against the Extrude, Extrude Region, Extrude Manifold, Extrude Along Normals, Extrude Individual Faces, Extrude to Cursor, Toolbar and Select All by Trait pages. Removed unconfirmed claims about right-click after E, Mirror clipping, and Merge by Distance reporting.
Method: documentation only; no commands were run.

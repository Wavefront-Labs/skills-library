---
id: creative-arts.animation.blender.select-by-attribute
name: select-by-attribute
category: creative-arts
field: animation
product: blender
tags: [blender, selection, select-by-attribute, select-by-trait, select-sharp-edges, faces-by-sides, select-similar]
level: practitioner
status: docs-checked
description: "Select mesh elements by data in Edit Mode: Select All by Trait, By Attribute, Select Sharp Edges and Select Similar options, for cleanup and procedural edits."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/selecting/all_by_trait.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/selecting/similar.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/selecting/sharp_edges.html
  - https://docs.blender.org/api/current/bpy.ops.mesh.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# select-by-attribute

Goal: find mesh elements by property instead of by clicking, as the basis of cleanup and procedural edits.

## Select > Select All by Trait (Edit Mode)

- **Non Manifold** (Vertex and Edge select modes only) with options Extend, Wire, Boundaries, Multiple Faces, Non Contiguous and Vertices.
- **Loose Geometry**: vertices not in any edge, edges not in any face, or faces sharing no edge with another face, depending on the selection mode.
- **Interior Faces**: faces that may have been created inside the mesh.
- **Faces by Sides**: number of sides plus comparison type (Equal, Not Equal, Greater, Less) in the redo panel; the API defaults are 4 and Equal. `Not Equal` to 4 finds triangles and n-gons.
- **Poles by Count**: vertices with an irregular number of edges (*Pole Count*, *Type*: Less Than, Equal To, Greater Than, Not Equal To; *Exclude Non Manifold*).
- **Ungrouped Vertices**: vertices that are in no vertex group.

## Select > By Attribute

Selects elements based on the active boolean attribute (the operator is `mesh.select_by_attribute`; in the 5.2 source it is an entry of the Select menu). Store a selection from Geometry Nodes as a boolean attribute, apply it, then select it in Edit Mode.

## Select > Sharp Edges

Adds edges at sharp corners to the selection. *Sharpness* is the minimum angle between the face normals; coplanar faces measure 0 degrees. The API default is 0.523599 radians (30 degrees). It does not deal with edges manually marked Sharp: select one marked edge and use Select Similar > Sharpness.

## Select Similar (`Shift-G`)

Compares against what is already selected; the list depends on the selection mode.
- Vertex: Normal, Amount of Adjacent Faces, Vertex Groups (membership, weights ignored), Amount of Connecting Edges, Vertex Crease.
- Edge: Length, Direction, Amount of Faces Around an Edge, Face Angles, Crease, Bevel, Seam, Sharpness, Freestyle Edge Marks.
- Face: Material, Area, Polygon Sides, Perimeter, Normal, Coplanar, Flat/Smooth, Freestyle Face Marks.
- Redo panel: *Compare* (Equal; Greater and Less include equal values) and *Threshold*. Face Regions selects other regions with the same topology.

## Recipes

- All edges marked seam: select one, `Shift-G` > Seam.
- All faces using a material: `Shift-G` > Material.
- All triangles: Faces by Sides, Equal, 3.

## Gotchas

- Select Similar needs an initial selection of the right element type.
- Poles by Count and Non Manifold depend on the current selection mode.

## Verify

Check the selected counts in the Statistics overlay against expectations.

## Checked

2026-10-27, against the Blender 5.3 manual (branch blender-v5.3-release) and the Blender 5.2 source (branch blender-v5.2-release; python API 5.2). Confirmed on the Select All by Trait, Select Sharp Edges and Select Similar manual pages and the 5.2 Python API (mesh.select_by_attribute, select_face_by_sides, edges_select_sharp defaults) and 5.2 source menu (By Attribute is a Select menu entry). Corrected: By Attribute is not under Select All by Trait; the Face Map similar option is not listed; the Non Manifold shortcut and the Hidden elements note are removed as unconfirmed.

Method: documentation only; no commands were run.

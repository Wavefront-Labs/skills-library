---
id: creative-arts.animation.blender.custom-normals-from-faces
name: custom-normals-from-faces
category: creative-arts
field: animation
product: blender
tags: [blender, normals, custom-normals, set-from-faces, point-to-target, average-normals, rotate-normals, game-art]
level: practitioner
status: docs-checked
description: "Author custom split normals in Blender Edit mode: Set from Faces, Point to Target, Average (face area, corner angle), Rotate, Merge/Split, copy/paste vectors and face strength."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/normals.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/normals/weighted_normal.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# custom-normals-from-faces

Goal: shading that looks right on low-poly hard surface and stylised meshes without extra geometry.

## Mesh > Normals (`Alt N`) operators

- **Set from Faces**: sets the custom normal of each selected vertex to the average normal of its surrounding selected faces. Option *Keep Sharp Edges*.
- **Point to Target** (`Alt L`): normals point at a target chosen with a key (`M` mouse cursor, `L` pivot point, `O` object origin, `Ctrl LMB` 3D cursor, `Ctrl RMB` a vertex/edge/face). Options *Invert*, *Align*, *Spherize*, *Reset*. Typical use: foliage cards pointing away from the tree centre, stylised faces.
- **Average**: groups face corners by Sharp edges and averages their normals; *Type* is Custom Normal, Face Area or Corner Angle, with *Weight* and *Threshold*.
- **Rotate** (`R` then `N`): rotate the selected normals interactively.
- **Merge** / **Split**: Merge smooths the selected faces and clears Sharp on the selected edges, then averages their normals; Split flat-shades the selected faces and marks the selected edges Sharp.
- **Copy Vector / Paste Vector**: copy one normal and apply to others (consistent shading across seams).
- **Smooth Vectors**: average with neighbouring vertices' normals (*Factor*).
- **Reset Vectors**: back to the default normals.
- **Select by Face Strength / Set Face Strength** (Weak/Medium/Strong): used by the Weighted Normal modifier when *Face Influence* is on.

## Requirements

- Custom normals are managed on the Object Data > *Geometry Data* panel (*Add/Clear Custom Split Normals Data*).

## Gotchas

- Topology edits (extrude, bevel) on areas with custom normals may produce odd interpolated normals; finalise topology first.
- The exporter and the receiving engine must both keep custom normals rather than recalculating them; check the exporter's normals or smoothing option.

## Verify

The *Split Normals* overlay shows vectors as intended; matcap in Solid shading reveals no gradients on flat faces.

## Checked

2026-10-27, Blender manual 5.2 (blender-v5.2-release RST, Editing Normals page). Confirmed: Mesh > Normals menu (Alt N popover); Set from Faces with Keep Sharp Edges; Point to Target (Alt L) targets and Invert, Align, Spherize, Reset; Rotate as R then N; Merge, Split, Average (Type Custom Normal, Face Area, Corner Angle, Weight, Threshold); Copy and Paste Vector; Smooth Vectors Factor; Reset Vectors; Select by Face Strength and Set Face Strength; Geometry Data panel entry. Removed as unconfirmed: the non-uniform scale gotcha and the FBX and glTF option names.

Method: documentation only; no commands were run.

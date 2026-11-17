---
id: creative-arts.animation.blender.weld-modifier
name: weld-modifier
category: creative-arts
field: animation
product: blender
tags: [blender, weld-modifier, weld, modifiers, merge-by-distance, connected-mode, cleanup, kitbash]
level: practitioner
status: verified
description: "Merge coincident vertices non-destructively with Blender's Weld modifier: distance, All vs Connected mode, loose edges only, vertex group, and its place in the stack."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/weld.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/merge.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/selecting/all_by_trait.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# weld-modifier

Goal: a live version of Merge by Distance (M > By Distance) — weld duplicated verts that come from imports, arrays, mirrored parts or Geometry Nodes, while keeping the source editable.

## Settings

- **Distance**: maximum distance between vertices for them to be merged. Increase in steps; too high collapses small details.
- **Mode**: *All* includes all geometry, including loose parts (a full merge by distance). *Connected* only merges along edges, so loose parts are not merged together.
- **Only Loose Edges** (Connected mode): only collapse short edges that are not adjacent to any face; the manual suggests this for stitching cloth-simulation seams.
- **Vertex Group**: only vertices with weight above zero are affected; *Invert* reverses that.

## Typical uses (practice, not from the manual)

- **Imported CAD/STL/OBJ** that arrives with every face split: Weld (All, a small Distance) then Smooth by Angle.
- **Array without Merge** or array of non-aligned pieces: Weld after the Array instead of fighting the Array's merge option.
- **Before Subdivision Surface** on kitbashed parts, so seams between parts subdivide smoothly.
- **After Geometry Nodes** that instance and realize pieces; GN also has a Merge by Distance node if you need it mid-tree.

## Python

`mod = obj.modifiers.new("Weld", 'WELD')`; properties `merge_threshold` (Distance), `mode` ('ALL' or 'CONNECTED'), `loose_edges`, `vertex_group`, `invert_vertex_group`.

## Gotchas

- *Connected* mode does not merge separate loose parts; use *All* to weld separate pieces together.
- The destructive equivalent is *Mesh → Merge → By Distance* (`M`), which also has an *Unselected* option and a *Sharp Edges* option that keeps sharp edges sharp when custom normals are used.

## Verify

Statistics overlay vertex count before/after; Select > Select All by Trait > Non-Manifold on an applied copy should drop to the expected open boundary.

## Checked

2026-10-27, Blender manual 5.2 (blender-v5.2-release RST: Weld modifier, Merge and Clean up pages) and rna_modifier.cc from the 5.2 release branch. Confirmed: Mode All and Connected, Distance, Only Loose Edges, Vertex Group and Invert; Merge By Distance on M with Unselected and Sharp Edges options; Select All by Trait > Non Manifold menu path. Removed as unconfirmed: the 0.001 default, the claim that Connected avoids fusing touching shells, and the Edge Split, normals and thin-solid gotchas.

Run check, 2026-11-01, Blender 4.5.14 LTS headless: two joined cubes with a shared face: 16 vertices become 12 in All mode and stay 16 in Connected mode; vertex group (weight above zero only) and Invert behave as described; Only Loose Edges collapsed a short faceless edge but not a short edge of a face (5 vertices became 4, against 3 without the option); the Mode enum has exactly All and Connected; Merge menu (M) lists By Distance, and the operator has the Unselected and Sharp Edges options.

Method: manual text confirmed from documentation; Weld behaviour run headless in Blender 4.5.14.

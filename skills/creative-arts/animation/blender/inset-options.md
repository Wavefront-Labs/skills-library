---
id: creative-arts.animation.blender.inset-options
name: inset-options
category: creative-arts
field: animation
product: blender
tags: [blender, mesh-editing, inset, inset-options, inset-individual, outset, edge-rail, boundary]
level: practitioner
status: docs-checked
description: "Control Blender Inset Faces (I): thickness, depth, Individual, Outset, Boundary, Offset Even/Relative, Edge Rail, Select Outer and Interpolate for clean panel and window topology."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/face/inset_faces.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# inset-options

Goal: inner loops for windows, panels, buttons and support edges with even width.

## Use

- Face mode, select faces (several disjoint patches work at once), `I` and move the mouse; click or `Return` confirms, `RMB`/`Esc` cancels. Type a value for exact thickness.
- Hold `Ctrl` to adjust **Depth** (moves each selected vertex along its normal, which can resize all faces). `B` toggles Boundary, `O` Outset, `I` Individual; the status bar shows the keys.

## Redo panel options

- **Thickness** and **Depth**.
- **Boundary**: also create border faces at boundary edges (edges that belong to only one face).
- **Offset Even** (on by default): even border width along edges; when off, the width is even at corners instead.
- **Offset Relative**: scales Thickness and Depth per border vertex by the average length of its two neighbouring border edges.
- **Edge Rail**: aligns new edges between border faces with the existing edges between inset faces.
- **Outset**: the border grows outward instead of inward.
- **Select Outer**: selects the new border faces (useful for extruding a frame).
- **Individual**: insets each face separately instead of each connected patch.
- **Interpolate**: interpolates UVs, color attributes, vertex group weights and similar data to the new border vertices.

## Recipes

- Window frame: inset, then extrude the inner face inward.
- Support loops for subdivision on a flat panel: a tiny inset of the face region instead of loop cuts.
- Bolt heads on many faces: Individual inset, then extrude.

## Verify

Select > Select All by Trait > Non Manifold selects nothing new, and the border width reads even in wireframe.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch, projects.blender.org/blender/blender-manual). Confirmed against the Inset Faces page: shortcut and key hints, every option and its meaning, Offset Even default. Removed unconfirmed Mirror-modifier advice and self-intersection claims.
Method: documentation only; no commands were run.

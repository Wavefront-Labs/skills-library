---
id: creative-arts.animation.blender.select-edge-ring
name: select-edge-ring
category: creative-arts
field: animation
product: blender
tags: [blender, selection, select-loops, select-edge-ring, edge-ring, loop-inner-region, boundary-loop, shortest-path]
level: practitioner
status: docs-checked
description: "Select loops, rings, inner regions, boundaries and shortest paths in Blender Edit Mode: Alt and Ctrl Alt click, Boundary Loops, Inner-Region, shortest path, Checker Deselect."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/selecting/loops.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/selecting/linked.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/selecting/checker_deselect.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# select-edge-ring

Goal: grab exactly the loops, rings and regions needed for cuts, seams and edits.

## Loops and rings

- **Edge loop**: `Alt LMB` an edge (Vertex or Edge mode); `Shift Alt LMB` adds. Running it on a boundary edge twice selects the whole boundary. With emulate-3-button-mouse on, double-click `LMB` instead.
- **Face loop**: in Face mode, `Alt LMB` an edge selects the row of faces perpendicular to it. In Vertex mode, Select Edge Rings gives the same result.
- **Edge ring**: `Ctrl Alt LMB` (Edge mode; `Shift Ctrl Alt LMB` adds) selects the parallel edges in the face row perpendicular to the clicked edge. Menu: Select > Select Loops > Edge Rings. To convert a ring to a face loop, switch to Vertex mode, or switch to Face mode while holding `Ctrl`.

## Inner region and boundary

- **Select Loop Inner-Region** (Select > Select Loops): with a closed edge loop selected, selects the faces inside it; *Select Bigger* selects the faces outside instead. If the edges are not a closed loop, all connected faces are selected.
- **Boundary Loops**: expands selected boundary edges (edges with one face) into whole loops; options Extend and Delimit (Seam, Sharp, N-gons, Inner Corners, Outer Corners).
- **Boundary of Selection**: replaces a face selection by the edges around each face island; switches to Edge mode when run from Face mode.

## Shortest path

- Select the start element, then `Ctrl LMB` the destination (Select > Select Linked > Shortest Path). Redo options: *Edge Tag* (Select, Tag Seam, Tag Sharp, Tag Crease, Tag Bevel, Tag Freestyle Edge Mark), *Face Stepping*, *Topology Distance* (fewest edges instead of shortest distance), *Fill Region* (`Shift Ctrl LMB`, all shortest paths), and *Deselected/Selected/Offset* for a dashed pattern.
- Select > Checker Deselect deselects in a repeating pattern from the active element (options Deselected, Selected, Offset).

## Gotchas

- Loops stop at poles and n-gons, so topology dictates which loops exist.
- With emulate-3-button-mouse on, `Alt LMB` does not work; double-click instead.

## Verify

Check the selected-element count in the Statistics overlay against what you expect (for example a ring around a cylinder equals its segment count).

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch, projects.blender.org/blender/blender-manual). Confirmed against the Select Loops, Select Linked and Checker Deselect pages: shortcuts, menu paths, Boundary Loops options, Inner-Region Select Bigger, shortest-path options. Corrected: Checker Deselect options are Deselected/Selected/Offset; the region operator is Select Loop Inner-Region (inside the loop, not the smaller side). Removed the unconfirmed ring-to-loop conversion via Edge Loops and Subdivide advice.
Method: documentation only; no commands were run.

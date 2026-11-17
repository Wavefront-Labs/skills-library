---
id: creative-arts.animation.blender.uv-stitch-weld-align
name: uv-stitch-weld-align
category: creative-arts
field: animation
product: blender
tags: [blender, uv, uv-editor, uv-stitch, uv-weld, uv-align, merge-uvs, straighten]
level: practitioner
status: docs-checked
description: "Clean UV layouts in Blender: Stitch (Alt V), Merge, Align (Shift W), Align Rotation, Split (Alt M), Rip Move UV (V) and Snap (Shift S), with the options that matter."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/uv.html
  - https://docs.blender.org/manual/en/latest/editors/uv/controls/snapping.html
  - https://docs.blender.org/manual/en/latest/editors/uv/overlays.html
  - https://docs.blender.org/manual/en/latest/editors/uv/selecting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# uv-stitch-weld-align

Goal: fewer seams, straight borders and clean shared edges in the UV layout.

## Stitch (`Alt V`, UV > Stitch)

- Joins selected UVs that share vertices. In the redo panel enable *Use Limit* and set *Limit Distance* to restrict stitching by distance.
- Use: reduce seams after Smart UV Project, rejoin a split sleeve.

## Merge (`M` in the UV Editor)

- **At Center** (average position), **At Cursor** (2D cursor), **By Distance** (*Merge Distance*, *Unselected* to merge into unselected UVs, *Shared Vertex* to merge UVs of the same mesh vertex even when their UV coordinates differ). It acts on UVs only, not 3D geometry.

## Align (`Shift W`, UV > Align)

- Axis: *Straighten*, *Straighten X*, *Straighten Y* (line through the selection's endpoints), *Align Auto*, *Align Vertically*, *Align Horizontally* (line through the selection midpoint; Position Mode Mean, Minimum or Maximum).
- **Align Rotation** (UV > Align Rotation): aligns whole islands to the U or V axis; methods Auto, Edge (selected edges to the V axis) and Geometry (X, Y or Z axis).

## Split and Rip

- **Split > Selection** (`Alt M` popover, `Y`): disconnects the selection from the rest of the UV; the border edges are duplicated and the copy stays in place until moved.
- **Rip Move UV** (`V`): separates selected UV elements and enters move mode; it does not work with Sync Selection on.

## Snap

- UV > Snap (`Shift S`): Selected to Pixels (needs a loaded image), Selected to Cursor, Selected to Cursor (Offset), Selected to Adjacent Unselected, Cursor to Pixels, Cursor to Selected, Cursor to Origin.
- The header magnet toggles snapping (hold `Ctrl` for temporary); Snap Target: Increment, Grid or Vertex. Overlays > Grid Shape Source > Pixel makes each grid cell one image pixel.

## Gotchas

- Sync Selection is on by default in 5.2 and changes which UVs a click selects; turn it off for island-level edits (Rip Move UV requires it).
- Stitching islands that differ in scale or rotation distorts the result; check the Display Stretch overlay.

## Verify

Run Seams from Islands and inspect the seam count; stretch overlay unchanged.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch, projects.blender.org/blender/blender-manual). Confirmed against the UV Operators, Selecting UVs, UV Snapping and UV Overlays pages: shortcuts and menus for Stitch, Merge, Align, Align Rotation, Split, Rip Move UV, Snap. Corrected: Stitch is Alt V (V is Rip Move UV); the Merge menu has no Collapse entry; Align entries are Align Vertically/Horizontally. Removed unconfirmed Stitch options (Snap Islands, Midpoint, Clear Seams), the version gate on Align Rotation and the Snap to Pixel popover claim.
Method: documentation only; no commands were run.

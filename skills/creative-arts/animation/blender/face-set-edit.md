---
id: creative-arts.animation.blender.face-set-edit
name: face-set-edit
category: creative-arts
field: animation
product: blender
tags: [blender, sculpting, face-set-edit, face-set-from-masked, face-set-from-visible, face-sets, face-set-expand]
level: practitioner
status: docs-checked
description: "Create and edit sculpt Face Sets in Blender: Draw Face Sets, initialize by loose parts or materials, from masked, grow and shrink, hide and isolate, auto-masking."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/editing/face_sets.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/edit_face_set.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/brushes/draw_facesets.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/editing/sculpt.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# face-set-edit

Goal: partition a sculpt into regions for fast isolation, masking and brush limits.

## Creating

- **Draw Face Sets** brush: each stroke draws a new face set or extends one. Hold Ctrl to keep drawing the face set under the cursor; hold Shift to relax the set edges so they flow along the perimeter.
- **Face Sets menu**: *Face Set from Masked*, *Face Set from Visible*, *Face Set from Edit Mode Selection*.
- *Initialize Face Sets* with a Mode: By Loose Parts, By Face Set Boundaries, By Materials, By Normals, By UV Seams, By Edge Creases, By Edge Bevel Weight, By Sharp Edges, plus a Threshold for the attribute modes.
- Gesture tools (Box, Lasso, Line, Polyline Face Set) create one new set from a drawn area.

## Editing

- **Edit Face Set** tool (Toolbar), Mode: *Grow Face Set* (Ctrl-W), *Shrink Face Set* (Ctrl-Alt-W), *Delete Geometry*, *Fair Positions* (a flat smooth patch; good for trimming dense meshes or Multires where vertex IDs must not change), *Fair Tangency* (as smooth as possible by minimizing tangent changes). **Strength** applies to the fair modes, **Modify Hidden** includes hidden sets.
- **Expand Face Set** by Topology (Shift-W) is the modal Expand operator for face sets; the Alt-W pie menu gathers the face set operations.
- *Randomize Colors* (Face Sets menu) only changes the display colours.
- Relax Face Sets (Mesh Filter) removes jagged lines on set borders.

## Visibility

- **H** hides the face set under the cursor. **Shift-H** hides all sets except the active one; pressed again, when sets are hidden, it shows everything.
- **Alt-H** (or W) shows all. Invert Visible and Show All are also in the Alt-W pie.
- Auto-Masking > Face Sets restricts brushes to the set under the cursor at stroke start.
- Pose and Cloth brushes use face sets for segments (see `creative-arts.animation.blender.sculpt-cloth-pose-brushes`).

## Gotchas

- Face sets are stored in the `sculpt_face_set` attribute (Integer, Face domain). Voxel remesh keeps them with Preserve > Face Sets; Dyntopo loses or corrupts them.
- The overlay opacity is under Viewport Overlays > Sculpt > Face Sets.

## Verify

The overlay shows coloured regions, and Shift-H isolates exactly the intended set.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release branch). Confirmed against sculpt_paint/sculpting/editing/face_sets and sculpt, tools/edit_face_set, brushes/draw_facesets, tool_settings/remesh and modeling attributes reference: menu entries, Initialize modes, Ctrl-W and Ctrl-Alt-W for grow and shrink (the manual does not give Face Set from Masked a shortcut), Shift-W expand (not Shift-Alt-W), Alt-W pie (not an M pie), H, Shift-H, Alt-H, Draw Face Sets modifiers, overlay location, sculpt_face_set attribute, Preserve Face Sets.
Method: documentation only; no commands were run.

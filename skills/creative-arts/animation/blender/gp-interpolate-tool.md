---
id: creative-arts.animation.blender.gp-interpolate-tool
name: gp-interpolate-tool
category: creative-arts
field: animation
product: blender
tags: [blender, grease-pencil, gp-interpolate-tool, interpolate-options, gp-interpolate-flip, inbetweening]
level: practitioner
status: docs-checked
description: "Generate Grease Pencil inbetweens with the Interpolate tool and Interpolate Sequence: layer and selection options, flip mode, smoothing and step."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/draw/tools/interpolate.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/animation/tools.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/animation/interpolation.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/multiframe.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# gp-interpolate-tool

Goal: auto-inbetween strokes between two keys, then clean them up by hand.

## Interpolate (single)
Draw or Edit mode, playhead between two Grease Pencil keyframes: Toolbar **Interpolate** tool (Ctrl-E). Drag left to right to set the factor; release to create a breakdown keyframe. Tool settings:
- **Layer**: Active Layer or All Layers.
- **Only Selected** (Edit mode): interpolate selected strokes only.
- **Exclude Breakdowns**: use only proper keys as extremes.
- **Flip Mode**: reverses interpolation direction; Automatic decides per stroke.
- **Smooth** and **Iterations**: smoothing of the generated strokes.
When curves of different types are interpolated, priority is NURBS, Bezier, Catmull-Rom, then Polyline.

## Interpolate Sequence
Grease Pencil menu > **Interpolate Sequence** (Shift-Ctrl-E) adds a breakdown keyframe on every frame between the previous and next keyframe, or every **Step** frames. Options: Layer, Exclude Break Downs, Flip Mode, Smooth, Iterations, and **Type** (the interpolation method for the sequence; choose from the operator panel list). Step 2 gives animation on twos.

## Stroke pairing
With Multiframe on, the Interpolate tool uses the selection order of strokes from different frames to compute stroke pairs. Keep stroke counts and directions the same between keys; fix with Edit mode Arrange and Switch Direction (Stroke menu).

## Gotchas
- Mismatched stroke counts leave extra strokes popping in; split or duplicate strokes to match.
- Generated frames are Breakdown keyframes (smaller light blue points in the Dope Sheet); use Exclude Breakdowns to keep them from becoming extremes.

## Verify
Scrub the range with onion skin off: strokes move smoothly without flipping direction.

## Checked

2026-10-27, Blender 5.2 manual (projects.blender.org blender-manual, branch blender-v5.2-release RST) and Python API docs. Confirmed tool settings, Ctrl-E and Shift-Ctrl-E, breakdown output, curve-type priority and selection-order pairing under Multiframe. Removed the easing and type list, the None/Flip/Auto flip names (docs name only Automatic), the large-rotation shrink claim and the Generated tag claim.
Method: documentation only; no commands were run.

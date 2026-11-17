---
id: creative-arts.animation.blender.gp-multiframe-editing
name: gp-multiframe-editing
category: creative-arts
field: animation
product: blender
tags: [blender, grease-pencil, gp-multiframe, multiframe-editing, falloff-curve, 2d-animation]
level: practitioner
status: docs-checked
description: "Edit many Grease Pencil keyframes at once with Multiframe: selecting frames in the dope sheet, falloff curves, and sculpt/edit across a range."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/multiframe.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# gp-multiframe-editing

Goal: apply the same correction (move, scale, sculpt, recolour) to a run of drawings instead of frame by frame.

## Enable

1. Select the desired keyframes (for example in the Dope Sheet).
2. Activate the **Multiframe** toggle (faded lines icon) in the 3D Viewport header; its popover holds *Use Falloff*.

With Multiframe on you can: select points across all selected keyframes and edit them; sculpt (brushes affect all strokes in the selected keyframes); weight paint (same); draw (new strokes are added to all selected keyframes, and the Fill tool is applied in all of them); interpolate (select strokes from different frames in the right order, since the Interpolate tool uses selection order to pair strokes).

## Falloff

**Use Falloff**: the effect on the strokes falls off from the current frame as defined by a curve widget; useful for easing a correction in and out.

## Gotchas

- Not all operators support Multiframe.
- If Multiframe stays on, later edits keep affecting the other selected keyframes; turn it off when done.

## Verify

Scrub after the change: each selected keyframe shows the correction.

## Checked

2026-10-27 against the Blender 5.2 manual (Grease Pencil Multiframe page). Confirmed the toggle location and icon, Use Falloff, supported edit, sculpt, weight paint, draw, fill and interpolate behaviour, and the operator-support note. Removed unconfirmed claims about Edit and Sculpt mode headers, specific operator names (Set Thickness, Assign material), holds, and undo performance.
Method: documentation only; no commands were run.

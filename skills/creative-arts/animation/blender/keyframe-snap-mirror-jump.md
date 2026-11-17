---
id: creative-arts.animation.blender.keyframe-snap-mirror-jump
name: keyframe-snap-mirror-jump
category: creative-arts
field: animation
product: blender
tags: [blender, animation, fcurve-snap, dope-sheet-snap, dope-sheet-mirror, extend-keys, snap-keyframes, mirror-keyframes, keyframe-jump, select-columns, dope-sheet, graph-editor]
level: practitioner
status: docs-checked
description: "Edit keys precisely in Blender's Dope Sheet/Graph Editor: Snap (Shift-S), Mirror (Ctrl-M), Extend (E), jump between keys (Up/Down), and column or between-marker selection."
sources:
  - https://docs.blender.org/manual/en/5.2/editors/graph_editor/fcurves/editing.html
  - https://docs.blender.org/manual/en/5.2/editors/dope_sheet/editing.html
  - https://docs.blender.org/manual/en/5.2/animation/animation_editors.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# keyframe-snap-mirror-jump

Goal: whole-frame, tidy timing and fast navigation between keys.

## Snap (Key > Snap, Shift-S)

- **Selection to Current Frame**, **Selection to Cursor Value** (Graph Editor, uses the 2D Cursor), **Selection to Nearest Frame** (rounds each key's time), **Selection to Nearest Second**, **Selection to Nearest Marker**, **Flatten Handles**, **Equalize Handles** (Side, Handle Length, Flatten).
- **Cursor to Selected** (Ctrl-G) and **Cursor Value to Selection** place the 2D Cursor on the average of the selected keys.
- Header **Snapping** toggle for transforms. In the Dope Sheet the dropdown offers Snap To *Frame*, *Second* or *Nearest Marker*, and **Absolute Time Snap** (off: keys move in increments of the Snap To unit and keep their subunit offset; on: keys land on multiples).
- After scaling key timing, use Snap > Selection to Nearest Frame so keys sit on whole frames.

## Mirror (Key > Mirror, Ctrl-M)

- **By Times over Current Frame**, **By Times over First Selected Marker**, **By Times over Zero Time** (horizontal).
- **By Values over Cursor Value**, **By Values over Zero Value** (vertical, Graph Editor).
- Left/right pose mirroring is a different tool: Pose > Paste Flipped.

## Extend (E)

Select keys, put the mouse to one side of the Playhead, press E, move the mouse to move only the keys on that side, LMB confirms and RMB cancels. Handy to make space for new keys.

## Jump and select

- Timeline/playback controls: **Up** jumps to the previous keyframe and **Down** to the next; **Shift-Left / Shift-Right** jump to the start/end frame (or the ends of the preview range); Left/Right step one frame.
- Dope Sheet Select menu: *Columns on Selected Keys* (K), *Column on Current Frame* (Ctrl-K), *Columns on Selected Markers* (Shift-K), *Between Selected Markers* (Alt-K), *Before Current Frame* ([) and *After Current Frame* (]), *Select Linked* (L: keys on the same channel as a selected key), *Select by Type*.
- Graph Editor has Select Linked (keys on the same curve) in its Select menu.
- Dope Sheet Key > **Slide** (Shift-T): stretches one set of keys while compressing the adjacent set, keeping the combined duration.

## Gotchas

- Scaling keys in the Dope Sheet changes only time (pivot is the Playhead), not values.
- The keys that jump-to-keyframe visits depend on which channels are shown and selected.

## Verify

Dope Sheet: all keys sit on whole frames; a mirrored selection reads as reversed timing on scrub.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release source): Snap and Mirror menu items and Shift-S/Ctrl-M, Extend E, Dope Sheet snap popover and Absolute Time Snap, jump shortcuts, Select menu items, Slide Shift-T. Removed as unconfirmed: subframe jitter claim, Alt-click column selection, mirror swapping remark, 4.x labels. Corrected: the Mirror menu lists Zero Time and Zero Value as the zero references.
Method: documentation only; no commands were run.

---
id: creative-arts.animation.blender.gp-timing-holds
name: gp-timing-holds
category: creative-arts
field: animation
product: blender
tags: [blender, grease-pencil, gp-timing, gp-on-twos, hold-frames, dope-sheet, time-offset]
level: practitioner
status: docs-checked
description: "Time Grease Pencil animation in the Dope Sheet: holds, on twos, blank and duplicate keyframes, retiming with snap and slide, and Time Offset loops."
sources:
  - https://docs.blender.org/manual/en/latest/editors/dope_sheet/modes/grease_pencil.html
  - https://docs.blender.org/manual/en/latest/editors/dope_sheet/editing.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/animation/tools.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/edit/time_offset.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/draw/introduction.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# gp-timing-holds

Goal: exposure-sheet-style timing control after drawing.

## Basics
A Grease Pencil keyframe holds its drawing until the next keyframe, so holds are just gaps. Dope Sheet > **Grease Pencil** mode lists the object and its layers as channels; the header has Add/Remove Layer, Move Layer and Isolate Layers.
- Scaling keys in the Dope Sheet moves them in time only, with the playhead as pivot; **Slide** (Shift-T) stretches one part of a key range while compressing the other.
- **Insert Blank Keyframe** (Shift-I; Stroke > Animation): blank key on the active layer at the current frame (or the next frame if one exists), with Duration and an All Layers option.
- **Duplicate Active Keyframe**: copies the last keyframe's strokes to the current frame (Active or All layers).
- Pressing I over the Dope Sheet inserts a key: a copy of the active frame when Additive Drawing is enabled, otherwise a blank frame.
- **Additive Drawing** (header): new frames start from the previous drawing.
- Dope Sheet Copy and Paste (Key menu) move frames between layers or objects; paste goes into selected layers.

## Ones vs twos
Keys every 2 frames give twos (12 drawings per second at 24 fps). Interpolate Sequence with Step 2 generates on twos.

## Snapping
Dope Sheet Snap: Frame, Second or Nearest Marker; Absolute Time Snap controls whether keys snap to multiples. Snap after scaling to avoid fractional-frame keys.

## Time Offset modifier
Modes: Regular, Reverse, Fixed Frame (Frame must be animated to change), Ping Pong, Chain (Repeat). Also Frame Offset, Scale (playback speed), **Keep Loop**, and **Custom Range** (Frame Start/End) for looping a short cycle. Influence filters (such as layer) limit what it affects. Handy for mouth shapes and desynchronising copies.

## Gotchas
- Fractional keys from scaling hold oddly; snap them.
- Additive Drawing copies strokes into each new key, which grows file size.

## Verify
Play back with onion skin off; the timing chart and Dope Sheet spacing agree.

## Checked

2026-10-27, Blender 5.2 manual (projects.blender.org blender-manual, branch blender-v5.2-release RST) and Python API docs. Confirmed Dope Sheet Grease Pencil mode behaviour (I key, Additive Drawing), Shift-I blank keyframe, Duplicate Active Keyframe, scaling around the playhead, Shift-T Slide, Snap options, and all Time Offset modes and options (Keep Loop, Custom Range). Removed the G/S/X/Shift-D shortcut claims, the Ctrl-snap claim and the object-transform note; the 4.3 gate on Chain was dropped.
Method: documentation only; no commands were run.

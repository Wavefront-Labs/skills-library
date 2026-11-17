---
id: creative-arts.animation.blender.grease-pencil-animation
name: grease-pencil-animation
category: creative-arts
field: animation
product: blender
tags: [blender, onion-skinning, gp-interpolate, frame-by-frame, interpolate-sequence, grease-pencil, gpencil, 2d-animation, keyframes, exposure-sheet, layers, timing, inbetweens]
level: advanced
status: docs-checked
description: "Frame-by-frame 2D animation with Grease Pencil in Blender: keyframes, Dope Sheet GP mode, onion skinning, Interpolate Sequence, blank and duplicate keyframes."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/animation/introduction.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/animation/tools.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/properties/onion_skinning.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# grease-pencil-animation

Goal: animate drawn frames with a workflow as fast as paper: draw keys, see neighbours, generate inbetweens, retime without redrawing.

## Ways to animate a Grease Pencil object

Whole-object transforms, drawing frame by frame (traditional), deforming points, and inherited animation (parent, hook, armature; useful for cut-out). This skill covers frame by frame.

## Keyframes

- Traditional animation uses keyframes that hold the strokes at a frame or frame range.
- With **Auto keyframe** on, every stroke you draw in Draw Mode adds a new keyframe at the current frame on the active channel. With it off you must add a keyframe manually or new strokes go on the active keyframe.
- The Dope Sheet has a Grease Pencil mode; its channels correspond to the active 2D layer of the object.
- The *File > New > 2D Animation* template starts with a Grease Pencil object, Onion Skinning on, Auto Keyframe on, in camera view.
- Draw Mode options: **Additive Drawing** (new frames start from the strokes of the previous/active frame), **Multiframe** (draw on several frames; button next to the modes selector), **Add Weight Data** (new strokes get weights from the current vertex group; handy for cut-out).
- Edit Mode **Multiframe** edits several frames at once, for example to reposition drawings.

## Stroke > Animation tools (Draw, Edit, Sculpt modes)

- **Insert Blank Keyframe (Active Layer)**, `Shift I`: blank keyframe on the active layer at the current frame; if a keyframe already exists there, the blank one is added on the next frame. *All Layers* option, or the separate (All Layers) entry.
- **Duplicate Active Keyframe**: copies the strokes of the last keyframe to the current frame (*Mode*: Active or All layers).
- **Delete Active Keyframe (Active Layer)**, `Alt I`: deletes the last keyframe in the Dope Sheet, or the current one if you are on one (*Type*: Active Frame or All Active Frames). The All Layers version is `Shift Delete`.
- **Bake Object Transform to Grease Pencil** (Object > Animation): applies object-level transform animation within a frame range to Grease Pencil keyframes (Start/End Frame, Step, Only Selected Keyframes, Target Frame, Projection Type).

## Interpolate Sequence (Grease Pencil menu, `Shift Ctrl E`, Draw or Edit Mode)

Interpolates strokes between the previous and next keyframe by adding multiple keyframes; a breakdown keyframe is added on every frame between them. Options: *Step* (frames between generated frames), *Layer*, *Exclude Break Downs* (exclude existing breakdowns as interpolation extremes), *Flip Mode* (invert the destination stroke so start and end match the source), *Smooth* and *Iterations* (smoothing of new strokes to reduce jitter), *Type* (interpolation method used the next time it runs).

## Onion skinning

The main show/hide switch is in the viewport Overlays, but onion skinning is per layer: its visibility is toggled in the layer list. Turn it off on background and effects layers so ghosts show only what you animate.
- **Mode**: *Keyframes* (keyframes in the range set by Before/After), *Frames* (frames in that range), *Selected* (only keyframes manually selected in the Dope Sheet).
- *Keyframes Before/After* sets how many frames or keyframes to show each side. *Opacity* controls ghost opacity. *Filter by Type* limits which keyframe types are shown.
- *Custom Colors*: Before/After colours. *Display*: *Fade* (ghosts decrease in opacity the further from the current frame) and *Show Start Frame* (on the last frame, shows the first keyframe as a ghost; for loops).

## Worked example (from the manual)

Bouncing ball: set the Timeline range 1 to 24, draw the ball upper left (extreme), at frame 12 draw a squashed ball bottom centre (breakdown), at frame 24 draw it upper right (extreme), then draw the inbetweens using the onion skin ghost as reference. Press Space to play.

## Verify

- Dope Sheet GP mode shows diamonds per layer in the intended rhythm.
- Onion skinning shows only the intended ghosts, only on the animated layer.
- After Interpolate Sequence, generated frames are breakdown keyframes and sit between the two source keys.

## Checked

2026-11-09. Confirmed against the three cited Blender manual pages (raw RST). Corrected: Insert Blank Keyframe is `Shift I` under Stroke > Animation (not plain `I`); the onion option formerly called Loop is *Show Start Frame*. Removed unconfirmed claims: keyframe type shortcuts and colours, the Interpolate tool and its stroke-pairing rules, Time Offset modifier retiming, draw-mode speedups, Fill and eraser options, export notes, and the stepped-timing (ones, twos) guidance.
Method: documentation only; no commands were run.

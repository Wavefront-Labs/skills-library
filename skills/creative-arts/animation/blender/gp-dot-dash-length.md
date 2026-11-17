---
id: creative-arts.animation.blender.gp-dot-dash-length
name: gp-dot-dash-length
category: creative-arts
field: animation
product: blender
tags: [blender, grease-pencil, gp-dot-dash, gp-length-modifier, build-on, gp-modifiers]
level: practitioner
status: docs-checked
description: "Make dashed, dotted and growing Grease Pencil lines: Dot Dash segments (dash/gap/radius/material) and Length modifier (extend/shrink, curvature, random)."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/generate/length.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/generate/dash.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/generate/build.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# gp-dot-dash-length

Goal: technical dashed lines, animated draw-on and overshoot strokes.

## Dot Dash modifier

- A list of **Segments** (plus/minus buttons); each has **Dash** (consecutive original points included), **Gap** (points skipped after it), **Radius** and **Opacity** (factors applied to the original point values), **Material Index** (-1 keeps the existing material) and **Use Cyclic** (close the segment).
- **Offset**: starting offset of the pattern.
- Dash and Gap count points, not distance, so uneven point spacing gives uneven dashes.

## Length modifier

- **Mode**: *Absolute* (geometry space) or *Relative* (ratio of the stroke length).
- **Start / End**: length added at that end; a negative value shrinks the stroke.
- **Used Length**: portion of the stroke used to compute the extension direction.
- **Curvature**: extension follows the stroke curvature (*Point Density*, *Segment Influence*, *Filter Angle*, *Invert*).
- **Random Offsets**: *Random Offset Start/End*, *Random Noise Offset*, *Seed*, *Randomize* (re-randomise over time) with *Step* (frames between recalculations).

## Build modifier (related)

*Mode* Sequential, Concurrent or Additive; *Transition* Grow, Shrink or Vanish (Sequential and Concurrent only); *Timing* Natural Drawing Speed (Sequential and Additive only), Number of Frames, Percentage Factor or Time Alignment (Concurrent only); optional *Custom Range* and *Fade*.

## Verify

Animate Offset or the Length values and scrub: dashes slide and strokes grow as expected.

## Checked

2026-10-27 against the Blender 5.2 manual (Dot Dash, Length and Build modifier pages). Confirmed all listed options and their semantics. Removed unconfirmed claims about resampling with Simplify, the Overshoot option, direction switching, negative length deleting strokes and the "4.x" Natural Drawing Speed version note.
Method: documentation only; no commands were run.

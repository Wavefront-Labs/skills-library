---
id: creative-arts.animation.blender.vse-transform-effect
name: vse-transform-effect
category: creative-arts
field: animation
product: blender
tags: [blender, vse, sequencer, vse-transform-effect, transform-strip, keyframes]
level: practitioner
status: docs-checked
description: "Animate position, scale and rotation in the VSE with the built-in strip Transform panel: keyframing, filter choice, pivot point, and the effect-strip list in 5.2."
sources:
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/strip_properties.html#transform
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/effects/index.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# vse-transform-effect

Goal: animated moves, zooms and rotations of strips in an edit.

## Strip transform (the current way)

Every visual strip has **Position X/Y**, **Scale X/Y**, **Rotation**, **Mirror** and **Filter** in Sidebar > Strip > Transform (see vse-strip-transform-crop).

The 5.2 manual's list of effect strips (Multicam, Speed Control, Glow, Gaussian Blur, Add, Subtract, Multiply, Alpha Over and Under, Color Mix, plus the Transitions) does not include a Transform effect strip, so use the strip's own Transform panel. Older projects that used a Transform effect should be checked when opened in a new version.

## Animating

- Hover over a property and press I to key it (the manual uses this for strip properties such as sound volume and opacity).
- Rotation and scale in the Preview happen around the **Pivot Point** set in the header (Bounding Box Center, Median Point, 2D Cursor or Individual Origins).
- Ken Burns move on a still: key Scale and Position over the strip duration. Use linear interpolation for constant drift or an ease for a settle.
- The **Filter** (Auto, Nearest, Bilinear, Cubic Mitchell, Cubic B-Spline, Box) controls how pixels are sampled when scaled or rotated.

## Gotchas

- Re-check animation after retiming or moving strips in time.
- Scaling up beyond the source resolution is soft.

## Verify

Play the animated move: smooth, no jumps at keyframes, and the image stays sharp at the largest scale.

## Checked

- Date: 2026-10-27. Documentation: Blender 5.2 manual (blender-v5.2-release branch of blender-manual).
- Confirmed: Transform panel fields and Filter list, key-by-hover with I for strip properties, Pivot Point options, and that the 5.2 effect-strip list has no Transform effect. Removed the Transform effect option list, the 2.92 version gate, the Origin field and the keys-on-scene-timeline claim, which the 5.2 manual does not document.
- Method: documentation only; no commands were run.

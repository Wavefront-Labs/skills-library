---
id: creative-arts.animation.blender.gp-sculpt-mode
name: gp-sculpt-mode
category: creative-arts
field: animation
product: blender
tags: [blender, grease-pencil, gp-sculpt-mode, gp-sculpt, gp-smooth, gp-grab]
level: practitioner
status: docs-checked
description: "Reshape Grease Pencil strokes in Sculpt mode: Smooth, Thickness, Strength, Randomize, Grab, Pull, Twist, Pinch and Clone brushes, selection masks and auto-masking."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/sculpting/introduction.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/sculpting/brushes.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/sculpting/tool_settings/brush.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/multiframe.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# gp-sculpt-mode

Goal: refine drawn lines and shapes without redrawing.

## Brushes (Essentials library)
| Brush | Use |
|---|---|
| Smooth Stroke | Smooths point positions inside the brush |
| Thickness Stroke | Increase or decrease point thickness |
| Strength Stroke | Increase or decrease point transparency (alpha) |
| Randomize Stroke | Moves points randomly to add noise |
| Grab Stroke | Selects points on mouse-down and drags them with the pointer (like Proportional Editing) |
| Pull Stroke | Moves points in the direction of the brush stroke |
| Twist Stroke | Twists points counter-clockwise or clockwise |
| Pinch Stroke | Pulls points towards the brush centre; inverse is Inflate |
| Clone Stroke | Pastes strokes from the clipboard at the brush centre; copy them first with Ctrl-C |

## Brush settings
Size (F, pixels), Strength (Shift-F), Use Falloff, Direction (Add or Subtract; Ctrl inverts the stroke toggle). **Sculpt Strokes** filters (Affect Position, Strength, Thickness, UV) apply to Smooth and Randomize only; with none selected, Affect Position is the default.

## Masking
- **Selection Mask** (keys 1, 2, 3): restrict sculpting to selected points or strokes; select with the toolbar selection tools.
- **Auto-Masking** (header, Shift-Alt-A pie): Stroke, Layer, Material, Active Layer, Active Material; modes combine, and masks are rebuilt for every tool use.
- U changes the active material.

## Multiframe
The Multiframe toggle (faded lines icon) makes brushes affect all strokes in the selected keyframes; Use Falloff fades the effect away from the current frame. Not every operator supports it.

## Gotchas
- Strokes with few points sculpt coarsely; use Stroke > Subdivide first.
- Sculpting changes the keyframe active on the current frame; on a held frame that is the earlier key.

## Verify
Toggle onion skin to compare before and after shapes across frames.

## Checked

2026-10-27, Blender 5.2 manual (projects.blender.org blender-manual, branch blender-v5.2-release RST) and Python API docs. Confirmed brush names (Pull Stroke, not Push), settings, Sculpt Strokes filters limited to Smooth and Randomize, Selection Mask, Auto-Masking options and Shift-Alt-A, Multiframe falloff. Removed the Alt-click selection and 4.3 gates and the claim that Smooth with Position off does nothing (docs say Affect Position is the default).
Method: documentation only; no commands were run.

---
id: creative-arts.animation.blender.fcurve-handles-extrapolation
name: fcurve-handles-extrapolation
category: creative-arts
field: animation
product: blender
tags: [blender, graph-editor, fcurve-handle-types, auto-clamped, aligned-handles, fcurve-extrapolation, extrapolation, constant-extrapolation, linear-extrapolation]
level: practitioner
status: docs-checked
description: "Control Blender F-curve shape with handle types (V menu), Handle Smoothing and extrapolation (constant, linear, cyclic) to fix overshoot and drift."
sources:
  - https://docs.blender.org/manual/en/5.2/editors/graph_editor/fcurves/properties.html
  - https://docs.blender.org/manual/en/5.2/editors/graph_editor/channels/editing.html
  - https://docs.blender.org/manual/en/5.2/editors/graph_editor/fcurves/editing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# fcurve-handles-extrapolation

Goal: curves that ease and settle where you want, without overshoot or unintended motion before/after the keys. Broader polish workflow is in `graph-editor-polish`.

## Handle types (Graph Editor, select keys, V or Key > Handle Type)

Handles matter when the key's interpolation is Bezier (the default interpolation).

- **Automatic**: automatic handles that produce smooth curves; can overshoot.
- **Auto Clamped**: automatic handles clamped to prevent overshoots and direction changes (S-shapes) between keys. The manual recommends it as the everyday choice.
- **Vector**: automatic handles that produce straight segments, like linear interpolation (impacts, bounces).
- **Aligned**: handles stay collinear when you move them.
- **Free**: each handle moves independently.
- Each key has its own Left/Right Handle Type in Sidebar > F-Curve > Active Keyframe. Dragging an automatic handle works without changing its type first.
- **Handle Smoothing** (Sidebar > F-Curve > Active F-Curve) affects Automatic and Auto Clamped handles: *None* (only adjacent keys are considered) or *Continuous Acceleration* (solves for smoother curves, but a key edit can ripple over a long stretch; stopped by Free, Aligned and Vector keys and by Auto Clamped extremes).
- Key > Snap > **Flatten Handles** flattens Bezier handles of selected keys; **Equalize Handles** sets equal handle length.

## Extrapolation (Channel > Extrapolation Mode, Shift-E)

- **Constant** (default): continue at the first/last key's value.
- **Linear**: continue in a straight line with the slope of the first/last key (constant-speed wheels, propellers, drifts).
- **Make Cyclic** / **Clear Cyclic**: adds or removes a Cycles modifier (see `fcurve-cycles-modes`).

## Fixes

- Overshoot in a hold: set the hold keys to Auto Clamped or Vector, or flatten their handles.
- "Floaty" ease into a contact: switch to Free or Aligned and pull the incoming handle steeper.
- Object keeps sliding after the last key: extrapolation was set to Linear; set it to Constant.

## Verify

Graph Editor with View > Show Extrapolation: the curve before and after the keys behaves as intended; no bump past a hold's value with Auto Clamped.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release source): handle type descriptions, V and Key > Handle Type, Handle Smoothing modes, Bezier default, extrapolation modes and Shift-E, Flatten and Equalize Handles. Removed as unconfirmed: the Default Handles preference and which handle type is default, the claim that linear extrapolation follows the end handle.
Method: documentation only; no commands were run.

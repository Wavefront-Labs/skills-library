---
id: creative-arts.animation.blender.weight-paint-brush-gradient
name: weight-paint-brush-gradient
category: creative-arts
field: animation
product: blender
tags: [blender, weight-paint, weight-brush-gradient, weight-gradient, sample-weight, weight-blend]
level: practitioner
status: docs-checked
description: "Control Blender weight-paint brushes: Draw blend modes, Blur, Average and Smear, the Gradient tool (linear or radial), sampling weights and groups."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/weight_paint/brushes.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/weight_paint/tools.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/weight_paint/editing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# weight-paint-brush-gradient

Goal: precise skin weights with the fewest strokes.

## Brush types
- **Draw** (Essentials brush *Paint*): paints the Weight value. **Blend** modes: Mix (Weight is the target weight; at Strength 1.0 it is painted immediately, and Weight 0.0 does nothing), Add (adds Weight, never above 1.0), Subtract (never below 0.0), Lighten (only weights below the target change), Darken (only weights above the target change), Multiply, Blur.
- **Blur**: smooths weights of adjacent vertices; Weight is ignored, Strength sets the amount.
- **Average**: paints the average of all weights under the brush.
- **Smear**: drags weights like a finger-painting tool.
- Brush Strength can be changed interactively with Shift-F. Brush settings include **Front Faces Only**; turn it on to avoid painting through thin geometry.
- Weight Paint options: **Auto Normalize** keeps deform weights summing to 1 (see weight-normalize); **Restrict** limits painting to vertices belonging to the selected vertex group.

## Gradient
Toolbar **Gradient** tool (type **Linear** or **Radial**), or the Weights menu entries Gradient (Linear) and Gradient (Radial). It blends the weights of selected vertices with unselected vertices; the gradient starts at the current Weight and blends out to nothing. Lower **Strength** mixes the gradient in with existing weights, like the brush.

## Sampling
- Toolbar **Sample > Weights**: sets the brush Weight to the weight under the cursor (shown in tool settings). Menu: Weights > Sample Weight, Shift-X.
- **Sample > Vertex Group**: lists the vertex groups under the cursor to pick from. Menu: Weights > Sample Group, Shift-Ctrl-X.
- Weights > Set Weight (Ctrl-X) fills the active group with the current paint weight.

## Bone workflow
Armature in Pose Mode (Ctrl-Tab), Lock Object Modes off (Edit menu), mesh in Weight Paint Mode, Bone Selection on in the header, then Alt-LMB (or Shift-Ctrl-LMB) on a bone to make its group active. Only one bone is selectable this way. Enable In Front on the armature if bones are hidden inside the mesh. A bone without a vertex group gets one when you start painting.

## Gotchas
- You paint the active vertex group; check which is highlighted.
- Overlays > Weight Paint: **Zero Weights** shows unreferenced and zero-weighted areas in black, and **Show Weight Contours** draws isolines of equal weight, which reveal variations too small to see in colour.

## Verify
Pose the rig to extremes; the contour overlay should show smooth, evenly spaced isolines across the joint.

## Checked
Date: 2026-10-27. Documentation: Blender manual (Weight Paint brushes, tools, editing, options, usage; Overlays), branch blender-v5.2-release. Confirmed: blend mode semantics, brush types, Gradient and Sample tool behaviour and shortcuts, Restrict, Shift-F strength, Front Faces Only (brush settings), overlay options, bone-selection workflow. Removed unconfirmed claims: Radius shortcut, Ctrl invert behaviour, Projected falloff comparison, "Blur needs connected vertices", and the Shift+click sample keymap.
Method: documentation only; no commands were run.

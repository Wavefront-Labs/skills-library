---
id: creative-arts.animation.blender.gp-weight-paint-armature
name: gp-weight-paint-armature
category: creative-arts
field: animation
product: blender
tags: [blender, grease-pencil, gp-weight-paint, gp-armature, cutout-animation, rigging]
level: practitioner
status: docs-checked
description: "Rig Grease Pencil drawings to bones: Armature Deform parenting, Armature modifier, GP weight paint brushes and Weights menu, Add Weight Data and cut-out setups."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/weight_paint/introduction.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/weight_paint/brushes.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/weight_paint/tool_settings/brush.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/weight_paint/tool_settings/options.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/weight_paint/weights_menu.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/deform/armature.html
  - https://docs.blender.org/manual/en/latest/animation/armatures/skinning/parenting.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/draw/introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# gp-weight-paint-armature

Goal: deform 2D drawings with bones (cut-out or puppet animation) instead of redrawing every frame.

## Setup
1. Draw the character, ideally parts on separate layers.
2. Add an armature with bones in the drawing plane (Front view).
3. Object mode: select the Grease Pencil object, then the armature (active), Ctrl-P and an Armature Deform option (With Empty Groups, or With Automatic Weights). The manual describes Armature Deform parenting as creating the Armature modifier and bone-named vertex groups; check the result on the Grease Pencil object. Alternatively add the Grease Pencil **Armature modifier** yourself: Object, Bind to Vertex Groups and/or Bone Envelopes.

## Weight Paint mode
Painting on strokes automatically adds weights to the active vertex group, creating one if needed. Default display: blue unweighted, red fully weighted. Brushes (Essentials): Paint Point Weight, Blur Point Weight, Average Point Weight, Smear Point Weight. Brush settings: Size (F), Strength, Use Falloff, **Weight** (Ctrl-F; Ctrl-RMB samples the weight under the cursor), Direction (Add or Subtract, D). Option **Auto Normalize** keeps deforming groups summing to one while painting. Multiframe paints several keyframes.
In Edit mode the **Weights** menu has Normalize All, Normalize, Invert, Smooth and Sample Weight (Shift-X).
Draw mode option **Add Weight Data** gives new strokes the current vertex group and weight, useful so new drawings join the rig.

## Cut-out alternative
Instead of weights, parent whole layers to bones (see gp-layer-parenting). Mix both: rigid hands, weighted elbows.

## Gotchas
- Bones not lying in the drawing plane rotate strokes out of plane.
- Strokes with few points deform in kinks; Subdivide before painting weights.
- Strokes drawn after binding have no weights unless Add Weight Data is on.
- Automatic weights are distance-based and mix overlapping parts; paint them clean.

## Verify
Rotate each bone 45 degrees: only its part moves, joints bend smoothly, nothing leaves the plane.

## Checked

2026-10-27, Blender 5.2 manual (projects.blender.org blender-manual, branch blender-v5.2-release RST) and Python API docs. Confirmed weight brush names and settings, Auto Normalize, Weights menu, Armature modifier Bind options, Add Weight Data and generic Armature Deform parenting behaviour. The manual does not say Armature Deform parenting is specific to Grease Pencil, so it is stated generally. Removed the Ctrl-G Assign claim and the tool list Draw/Blur/Average/Smear.
Method: documentation only; no commands were run.

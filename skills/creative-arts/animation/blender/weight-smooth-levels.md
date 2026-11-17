---
id: creative-arts.animation.blender.weight-smooth-levels
name: weight-smooth-levels
category: creative-arts
field: animation
product: blender
tags: [blender, weight-paint, weight-smooth, weight-levels, quantize-weights, invert-weights]
level: practitioner
status: verified
description: "Fix skin weights with Blender's Weights menu operators: Smooth (Factor, Iterations, Expand/Contract), Levels (Offset, Gain), Quantize, Invert and Subset options."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/weight_paint/editing.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# weight-smooth-levels

Goal: global, repeatable weight corrections instead of brush passes.

These are in the **Weights** menu (Edit Mode and Weight Paint Mode). Several take a **Subset** (Active Group, Selected Pose Bones, Deform Pose Bones, All Groups) in the Adjust Last Operation panel, and all work with vertex or face selection masking, operating only on selected vertices or faces.

## Smooth
Blends the weights of selected vertices with the average of adjacent (unselected) vertices. The manual says it requires vertex selection to be enabled; in 4.5.14 the operator (`vertex_group_smooth(group_select_mode=, factor=, repeat=, expand=)`) ran in Edit Mode in both Vertex and Face select modes, and its poll was False in Object Mode.
- **Factor**: 0.0 keeps the original weights, 1.0 fully adopts the average, between blends proportionally.
- **Iterations**: repeat count; higher is smoother but can lose fine detail.
- **Expand/Contract**: positive values expand the selection to neighbouring vertices, negative contract it.
Typical use: select an edge loop at a joint and smooth with a moderate Factor.

## Levels
Adds an offset and a scale: **Offset** (range -1.0 to 1.0) is added to all weights and **Gain** multiplies them in the Subset. The result is always clamped to 0.0 to 1.0. Tested: the result was (weight + Offset) x Gain, so with Offset 0.3 and Gain 2 a weight of 0.1 became 0.8 and 0.5 became 1.0; with Offset -0.5 a weight of 0.5 became 0.0.

## Quantize
**Steps** is the number of steps between 0 and 1; Steps 5 allows 0.0, 0.2, 0.4, 0.6, 0.8, 1.0. Gradients become stepped. Tested with Steps 5: 0.5 became 0.6, 0.9 became 1.0, 0.1 became 0.2 and 0.37 became 0.4 (nearest step, halves round up).

## Invert
Replaces each weight with its complement (1.0 becomes 0.0, 0.5 stays 0.5, 0.0 becomes 1.0). **Add Weights** adds unweighted vertices first (set to 1.0); **Remove Weights** drops vertices that are 0.0 after inverting. Both are on by default (`auto_assign`, `auto_remove`); tested: a vertex at 1.0 left the group, one at 0.0 became 1.0 and an unweighted vertex became 1.0 only while Add Weights was on. Locked vertex groups are not affected.

## Related
Clean, Limit Total, Normalize, Mirror: see weight-limit-clean, weight-normalize and weight-mirror.

## Gotchas
- After Smooth, Levels or Invert the per-vertex sums may no longer equal 1; run Normalize All if you need that.
- Smooth with Multi-Paint: to seed weights on vertices with none, apply one Smooth iteration with Subset Selected Pose Bones and a low Factor, as the manual suggests.

## Verify
Bend the joint before and after and compare; the Show Weight Contours overlay should show smoother spacing.

## Checked
Date: 2026-10-27. Documentation: Blender manual, Weight Paint Editing page, branch blender-v5.2-release. Confirmed: Weights menu operators, Subset list, Smooth options (Factor, Iterations, Expand/Contract) and the vertex-selection requirement, Levels Offset range and Gain with clamping, Quantize example, Invert options and locked-group note. Removed unconfirmed claims: suggested Factor and Iteration values, the Levels example numbers, 8-bit precision, "smooths only within the same group", and the modifier-stack note.
Run check, 2026-11-01, Blender 4.5.14 LTS headless: Smooth (Factor 0 to 1, Iterations 1 to 10000, Expand/Contract -1 to 1), Levels (Offset -1 to 1, Gain from 0), Quantize (Steps 1 to 1000) and Invert were run in Edit Mode on a UV sphere with the results above. Unrun: Subset values that need an armature, the Multi-Paint seeding tip, the contour overlay, locked-group exclusion in Invert, Weights menu paths.
Method: documentation checked against the manual and API pages; the code and operators were run headless in Blender 4.5.14.

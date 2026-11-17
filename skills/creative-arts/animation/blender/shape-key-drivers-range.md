---
id: creative-arts.animation.blender.shape-key-drivers-range
name: shape-key-drivers-range
category: creative-arts
field: animation
product: blender
tags: [blender, shape-keys, shape-key-drivers, driven-shape-key, shape-key-range, shape-key-vertex-group, slider-min-max, corrective-shape-keys]
level: practitioner
status: docs-checked
description: "Drive shape keys from bones and sliders in Blender, use slider min/max for overshoot and negative shapes, and split one sculpt into left/right keys with vertex group masking."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/shape_keys/shape_keys_panel.html
  - https://docs.blender.org/manual/en/5.2/animation/shape_keys/workflow.html
  - https://docs.blender.org/manual/en/5.2/animation/drivers/drivers_panel.html
  - https://docs.blender.org/manual/en/5.2/animation/drivers/usage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# shape-key-drivers-range

Goal: shape keys that respond to the rig (bone rotation, control sliders) and symmetric sculpts split into independent sides.

## Driving from a bone

1. Right-click the shape key Value > **Add Driver** (or Ctrl-D over it).
2. Variable: Transform Channel with the bone, a rotation channel and a **Space** (World Space, Transform Space or Local Space); rotation channels also offer modes such as Auto Euler, Quaternion, and Swing and X/Y/Z Twist (swing aims the axis, twist rotates around it; see `driver-variable-types`).
3. Expression: `clamp(var / radians(90), 0, 1)`. This uses only functions from the documented Simple Expressions subset (`clamp`, `radians`), which are evaluated without Python; the value reaches 1 at 90 degrees. Rotation values are radians.
4. Shape the response with the driver F-curve if needed (see `driver-fcurve-debugging`).
For a slider control, drive from a control bone's location.

## Range

- **Range** (min/max) on the key sets the minimum and maximum of its influence value; Blender can extrapolate below 0.0 and above 1.0. Widen it for inverse or overshoot shapes (for example a brow up/down from one key).

## Vertex group masking (left/right split)

1. Sculpt a symmetric `smile` key.
2. Create vertex groups `L` and `R` with a soft falloff across the centre line.
3. Set the key's **Vertex Group** field to `L` (it limits that key's deformation to the group), leave other keys at 0 and `smile` at 1, then Specials > **New Combined** and rename the result `smile_L`.
4. Switch the field to `R`, New Combined again, rename `smile_R`. Delete or mute the original.
- Related: Specials > **New from Objects Flipped** and **Update from Objects Flipped** mirror shapes across local X; they need matching topology.

## Gotchas

- A hard 0/1 vertex group gives a seam at the centre line; use a falloff.
- Pose-corrective shapes: **Update from Objects Flipped** is documented as useful for mirrored corrective shapes.

## Verify

Rotate the bone: the key value rises smoothly from 0 at rest to 1 at the target angle; the L and R keys together equal the original symmetric shape.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release source): Add Driver and Ctrl-D, variable Space options, Swing and Twist mode, Simple Expressions list (clamp, radians), Range and Vertex Group fields, New Combined and flipped specials. Removed as unconfirmed: game-export remark about drivers, centre weight value, Limit Location slider recipe, "drivers and animation are clamped" wording.
Method: documentation only; no commands were run.

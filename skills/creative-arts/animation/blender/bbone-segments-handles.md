---
id: creative-arts.animation.blender.bbone-segments-handles
name: bbone-segments-handles
category: creative-arts
field: animation
product: blender
tags: [blender, rigging, bendy-bones, bbone-segments, bbone-handles, bbone-ease, b-bones, curved-deformation]
level: practitioner
status: docs-checked
description: "Configure Blender Bendy Bones: segments, vertex mapping, start/end handle types, custom handle bones, curve/roll/scale/ease in and out, and scale easing."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/armatures/bones/properties/bendy_bones.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# bbone-segments-handles

Goal: smooth, curved deformation from few bones — spines, mouths, eyebrows, tails, cartoony limbs. The broader rig patterns are in `rigging`.

## Segments

- Bone Properties > Bendy Bones > **Segments**: the number of rigid segments the bone is subdivided into; more segments bend more smoothly but cost more pose calculation. Segments are only visible with Display As B-Bone; with other display types the segments still deform.
- **Display Size X, Z**: visible thickness of the segments in B-Bone display.
- **Vertex Mapping**: *Straight* is a fast mapping for straight or gently curved rest poses; *Curved* is slower and improves deformation for strongly curved rest poses, so use it selectively.
- The rest shape is set in Edit Mode; Edit Mode and Pose Mode each have their own set of Bendy Bone properties and the two are added or multiplied to give the final shape.

## Handles

- **Start/End Handle** type: *Automatic* (connected parent or first connected child is the handle, calculated as Absolute), *Absolute* (handle bone position relative to the current bone's head or tail; needs a nonzero distance), *Relative* (handle bone's offset from its rest pose; the manual does not recommend it because of numerical stability near zero offset), *Tangent* (handle bone orientation, independent of location).
- **Custom Handle**: the bone to use for non-Automatic types; leaving it empty effectively disables the handle. Two bones may refer to each other as handles.
- **Scale X/Y/Z/Ease** toggles multiply the final Scale or Ease values by the handle bone's local scale channels (a cheaper replacement for up to eight drivers).
- When a B-Bone is a constraint target, the target field offers a button to follow its curvature; only Armature and Copy Transforms constraints use the full transformation including roll and scale.

## Shape parameters (rest + pose)

- **Curve In/Out X, Y, Z**: offsets of the curve handle positions. **Roll In/Out**: twist interpolated per segment. **Scale In/Out X, Y, Z**: thickness (X, Z) and spacing (Y) per segment. **Ease In/Out**: length of the auto Bezier handle; Edit and Pose values are added, so they start at 1 and 0.
- **Inherit End Roll**: adds the Roll Out of the start handle bone to this bone's Roll In. **Scale Easing**: multiplies the easing values by Scale Y.
- The "BBone Shape" keying set keys all Bendy Bone properties.

## Recipes

- **Cartoon arm**: upper and lower arm B-Bones with several segments and the elbow control as custom handle for both.
- **Mouth corners**: lip B-Bones with handle bones at corners and centre.

## Gotchas

- Only Armature and Copy Transforms constraints read a B-Bone target's full transformation; other constraints use the plain bone.

## Verify

Rotate the handle controls: segments curve smoothly; deformation follows without kinks at bone joins.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release). Confirmed on the Bendy Bones page: Segments, Display Size X/Z, Vertex Mapping Straight/Curved, handle types and Custom Handle, Scale X/Y/Z/Ease toggles, Curve/Roll/Scale/Ease In/Out, Inherit End Roll, Scale Easing, constraint-target note and keying set. Removed unconfirmed version tags, defaults, segment counts, shortcut for Display Size and game-engine export claims.

Method: documentation only; no commands were run.

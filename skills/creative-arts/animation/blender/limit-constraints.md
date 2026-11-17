---
id: creative-arts.animation.blender.limit-constraints
name: limit-constraints
category: creative-arts
field: animation
product: blender
tags: [blender, constraints, limit-location, limit-rotation, limit-scale, limit-distance, affect-transform, rigging]
level: practitioner
status: docs-checked
description: "Restrict controls with Blender's Limit Location, Rotation, Scale and Distance constraints: per-axis min/max, Affect Transform, Euler order and clamp regions."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/constraints/transform/limit_location.html
  - https://docs.blender.org/manual/en/5.2/animation/constraints/transform/limit_rotation.html
  - https://docs.blender.org/manual/en/5.2/animation/constraints/transform/limit_scale.html
  - https://docs.blender.org/manual/en/5.2/animation/constraints/transform/limit_distance.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# limit-constraints

Goal: controls that can't be moved where they shouldn't (slider bones, knees bending backwards, eyelids past closed).

## Limit Location / Scale

- Minimum/Maximum X, Y, Z: number fields plus a checkbox per bound saying whether it applies. If a Minimum is higher than its Maximum, the Maximum is used for both. The Owner space is chosen on the constraint (Local Space is common for controls).
- **Affect Transform**: when the owner is moved by hand, also restrict the Location (or Scale) values in the Properties editor Transform panel, not just the visual result. Useful for slider controls.
- Slider control: bone with Limit Location Y 0..1 (Local), other axes locked (padlock), driver reads location Y.

## Limit Rotation

- Limit X, Y, Z: angle range per axis with a checkbox each. **Order**: Euler order used to apply the limits (owner's order, or XYZ for non-Euler owners). **Affect Transform** as above. Even with all limits off the constraint removes shearing.
- **Legacy Behavior** restores the pre-4.2 behaviour, which does not account for the looping nature of rotations and causes erratic snapping; the manual prefers drivers on the rotation properties for new rigs.
- Use for joint ranges on FK controls (knee X 0..150 degrees). Prefer IK limits for IK chains (see `ik-limits-stiffness`).

## Limit Distance

- Target + **Distance** (the radius of the sphere; calculated when the first target is chosen; the Reset Distance button sets it to the current distance), **Clamp Region**: *Inside* (trapped within the sphere, for example tethers), *Outside* (prevented from entering), *On Surface* (constrained to the sphere surface). Affect Transform is available.

## Gotchas

- Without Affect Transform only the visual result is limited; the Transform panel value can keep going beyond the limit.
- Order: the stack runs top to bottom, so limits placed last clamp the final result.

## Verify

Drag beyond the limit: owner stops; with Affect Transform the N panel value also stops.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release). Confirmed on the Limit Location, Limit Rotation, Limit Scale and Limit Distance pages: Min/Max checkbox semantics and the Min greater than Max rule, Affect Transform, Order, Legacy Behavior (pre-4.2 behaviour), Clamp Region modes and Reset Distance. Removed the unconfirmed gimbal remark.

Method: documentation only; no commands were run.

---
id: creative-arts.animation.blender.foot-roll-rig
name: foot-roll-rig
category: creative-arts
field: animation
product: blender
tags: [blender, rigging, foot-roll, reverse-foot, heel-pivot, toe-pivot, ik-leg]
level: practitioner
status: docs-checked
description: "Build a reverse-foot IK rig in Blender: heel, toe-tip and ball pivots, MCH roll bones, a single roll control via Transformation constraints, and side-to-side bank pivots."
sources:
  - https://docs.blender.org/manual/en/latest/animation/constraints/transform/transformation.html
  - https://docs.blender.org/manual/en/latest/animation/constraints/relationship/pivot.html
  - https://docs.blender.org/manual/en/latest/addons/rigify/rig_features.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# foot-roll-rig

Goal: the foot peels heel → ball → toe from one rotation control, the industry-standard walk-friendly leg.

## Bone hierarchy (all non-deforming except DEF)

```
foot_ik (main control, at ankle, flat on ground)
 └ MCH-heel (pivot at heel back)
    └ MCH-toe_tip (pivot at toe tip)
       └ MCH-ball (pivot at ball of foot)
          ├ MCH-leg_ik_target (at ankle) ← IK constraint target for the shin
          └ (toe control parented here or to MCH-toe_tip)
```
`roll` control: a bone on the foot whose local X rotation drives the roll.

## Wiring (Transformation constraints from `roll` X rotation)

- **MCH-heel**: rotation X maps roll 0..-90° → 0..-90° (only backward roll rotates the heel).
- **MCH-ball**: roll 0..45° → 0..45° (first part of forward roll lifts the heel by rotating at the ball).
- **MCH-toe_tip**: roll 45..90° → 0..45° (beyond 45° the foot pivots on the toe tip).
Leave **Extrapolate** off (the default) so input and output clamp to the Map From and Map To ranges. Rotation input is always taken back into the -180 to 180 degree range, which is why the roll ranges here stay inside it. The angle ranges above are practice values for a typical foot, not from the manual. Alternatively use Rigify's leg rig, whose Legs rig has an IK Heel control that commands forward or backward roll, sideways rock and yaw, plus an optional Roll On Toe slider — check `rigify-rig-types`.

## Bank (side roll)

Two pivot MCH bones at inner/outer foot edges driven by roll Y rotation ±, or Pivot constraints whose **Rotation Range** limits them to positive or negative rotation on one axis (see `pivot-constraint`).

## Gotchas

- Pivots must sit exactly on the ground plane and at the correct heel/toe extents (snap to mesh vertices).
- The IK target must be the child at the ankle, not the foot control, or the roll won't lift the leg.
- Toe control needs to counter-rotate if the toes should stay planted while the ball rolls.

## Verify

Rotate `roll` from -90 to 90: heel pivot, then ball lift, then toe-tip pivot, with the leg following; ankle never dips below ground.

## Checked

2026-10-27. Documentation release: Blender manual 5.2 (branch blender-v5.2-release). Confirmed: Transformation constraint Map From/Map To ranges, Extrapolate (off clamps to the ranges), Mix defaulting to Add for rotation, and rotation input wrapping to -180..180 (animation/constraints/transform/transformation.rst); Pivot constraint Rotation Range options (relationship/pivot.rst); Rigify leg foot features, heel control for roll, rock and yaw, and Roll On Toe slider (addons/rigify/rig_features.rst). Wrong in the old text: the claim that Rigify generates this exact rig with a roll slider was softened to the documented heel control. The 0-90 and 45-90 degree mappings are practice values and are labelled so.

Method: documentation only; no commands were run.

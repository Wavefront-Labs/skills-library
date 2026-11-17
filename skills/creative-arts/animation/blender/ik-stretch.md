---
id: creative-arts.animation.blender.ik-stretch
name: ik-stretch
category: creative-arts
field: animation
product: blender
tags: [blender, rigging, ik-stretch, stretchy-ik, stretch-to, squash-stretch, cartoon-rig]
level: practitioner
status: docs-checked
description: "Build stretchy IK limbs in Blender: bone IK Stretch values with the IK constraint's Stretch option, and Stretch To with volume preservation as a controllable alternative."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/armatures/bones/properties/inverse_kinematics.html
  - https://docs.blender.org/manual/en/5.2/animation/constraints/tracking/ik_solver.html
  - https://docs.blender.org/manual/en/5.2/animation/constraints/tracking/stretch_to.html
  - https://docs.blender.org/manual/en/5.2/animation/armatures/bones/properties/relations.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# ik-stretch

Goal: limbs that stretch beyond full extension (cartoony reach) and don't hyperextend-pop.

## Built-in IK stretch

1. IK constraint: enable **Stretch** (bones may scale up or down to reach the Target).
2. Each bone in the chain: Bone Properties > Inverse Kinematics > **IK Stretch** ("stretch influence to IK target"). Stretch only applies to bones whose IK Stretch value is greater than 0, so give the chain bones a non-zero value (start small and equal on thigh and shin).
3. Bones scale when the target is out of reach.
Simple, but it can only be switched per shot by animating the IK Stretch values.

## Stretch To approach (controllable)

- Stretch To makes a bone point at and scale towards a target using its local Y axis. Settings: **Original Length** (distance with no stretching, with a Reset Original Length button), **Maintain Volume** (XZ, X, Z, None), **Volume Variation** (exponent: above 1 exaggerates, below 1 reduces the thickness change; 0 equals None), **Volume Min/Max**, **Smooth**, and **Rotation** (XZ, ZX, Swing).
- One possible rig: an MCH chain solves IK without stretch, and a separate stretch bone from the hip to the IK control uses Stretch To; its Y scale can drive the visible chain through Copy Scale or drivers, with a custom property switching the stretch on and off.

## Volume preservation

Stretch To **Maintain Volume** XZ makes the owner thinner when stretched and thicker when contracted; set it to None to leave X and Z scales unchanged.

## Gotchas

- Children of a stretched bone inherit its scale under the default Inherit Scale Full; the Inherit Scale options (Aligned, Average, None, Fix Shear) on the child decide what propagates (see `bone-relations-inherit`).
- IK constraints run after all other constraints on the affected bones, whatever their stack position.

## Verify

Pull the IK control past reach: limb stretches smoothly from exactly full extension; toggle off returns to normal reach without a jump at rest.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release). Confirmed on the Bone Inverse Kinematics, IK constraint, Stretch To and Bone Relations pages: IK constraint Stretch only affects bones with IK Stretch above 0, Stretch To options (Original Length, Maintain Volume, Volume Variation/Min/Max, Smooth, Rotation) and Inherit Scale options. Removed unconfirmed defaults, the IK Stretch 0..1 range, the Rigify remark, game-engine export claims and the toggle formula.

Method: documentation only; no commands were run.

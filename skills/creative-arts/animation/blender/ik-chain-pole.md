---
id: creative-arts.animation.blender.ik-chain-pole
name: ik-chain-pole
category: creative-arts
field: animation
product: blender
tags: [blender, rigging, inverse-kinematics, ik-chain-length, chain-length, ik-target, ik-pole-angle, pole-angle, pole-placement]
level: practitioner
status: docs-checked
description: "Set up a Blender IK limb: chain length, an IK target bone, Pole Target placement, Use Tail, Stretch, iterations and per-chain weights, and how IK sits in the constraint stack."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/constraints/tracking/ik_solver.html
  - https://docs.blender.org/manual/en/5.2/animation/armatures/posing/bone_constraints/inverse_kinematics/introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# ik-chain-pole

Goal: a two-bone leg/arm IK that bends the right way and doesn't rotate at rest.

## Chain and target

1. Add an IK constraint to the **lower** bone (shin/forearm) with Shift-I in Pose Mode, or from the Bone Constraints tab.
2. **Target**: the object or bone the chain reaches for, for example `foot_ik` / `hand_ik`. Unlike most constraints the IK constraint works without a Target: the chain-tip bone can then be moved and rotated freely and only its ancestors are constrained.
3. **Chain Length** = 2 (shin + thigh). It counts bones starting with the owner and walking up its ancestors: 1 rotates only the owner, 0 includes every ancestor up to the root, which is why a too-long chain makes the spine bend when the foot moves.

## Pole target

- **Pole Target** (object or bone) determines the roll of the IK chain: for an arm with the Target at the hand, the Pole Target sets the elbow position. Place it on the side the joint should bend towards, away from the limb, and parent it to the root or the IK control so it moves with the rig.
- The 5.2 manual page for the IK constraint lists no pole angle field, so check the constraint panel in your version for any angle offset and set it before animating.

## Settings

- **Use Tail**: use the bone's tail as the end of the chain; unchecked it uses the head. **Stretch**: lets bones scale to reach the Target, only for bones whose IK Stretch value is above 0 (see `ik-stretch`). **Iterations**: maximum number of solving iterations. **Weight Position / Rotation**: the checkbox says whether the chain tip tries to match the Target's position or rotation; the slider weighs this chain against other IK chains affecting the same bones (a "tree").
- **Influence** is animatable for IK/FK blending (see `ik-fk-snapping`).
- IK constraints ignore their position in the constraint stack and always run after all other constraints on the affected bones. To apply constraints after IK, copy the final transformation to a new bone chain, for example with Copy Transforms.

## Verify

Enable/disable the IK constraint at rest pose: no movement. Move the control: knee tracks the pole, no flipping through the full range.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release). Confirmed on the IK constraint and Inverse Kinematics introduction pages: Shift-I, Target optional, Pole Target meaning, Chain Length semantics (0 = all ancestors), Use Tail, Stretch dependence on bone IK Stretch, Iterations, Weight Position/Rotation, IK ignoring stack order. Removed pre-bend advice, pole angle procedure and defaults (500 iterations, Use Tail on), and the gotcha list, none of which the manual states.

Method: documentation only; no commands were run.

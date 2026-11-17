---
id: creative-arts.animation.blender.armature-constraint
name: armature-constraint
category: creative-arts
field: animation
product: blender
tags: [blender, constraints, armature-constraint, multi-parent, weighted-parenting, prop-attachment, rigging]
level: practitioner
status: docs-checked
description: "Use Blender's Armature constraint as a weighted multi-parent: bone targets and weights, Preserve Volume, envelopes, current location — e.g. a prop held in two hands."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/constraints/relationship/armature.html
  - https://docs.blender.org/manual/en/5.2/animation/constraints/relationship/child_of.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# armature-constraint

Goal: an object or bone that follows several bones blended by weights, exactly like a vertex skinned to them — the robust alternative to stacking Child Of constraints.

## Setup

1. Add an Armature constraint to the owner (object or bone). Unlike the Armature modifier it also uses bones whose Deform option is off, and the targets may come from different armatures.
2. **Add Target Bone** for each parent: Target (armature object), Sub-Target (bone name) and **Weight**. Remove an entry with the X button. **Normalize Weights** rescales the list so the weights add up to 1.0.
3. Options:
   - **Preserve Volume**: prevents the owner shrinking when the target bones rotate relative to each other.
   - **Use Envelopes**: uses bone envelopes to weaken the influence of bones that are further away; the manual advises setting every Weight to 1.0 for best results. Every bone must be added by hand (no automatic detection of nearby bones).
   - **Use Current Location** (bone constraint only): finds nearby envelopes and B-Bone segments from the owner bone's current location (pose and earlier constraints included) instead of its rest location. Objects have no rest location, so they always use the current one.
   - **Influence**: overall strength of the constraint.

## Recipes

- **Sword held in both hands**: sword Armature constraint, targets hand.R (0.5) and hand.L (0.5); animate weights for hand-offs (or use influence switches).
- **Cheek control riding jaw and skull**: control bone targets jaw (0.3), head (0.7).
- **Glasses on a face**: targets head bone 1.0 — a single target bone at weight 1.0.

## Versus Child Of

- Child Of has one target, which can also be an object, and a Set Inverse button; the manual suggests the Armature constraint when the parents are bones and several must be blended.
- The Armature constraint blends several bone targets by weight, like the Armature modifier does for vertices.

## Gotchas

- Weights that do not add up to 1.0 can be fixed with Normalize Weights.
- Envelope-based weakening needs every target bone added manually.

## Verify

Pose each target bone separately: owner moves by its weight share; at rest pose it sits at its modelled position.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release). Confirmed on the Armature constraint page: option names (Preserve Volume, Use Envelopes, Use Current Location, Add Target Bone, Normalize Weights), the Target/Sub-Target/Weight list, and the comparison with Child Of. Removed unconfirmed claims (dual quaternion blending, parenting advice, weight-sum scaling, rest-pose and inverse-matrix remarks).

Method: documentation only; no commands were run.

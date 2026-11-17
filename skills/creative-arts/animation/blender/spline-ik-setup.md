---
id: creative-arts.animation.blender.spline-ik-setup
name: spline-ik-setup
category: creative-arts
field: animation
product: blender
tags: [blender, rigging, spline-ik, spline-ik-setup, spline-ik-scaling, spline-ik-chain, hook-modifier, tails, tentacles]
level: practitioner
status: docs-checked
description: "Rig tails, spines and tentacles with Blender's Spline IK: curve with hooked control points, chain count, Even Divisions/Fit Curve, Y and XZ scale modes, and Use Curve Radius."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/constraints/tracking/spline_ik.html
  - https://docs.blender.org/manual/en/5.2/animation/armatures/posing/bone_constraints/inverse_kinematics/spline_ik.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# spline-ik-setup

## Build

1. A chain of connected bones (for example 12 bones; Subdivide splits one bone into several). Name clearly (`tail.001`...). The manual advises bones of roughly equal length that follow the curve's shape in rest pose, and not too long.
2. A curve along the chain. The curve type is not important as long as a path can be extracted from it, as for Follow Path. Control it with hooks (the manual recommends Bone Hooks), one hook per control point, with about one control point for every 3-5 bones (see `hook-modifier`).
3. With the last bone selected, add Spline IK from the Bone Constraints tab: **Chain Length** = number of bones to include, counting from and including the selected bone; **Target** = the curve.

## Settings

- **Even Divisions**: off, each bone covers a distance along the curve relative to its rest length; on, each covers the same distance. **Chain Offset**: off, the chain moves to match the curve's position; on, it stays at its original starting location and mimics the curve's shape.
- **Use Curve Radius**: use the radii of the curve points as extra X and Z scaling factors.
- **Y Scale Mode**: *None* (reset bones to rest length), *Fit Curve* (stretch to cover the whole curve), *Bone Original* (keep original length including Pose Mode scale). The curve object's scale also affects the result.
- **XZ Scale Mode** (thickness): *None* (X and Z scales 1), *Bone Original*, *Inverse Scale* (inverse of the Y scale), *Volume Preservation* (like Stretch To). **Use Original Scale** applies Inverse Scale or Volume Preservation on top of the Pose Mode bone scales.
- Spline IK, like IK, ignores its stack position (runs after other constraints); if a Standard IK chain and a Spline IK chain affect the same bone, Standard IK wins.

## Twist

Roll is controlled by rotating bones around their local Y axes (start at the farthest bone and work back), or with Copy Rotation constraints on the bones. The manual notes that bones do not inherit the curve's tilt and that there is no automatic twist falloff up the chain; consider Bendy Bones for that.

## Gotchas

- Spline IK cannot be used on objects, only bones.
- Sharp bends in the curve are where long or poorly matched bones fit worst, especially with stretching disabled.

## Verify

Move each control: the chain follows the curve smoothly; with Fit Curve the chain always spans the whole curve; no flipping at rest.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release). Confirmed on the Spline IK constraint and Armature Posing Spline IK pages: Chain Length semantics, Even Divisions, Chain Offset, Use Curve Radius, Y and XZ Scale Modes, Use Original Scale, roll and tilt limitations, hook recommendations, priority versus Standard IK. Removed the unconfirmed Ctrl-H menu path, parenting advice and curve direction/resolution gotchas.

Method: documentation only; no commands were run.

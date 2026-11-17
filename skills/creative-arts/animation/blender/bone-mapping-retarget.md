---
id: creative-arts.animation.blender.bone-mapping-retarget
name: bone-mapping-retarget
category: creative-arts
field: animation
product: blender
tags: [blender, motion-capture, bone-mapping-retarget, bone-mapping, retargeting, copy-rotation, rest-pose-matching]
level: practitioner
status: docs-checked
description: "Retarget mocap to a custom rig in Blender: match rest poses, build a bone map, constraint-based retarget (Copy Rotation world/local, Copy Location on hips), bake to the target, and retarget add-ons."
sources:
  - https://docs.blender.org/manual/en/latest/animation/constraints/transform/copy_rotation.html
  - https://docs.blender.org/manual/en/latest/animation/constraints/transform/copy_location.html
  - https://docs.blender.org/manual/en/latest/animation/armatures/posing/editing/apply.html
  - https://docs.blender.org/api/current/bpy.ops.nla.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# bone-mapping-retarget

Goal: motion from a source skeleton (BVH/FBX mocap, Mixamo) onto your character's rig controls. Overview of mocap pipelines is in `mocap-retarget`.

## 1. Match rest poses

Pose the *source* to match the target's rest (T vs A pose): rotate source arms down in pose mode at a frame before the motion, or pose a duplicated source to the target's A-pose and use Pose > Apply > Pose as Rest Pose. That operator permanently changes the armature rest pose (it applies the bone transforms in Edit Mode) and can require re-binding or adjusting skinning, constraints, drivers and animation, so only run it on a duplicate. Rest-pose mismatch is the most common cause of bad retargets (practice).

## 2. Bone map

Table source → target: `Hips → torso/hips control`, `Spine/Spine1/Spine2 → spine_fk.001..`, `LeftArm → upper_arm_fk.L`, ... Keep it as a text/JSON for reuse across clips.

## 3. Constraint retarget

- Hips: Copy Location (World → World; Copy Location has no scale-compensation option, so if skeleton heights differ scale the source armature object or drive a helper by the ratio of leg lengths) + Copy Rotation.
- Other bones: **Copy Rotation**, World Space → World Space when rest orientations differ (bone rolls), Mix Replace. For FK controls of a Rigify rig, target the FK controls with limbs in FK mode.
- Feet/hands for IK: Copy Transforms the IK controls to the source feet (with an offset bone to account for ankle height differences).

## 4. Bake

Select target controls, **Pose > Animation > Bake Action...**: Visual Keying ON (it is off by default), Clear Constraints ON (the operator names it Clear Local Constraints and says Visual Keying should be enabled for a correct bake), frame range = clip, Only Selected Bones. Then remove the source.

## Tools

Third-party add-ons and extensions can automate bone maps and rest-pose matching; use one for volume work (follow its own documentation) and know the manual method for debugging.

## Gotchas

- Scale mismatch: source in cm (100x) — scale the source armature object, not bones (practice).
- Roll differences produce twisted forearms when using Local space; prefer World space.
- Foot sliding after retarget: lock contacts with IK and adjust hip height.

## Verify

Overlay source and target: limbs align through the clip; feet plant at contacts; no twisted joints.

## Checked

2026-10-27. Documentation release: Blender manual 5.2 (branch blender-v5.2-release), Pose menu in space_view3d.py and the bpy.ops.nla.bake reference. Confirmed: Copy Rotation Mix Replace and World/Local space options (copy_rotation.rst); Copy Location has only Axis, Invert, Offset and spaces (copy_location.rst); Pose > Apply > Pose as Rest Pose and its permanence warning (apply.rst); Bake Action is under Pose > Animation, with Only Selected Bones, Visual Keying (default off) and Clear Local Constraints options (API reference for bpy.ops.nla.bake). Wrong in the old text: Copy Location has no scale compensation. Removed named third-party retarget add-ons that no accessible source confirms.

Method: documentation only; no commands were run.

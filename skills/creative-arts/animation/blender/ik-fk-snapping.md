---
id: creative-arts.animation.blender.ik-fk-snapping
name: ik-fk-snapping
category: creative-arts
field: animation
product: blender
tags: [blender, rigging, ik-fk-snapping, ik-fk-switch, ik-fk-snap, ik-fk, visual-transform, rigify-snap]
level: practitioner
status: docs-checked
description: "Switch limbs between IK and FK in Blender without pops: three-chain setup (IK, FK, deform blended), a keyed IK/FK property, snapping by visual transform, and keying both sides at the switch frame."
sources:
  - https://docs.blender.org/manual/en/latest/animation/armatures/posing/editing/apply.html
  - https://docs.blender.org/manual/en/latest/addons/rigify/rig_features.html
  - https://docs.blender.org/api/current/bpy.types.PoseBone.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# ik-fk-snapping

Goal: animate a planted hand in IK and a swinging arm in FK in the same shot.

## Rig structure

- **FK chain** (controls), **IK chain** (MCH bones with IK constraint + pole), **deform chain** (DEF) with Copy Transforms from FK and Copy Transforms from IK stacked; the IK one's influence driven by a custom property `ik_fk` (0 = FK, 1 = IK) on a properties bone.
- Expose the property in a rig UI panel (see `rig-ui-controls`).

## Switching procedure (manual)

1. At the switch frame, key the current state of both chains and the property.
2. Snap the destination chain to match the current visual pose:
   - FK → IK: put the IK control at the hand's visual transform (for example Snap Cursor to Selected on the wrist then Selection to Cursor, or a temporary Copy Transforms constraint followed by Pose > Apply > **Visual Transform to Pose**), and the pole on the elbow plane.
   - IK → FK: copy the visual rotations of the IK MCH bones to the FK controls with the classic trick: add Copy Transforms from the IK bone to the FK control, use Pose > Apply > **Visual Transform to Pose**, then remove the constraint. That operator converts the final constrained transform into regular pose transforms.
3. Key the property switch (Constant interpolation) and key the destination chain.

## Snapping tools

- **Rigify** generated rigs expose an IK-FK slider and IK<->FK snapping buttons in the sidebar Item tab, *Rig Main Properties* panel. The main button snaps on the current frame and auto-keys the result if auto keying is on; the *Action* button bakes the change over multiple keyframes according to *Rig Bake Settings*; *Clear* deletes keyframes on those controls in the bake interval. Rigify's slider runs full IK at 0 to full FK at 1, the opposite of the `ik_fk` convention above, so keep one convention per rig.
- Script approach: `bone.matrix = other_bone.matrix` (`PoseBone.matrix` is the final matrix in armature object space), then `bpy.context.view_layer.update()` per bone along the chain from parent to child.

## Gotchas

- Snap order matters: set parents first, update, then children.
- Linear interpolation on the property blends chains over several frames — usually wrong; use Constant.
- Pole position mismatch causes the elbow to rotate at the switch.

## Verify

Scrub across the switch frame with the deform chain visible: no pop; both chains overlap exactly at the switch.

## Checked

2026-10-27. Documentation release: Blender manual 5.2 (branch blender-v5.2-release) and Python API 'current'. Confirmed: Pose > Apply > Visual Transform to Pose converts constrained results to pose transforms (animation/armatures/posing/editing/apply.rst); Rigify IK-FK slider (full IK at 0, FK at 1), snapping button group (main button snaps and auto-keys if enabled, Action bakes, Clear deletes) and the Item tab Rig Main Properties and Rig Bake Settings panels (addons/rigify/rig_features.rst); PoseBone.matrix is in armature object space (API reference). Wrong in the old text: the operator is Visual Transform to Pose, not Apply Visual Transform; there is no Snap and keyframe button; Copy Attributes is an add-on and was removed; matrix is armature space, not pose space.

Method: documentation only; no commands were run.

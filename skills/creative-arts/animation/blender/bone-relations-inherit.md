---
id: creative-arts.animation.blender.bone-relations-inherit
name: bone-relations-inherit
category: creative-arts
field: animation
product: blender
tags: [blender, rigging, bone-inherit-scale, inherit-rotation, local-location, bone-relations, parenting, hinge]
level: practitioner
status: verified
description: "Set Blender bone Relations: parent and connected, Inherit Rotation, the Inherit Scale modes (Full, Fix Shear, Aligned, Average, None, Legacy), and Local Location."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/armatures/bones/properties/relations.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# bone-relations-inherit

Goal: controls that inherit just the right parts of their parent's transform.

## Relations panel (Bone Properties > Relations)

- **Parent** + **Connected** (head connected to the parent's tail). Connected bones cannot be moved on their own: pressing G switches to rotation.
- **Inherit Rotation** (`use_inherit_rotation`) off: the child keeps its rotation in armature object space when its parent rotates. The manual notes that disabling Inherit Rotation or Inherit Scale breaks the propagation for that bone and all its descendants.
- **Inherit Scale** (`Bone.inherit_scale`: `FULL`, `FIX_SHEAR`, `ALIGNED`, `AVERAGE`, `NONE`, `NONE_LEGACY`):
  - *Full*: inherits all parent scaling and shear.
  - *Fix Shear*: applies full parent effects to the rest state, then removes shear while preserving direction, length and volume; shear can still reappear from local rotation if the inherited scale is non-uniform. Closest to Full while suppressing shear; useful at the base of an appendage.
  - *Aligned*: parent scaling is applied as if the child were oriented like the parent (X over X, and so on); useful in chains such as tentacles to keep lengthwise scaling lengthwise.
  - *Average*: inherits a uniform factor equal to the total volume change of the parent (run: a parent scaled 2 x 1 x 1 gives the child 1.26 on every axis, the cube root of 2); useful to block squash and stretch propagation between sub-rigs while letting uniform size changes through.
  - *None*: ignores all parent scale and shear; useful when overriding scale with constraints.
  - *None (Legacy)*: replicates the old Inherit Scale checkbox and may be removed in a future release.
- **Local Location**: when disabled, the location property is evaluated in the parent bone's local space rather than the bone's own rest-pose orientation.
- **Relative Parenting** (Pose Mode only): changes how the bone's transformation is applied to its child objects.
- The panel also lists the bone collections the bone belongs to (visibility, solo and remove buttons; M or Shift-M assigns).

## Recipes

- **Head isolation**: Inherit Rotation off on the head bone keeps it level in armature space when the torso rotates; a Copy Rotation constraint from a helper bone with animatable influence is an alternative.
- **Squash-stretch body**: torso control scale with Fix Shear or Aligned on children to limit skewed limbs.

## Gotchas

- Non-uniform parent scale with Full can shear children; Fix Shear, Aligned, Average or None avoid it in different ways.

## Verify

Rotate/scale the parent: child behaves as intended (level head, no skew); no visual pop when switching via constraint influence.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release). Confirmed on the Bone Relations page: Parent, Connected, Local Location, Inherit Rotation, every Inherit Scale mode and its stated use, Relative Parenting, bone collections list. Removed the unconfirmed claims about animating Inherit Rotation, pose pops, game-engine shear, and eye-scale uses.

Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): Bone.inherit_scale enum names; parent pose bone scaled (2,1,1), child connected and rotated: AVERAGE gives 1.2599 on all axes, NONE and NONE_LEGACY give 1 on all axes, ALIGNED keeps the 2 on the child X axis while FULL puts it on the child Y axis; use_inherit_rotation True makes the child follow a 90 degree parent rotation, False keeps its rest orientation; a new connected child bone has use_connect, use_inherit_rotation and use_local_location True, use_relative_parent False and inherit_scale FULL. Not run (confirmed from the manual only): the shear-suppression details of Fix Shear, Local Location semantics, Relative Parenting effect on child objects and the G-key behaviour of connected bones.

Method: manual text and shipped UI scripts confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.

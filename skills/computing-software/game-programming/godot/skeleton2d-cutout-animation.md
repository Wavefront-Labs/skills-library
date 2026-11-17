---
id: computing-software.game-programming.godot.skeleton2d-cutout-animation
name: skeleton2d-cutout-animation
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, skeleton2d, bone2d, cutout-animation, polygon2d, 2d-ik, game-programming]
level: practitioner
status: docs-checked
description: "Build Godot 2D cutout characters with Skeleton2D and Bone2D, skinned Polygon2D weights, rest poses, and AnimationPlayer keys plus 2D IK modifications."
sources: ["https://docs.godotengine.org/en/stable/tutorials/animation/2d_skeletons.html", "https://docs.godotengine.org/en/stable/tutorials/animation/cutout_animation.html", "https://docs.godotengine.org/en/stable/classes/class_skeleton2d.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Skeleton2D and cutout animation

**Goal:** a 2D character made of parts, deformed by bones, animated with keys and IK.

## Rig
1. `Skeleton2D` root with a chain of `Bone2D` children (hip > torso > upper_arm > forearm > hand).
   Every bone warns about a missing rest pose until you select the Skeleton2D node, open the
   **Skeleton2D** toolbar button and choose **Overwrite Rest Pose**. Repeat it whenever you add or
   remove bones.
2. Simple cutout: Sprite2D parts parented under bones (rigid parts, no deformation), as in the cutout animation tutorial.
3. Deforming meshes: a **Polygon2D** with the texture; set its Skeleton, push **Sync Bones to Polygon**
   (once, again only if bones are added, removed or renamed), then paint bone weights per vertex.

## Animate
Use an AnimationPlayer to key the bones (see the cutout animation tutorial). Always animate from the
rest pose so parts do not shift.

## IK (SkeletonModificationStack2D)
`Skeleton2D` holds a `SkeletonModificationStack2D` (`get_modification_stack()`,
`set_modification_stack()`, `execute_modifications(delta, execution_mode)`). Create the stack, raise its
`modification_count` and add the modifications you need to apply inverse kinematics. The class pages
still list this API in the 4.7 docs; the 3D equivalent is `SkeletonModifier3D` (see that skill).

## Verify
- [ ] Rest pose set after the last bone change; deformation shows no tearing at joints.

## Checked
2026-10-28, Godot docs `stable` (latest release tag 4.7.2-stable). Confirmed from the 2D skeletons tutorial and the Skeleton2D class page: rest pose warning and Overwrite Rest Pose, re-set after adding or removing bones, Sync Bones to Polygon, SkeletonModificationStack2D methods and modification_count. Fixed: "Make Rest Pose" is Overwrite Rest Pose in the docs. Removed (not confirmed in the pages read): Reset to rest pose, Polygon2D-must-not-be-child rule, key-insert toolbar advice, named IK modification classes (TwoBoneIK, FABRIK, CCDIK), draw-order via z_index/show_behind_parent, scale and mirroring gotchas, RESET track.
Method: documentation only; no commands were run.

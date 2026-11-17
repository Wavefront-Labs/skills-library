---
id: computing-software.game-programming.godot.skeletonmodifier3d-and-ik
name: skeletonmodifier3d-and-ik
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, skeletonmodifier3d, skeleton-ik, lookatmodifier3d, procedural-animation, game-programming]
level: practitioner
status: docs-checked
description: "Apply procedural bone changes in Godot 4.3+ with SkeletonModifier3D: built-in LookAt and IK modifiers, custom _process_modification, and influence blending."
sources: ["https://docs.godotengine.org/en/stable/classes/class_skeletonmodifier3d.html", "https://docs.godotengine.org/en/stable/classes/class_lookatmodifier3d.html", "https://docs.godotengine.org/en/stable/classes/class_skeleton3d.html", "https://godotengine.org/article/design-of-the-skeleton-modifier-3d/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SkeletonModifier3D and IK

**Goal:** heads that track targets, feet that plant and custom bone tweaks after animation.

## How it works (Godot 4.3+)
Child nodes of `Skeleton3D` that extend `SkeletonModifier3D` run after the AnimationMixer applies
poses, in child order; the Skeleton3D runs them once per frame. Each has `active` (default true) and
`influence` (default 1.0). The Skeleton3D applies influence itself, so a modifier must not apply it to
the poses it sets. Modifier changes are discarded after being applied to the skin, so they are not in
the Skeleton3D bone pose seen in `_process()`.

## Built-in modifiers
The stable class reference lists these direct subclasses of `SkeletonModifier3D`: `LookAtModifier3D`
(look-at with limits and a forward axis), `XRBodyModifier3D`, `XRHandModifier3D`,
`PhysicalBoneSimulator3D`, `SpringBoneSimulator3D`, `RetargetModifier3D`, `BoneConstraint3D`,
`BoneTwistDisperser3D`, `LimitAngularVelocityModifier3D`, `ModifierBoneTarget3D`, `IKModifier3D` and
`SkeletonIK3D`. Which release added each one is not checked here: look it up for the version you
target. Godot 4.3 introduced the `SkeletonModifier3D` base class itself.

## Custom modifier
```gdscript
@tool
extends SkeletonModifier3D
@export var bone_name := "Spine"
@export var lean := 0.2

func _process_modification_with_delta(delta: float) -> void:
    var skel := get_skeleton()
    var idx := skel.find_bone(bone_name)
    if idx < 0: return
    var pose := skel.get_bone_pose_rotation(idx)
    skel.set_bone_pose_rotation(idx, pose * Quaternion(Vector3.FORWARD, lean))
```
`_process_modification()` is marked deprecated in the current docs in favour of `_process_modification_with_delta(delta)`; older releases may only have the old name, so check your version. Use `influence` for fades instead of manually lerping. The modifier's `modification_processed` signal helps sync dependent nodes (e.g. attachments reading final bone poses). Declare `@tool` to preview modifications in the editor.

## Gotchas
- To read the final modified pose (for example for a Label3D), connect to the `Skeleton3D`
  `skeleton_updated` signal; `_process()` does not see modifier results.
- Modifiers in tool mode run in the editor; guard heavy logic.
- Modifiers always run after the AnimationMixer, whatever the scene-tree order.

## Verify
- [ ] Setting influence 0 restores the pure animation; look-at respects angle limits.

## Checked
2026-11-01. Confirmed against the SkeletonModifier3D, LookAtModifier3D and Skeleton3D class references
and the Godot design article: 4.3 introduction, child order and once-per-frame processing, active and
influence defaults, deprecated virtual, direct subclass list, Skeleton3D method names, skeleton_updated.
Removed unconfirmed claims: per-class release versions, the IK subclass tree and its 4.6 date, the
SkeletonIK3D pre-4.6 note.
Method: documentation only; no commands were run.

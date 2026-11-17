---
id: computing-software.game-programming.godot.root-motion-in-godot
name: root-motion-in-godot
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-animation, godot-root-motion, root-motion-track, get-root-motion-position, animationtree, characterbody3d, animation-driven-movement, game-programming]
level: advanced
status: docs-checked
description: "Use root motion in Godot 4: the root motion track, extracting deltas from AnimationTree, applying them to CharacterBody3D velocity, and mixing with gameplay control."
sources: ["https://docs.godotengine.org/en/stable/tutorials/animation/animation_tree.html#root-motion", "https://docs.godotengine.org/en/stable/classes/class_animationmixer.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Root motion in Godot

**Goal:** movement driven by the animation's root bone (dodges, climbing, attacks with lunges) so feet
do not slide and moves cover the authored distance.

## Setup
1. Animations must animate a root bone that carries the motion (authored in the DCC tool).
2. On the AnimationTree (or AnimationPlayer; both inherit AnimationMixer) set `root_motion_track` to the
   root bone path, e.g. `Skeleton3D:Root`.
3. Godot cancels that bone's transform visually (the animation stays in place); the motion is retrieved
   through the AnimationTree API instead.

## Applying it
```gdscript
@onready var tree: AnimationTree = $AnimationTree

func _physics_process(delta: float) -> void:
    var rm_pos: Vector3 = tree.get_root_motion_position()          # local delta this frame
    var rm_rot: Quaternion = tree.get_root_motion_rotation()
    quaternion = quaternion * rm_rot                                 # apply rotation first
    var world_delta := (global_basis * rm_pos)                       # local -> world
    # model facing may be flipped vs Godot's -Z forward; correct here if needed
    if delta > 0.0:
        velocity.x = world_delta.x / delta
        velocity.z = world_delta.z / delta
    if not is_on_floor():
        velocity.y -= gravity * delta                                # keep gravity under game control
    move_and_slide()
```
Converting the delta to velocity and calling `move_and_slide()` keeps collisions working (do not add
the delta to `position` directly). Set the AnimationTree's callback process mode to Physics so deltas
match physics frames.

## Mixing with gameplay
- Common split: locomotion is code-driven (responsive input), specific actions (attacks, vaults,
  hit reactions) use root motion. Toggle via a flag per state; while root motion is active, ignore
  input movement.
- `get_root_motion_position_accumulator()` (and the rotation and scale versions) return the actual
  blended value of the animation, while `get_root_motion_position()` returns the per-frame delta.
- A `TimeScale` node (parameter `scale`) changes animation speed, and with it the distance covered.

## Gotchas
- Godot's humanoid skeleton profile defines the rest pose as facing +Z, while a CharacterBody3D moves
  along -Z: if the deltas point backwards, rotate the model node 180 degrees or flip the vector.
- Blending states blends their root motion as well; keep transitions short between root-motion and
  code-driven states.

## Verify
- [ ] Dodge animation moves the character exactly the authored distance (measure before/after).
- [ ] No foot sliding visible during root-motion states.
- [ ] Root-motion moves stop at walls (collision preserved).

## Checked

Checked 2026-10-25 against the Godot 4.7 documentation (godot-docs stable branch, last commit 2026-10-24; latest engine release 4.7.2). Confirmed: the root bone is selected as the root motion track and its transform is cancelled visually; `get_root_motion_position/rotation/scale()` return the motion delta and the `*_accumulator()` versions the actual blended value; the result can feed `CharacterBody3D.move_and_slide`; `root_motion_track` and `callback_mode_process` are AnimationMixer properties; `TimeScale` has a `scale` parameter; the humanoid profile rest pose faces +Z (retargeting page). Removed the unconfirmed 4.2 version gate, import-setting advice, half-speed and wrong-path claims.

Method: documentation only; no commands were run.

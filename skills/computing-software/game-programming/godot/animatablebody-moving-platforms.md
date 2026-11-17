---
id: computing-software.game-programming.godot.animatablebody-moving-platforms
name: animatablebody-moving-platforms
category: computing-software
field: game-programming
product: godot
tags: [godot, godot-physics, animatablebody, moving-platform-godot, sync-to-physics, game-programming]
level: practitioner
status: docs-checked
description: "Build moving platforms and doors in Godot 4 with AnimatableBody2D/3D: sync_to_physics, animating via AnimationPlayer or code, and carrying CharacterBody riders correctly."
sources: ["https://docs.godotengine.org/en/stable/classes/class_animatablebody3d.html", "https://docs.godotengine.org/en/stable/classes/class_staticbody3d.html", "https://docs.godotengine.org/en/stable/classes/class_characterbody3d.html#class-characterbody3d-property-platform-floor-layers", "https://docs.godotengine.org/en/stable/classes/class_animationmixer.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AnimatableBody moving platforms

**Goal:** platforms, elevators and doors that move on a path and push/carry characters and rigid
bodies without jitter.

## Why AnimatableBody
- A `StaticBody` that is moved manually is teleported to its new position without affecting other
  bodies in its path.
- `AnimatableBody2D/3D` is a static body meant to be moved by code, an AnimationMixer or a
  RemoteTransform: its linear and angular velocity are estimated when it moves and used to affect other
  physics bodies in its path (platforms, doors).
- A `RigidBody` frozen in kinematic mode also works; the RigidBody docs point to AnimatableBody for a
  body that is always frozen.

## Moving it
- `sync_to_physics` (default true) synchronizes the body's movement to the physics frame; the class
  reference calls this useful when animating with AnimationPlayer. Set the AnimationPlayer's
  `callback_mode_process` to `ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS` (the default is idle). Do not
  combine `sync_to_physics` with `move_and_collide()`.
- Or move it from code in `_physics_process`.
```gdscript
extends AnimatableBody3D
@export var travel := Vector3(0, 4, 0)
@export var period := 4.0
var _t := 0.0
@onready var _start := global_position
func _physics_process(delta):
    _t += delta
    global_position = _start + travel * (0.5 - 0.5 * cos(TAU * _t / period))
```

## Riders (CharacterBody)
`CharacterBody` follows moving platforms: `platform_floor_layers` (default: all layers) selects the
floor bodies that act as moving platforms, and `platform_wall_layers` (default 0: none) the wall bodies.
`platform_on_leave` controls what happens when leaving a platform: `PLATFORM_ON_LEAVE_ADD_VELOCITY`
(default, the last platform velocity is applied), `PLATFORM_ON_LEAVE_ADD_UPWARD_VELOCITY` or
`PLATFORM_ON_LEAVE_DO_NOTHING`. `get_platform_velocity()` returns the platform velocity.

## Gotchas
- With physics interpolation on, animation and tweens that move objects should also run on the physics
  tick (see the physics interpolation skill).

## Verify
- [ ] Character stands on an elevator going up and down without bouncing or sinking.
- [ ] Jumping off a moving platform inherits its velocity as configured.

## Checked

2026-10-25, against godot-docs master ("latest" docs, last commit 2026-10-24). Confirmed in the AnimatableBody3D, StaticBody3D, CharacterBody3D, RigidBody3D and AnimationMixer class pages: AnimatableBody estimates velocity and affects bodies in its path, StaticBody is teleported when moved, sync_to_physics default true with the move_and_collide warning, callback_mode_process default idle and the physics mode, platform_floor_layers, platform_wall_layers, platform_on_leave values and get_platform_velocity; and the physics interpolation tutorial (indirect movement on the physics tick). Removed unsupported jitter, scaling and rigid-body rider claims.

Method: documentation only; no commands were run.

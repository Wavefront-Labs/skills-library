---
id: computing-software.game-programming.godot.rigidbody-and-integrate-forces
name: rigidbody-and-integrate-forces
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-physics, godot-rigidbody, rigidbody3d, rigidbody2d, _integrate_forces, physicsdirectbodystate, apply-impulse, freeze-mode, contact-monitor, game-programming]
level: practitioner
status: docs-checked
description: "Control Godot RigidBody2D/3D correctly: forces vs impulses, _integrate_forces with PhysicsDirectBodyState, teleporting, freeze modes, contact reporting and sleeping."
sources: ["https://docs.godotengine.org/en/stable/tutorials/physics/rigid_body.html", "https://docs.godotengine.org/en/stable/classes/class_rigidbody3d.html", "https://docs.godotengine.org/en/stable/classes/class_physicsdirectbodystate3d.html", "https://docs.godotengine.org/en/stable/tutorials/physics/physics_introduction.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RigidBody and _integrate_forces

**Goal:** physics-driven objects (crates, balls, vehicles, ragdoll parts) that you can push, steer and
teleport without fighting the physics engine.

## Rule: do not set position/transform each frame
Setting the transform of a RigidBody (`set_global_transform()`, `look_at()`) is fine once, for an
initial placement, but not every frame: the physics engine can then no longer simulate the body
correctly. Use forces/impulses, or modify the state inside `_integrate_forces`.

## Forces and impulses (from _physics_process)
```gdscript
extends RigidBody3D
@export var thrust := 20.0

func _physics_process(_delta: float) -> void:
    if Input.is_action_pressed("thrust"):
        apply_central_force(-global_basis.z * thrust)        # continuous, scaled by step
    if Input.is_action_just_pressed("jump"):
        apply_central_impulse(Vector3.UP * 5.0)                # instant velocity change * mass
```
`apply_force(force, position)` / `apply_impulse(impulse, position)` take `position` as the offset from
the body origin in global coordinates and also produce torque. `apply_torque`, `apply_torque_impulse` for
rotation. `constant_force`/`add_constant_force` for persistent forces.

## _integrate_forces: direct state access
Called during the physics step with the body's `PhysicsDirectBodyState3D`. Safe place to read
contacts and set velocity or transform:
```gdscript
var teleport_to = null

func _integrate_forces(state: PhysicsDirectBodyState3D) -> void:
    if teleport_to != null:
        state.transform.origin = teleport_to
        state.linear_velocity = Vector3.ZERO
        teleport_to = null
    # clamp speed
    if state.linear_velocity.length() > 30.0:
        state.linear_velocity = state.linear_velocity.limit_length(30.0)
    for i in state.get_contact_count():
        var n := state.get_contact_local_normal(i)
        if n.dot(Vector3.UP) > 0.7: on_ground = true
```
Set `custom_integrator = true` to skip Godot's own gravity/damping integration and do all of it
yourself in this function.

## Contacts and signals
For `body_entered`/`body_shape_entered` signals and `get_colliding_bodies()`, enable
`contact_monitor = true` and set `max_contacts_reported` > 0. Without these, contact signals never
fire (common confusion).

## Freeze and sleeping
- `freeze = true` with `freeze_mode` `FREEZE_MODE_STATIC` (default; not affected by gravity and
  forces, moved only by code, does not collide with bodies along its path) or `FREEZE_MODE_KINEMATIC`
  (like static, but collides with bodies along its path when moved): pick up/carry objects, animated
  platforms. For a body that is always frozen use StaticBody3D or AnimatableBody3D instead.
- `can_sleep` (default true); `sleeping` to force sleep. A sleeping body acts like a static body and
  wakes when forces are applied, by a collision or via code. While asleep `_integrate_forces()` is not
  called; keep the body awake or disable `can_sleep` if you need it every step.

## Stability settings
`continuous_cd` (default false) for fast bodies that tunnel through thin shapes;
`physics_material_override` for friction/bounce; Jolt is available as the 3D physics engine since
Godot 4.4 and is the default for new projects (see the Jolt skill).

## Verify
- [ ] Teleport via `_integrate_forces` places the body without explosion or residual velocity.
- [ ] Contact signals fire only after enabling contact_monitor and max_contacts_reported.
- [ ] No script assigns RigidBody positions in `_process`.

## Checked

2026-10-25, against godot-docs master ("latest" docs, last commit 2026-10-24). Confirmed in the RigidBody tutorial (do not call set_global_transform or look_at every frame; use _integrate_forces), the RigidBody3D class page (apply_* methods and position offset, constant_force and add_constant_force, custom_integrator disables standard integration, contact_monitor with max_contacts_reported greater than 0, freeze and the two freeze modes, can_sleep, continuous_cd), the Physics introduction (sleeping behaviour and _integrate_forces not called while asleep) and the Jolt page (added in 4.4, default for new projects). Removed the unsupported 1:100 mass-ratio guidance.

Method: documentation only; no commands were run.

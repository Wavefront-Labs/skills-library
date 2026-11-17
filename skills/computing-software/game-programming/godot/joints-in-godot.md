---
id: computing-software.game-programming.godot.joints-in-godot
name: joints-in-godot
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-joints, pinjoint, hingejoint, generic6dof, ragdoll, game-programming]
level: practitioner
status: docs-checked
description: "Connect Godot bodies with joints: PinJoint, HingeJoint3D limits and motors, SliderJoint, ConeTwist and Generic6DOF, plus 2D joints, breaking and stability tips."
sources: ["https://docs.godotengine.org/en/stable/classes/class_joint3d.html", "https://docs.godotengine.org/en/stable/classes/class_hingejoint3d.html", "https://docs.godotengine.org/en/stable/classes/class_generic6dofjoint3d.html", "https://docs.godotengine.org/en/stable/classes/class_joint2d.html", "https://docs.godotengine.org/en/stable/tutorials/physics/using_jolt_physics.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Joints in Godot

**Goal:** doors on hinges, chains, wrecking balls and vehicles built from constrained bodies.

## Setup
Add a joint node, set `node_a` and `node_b` (NodePaths to PhysicsBody nodes; one may be a StaticBody
or empty so the world is the other body). The joint's transform defines the anchor point and axes.
With one body omitted, GodotPhysics treats the assigned body as `node_a`; Jolt treats it as `node_b`
(project setting Physics > Jolt Physics 3D > Joints > World Node switches this), so limits can invert
between engines. Assign single-body joints explicitly and test under the physics engine you ship.

## 3D joints
| Joint | Use | Key params |
|---|---|---|
| PinJoint3D | ball socket (chains, pendulums) | bias, damping, impulse_clamp |
| HingeJoint3D | doors, wheels, levers | angular_limit/enable, lower, upper; motor via flags and params |
| SliderJoint3D | pistons, drawers | linear_limit/lower_distance, upper_distance, damping |
| ConeTwistJoint3D | shoulders, ragdolls | swing_span, twist_span |
| Generic6DOFJoint3D | anything: per-axis linear/angular limits, springs, motors | flags per axis |
```gdscript
$Hinge.set_flag(HingeJoint3D.FLAG_ENABLE_MOTOR, true)
$Hinge.set_param(HingeJoint3D.PARAM_MOTOR_TARGET_VELOCITY, 2.0)
$Hinge.set_param(HingeJoint3D.PARAM_MOTOR_MAX_IMPULSE, 50.0)
```
Jolt ignores the soft-limit style properties of these nodes (PinJoint3D bias, damping, impulse_clamp;
HingeJoint3D bias, softness, relaxation; ConeTwistJoint3D bias, relaxation, softness), so do not tune
with them if you ship Jolt.

## 2D joints
PinJoint2D (softness, angular_limit_enabled, angular_limit_lower/upper), GrooveJoint2D (point slides
along a groove: length, initial_offset), DampedSpringJoint2D (rest_length, stiffness, damping, length).

## Breaking joints
The Joint classes expose no break-force property. Measure it yourself (compare body velocities or read
contact impulses), then `queue_free()` the joint or clear `node_b`.

## Stability tips
- `exclude_nodes_from_collision` (default true) stops connected bodies colliding with each other.
- Jolt solver quality is set by the project settings `simulation/position_steps` and
  `simulation/velocity_steps` under Physics > Jolt Physics 3D; raise them if long chains stretch.

## Verify
- [ ] Joint limits hold under player interaction; chains do not stretch or explode at expected loads.

## Checked
2026-10-28, Godot docs `stable` (latest release tag 4.7.2-stable). Confirmed from the HingeJoint3D, PinJoint3D,
ConeTwistJoint3D, SliderJoint3D, PinJoint2D, GrooveJoint2D, DampedSpringJoint2D, Joint3D class pages and the Jolt
Physics page: flag/param names, property names, `exclude_nodes_from_collision` default true, Jolt unsupported joint
properties, single-body node_a/node_b difference, Jolt step settings. Removed: hinge axis is local Z, "Godot has no
built-in break force" as absolute, 10:1 mass ratio figure, "Jolt more stable" claim, the GodotPhysics solver settings path, the no-overlap tip, "joint solver settings in Jolt",
"4.x" gate on PinJoint2D limits (the properties exist in 4.7).
Method: documentation only; no commands were run.

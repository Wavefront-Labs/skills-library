---
id: computing-software.game-programming.godot.jolt-physics
name: jolt-physics
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-physics, jolt-physics, physics-engine, 3d-physics, performance, game-programming]
level: practitioner
status: docs-checked
description: "Switch Godot 4 3D physics to Jolt (built in from 4.4, GDExtension before): enabling it, behaviour differences from Godot Physics, settings, and what to retest."
sources: ["https://docs.godotengine.org/en/stable/tutorials/physics/using_jolt_physics.html", "https://github.com/godot-jolt/godot-jolt"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Jolt physics in Godot

**Goal:** faster, more stable 3D physics (stacking, many bodies, joints) by switching engines safely.

## Enable
- Jolt was added in Godot 4.4 as a built-in alternative to Godot Physics. Set Project Settings > Physics >
  3D > **Physics Engine** to `Jolt Physics`, click **Save & Restart**. The docs state that new projects
  use it by default.
- The older Godot Jolt extension (github.com/godot-jolt/godot-jolt) is in maintenance mode: bug fixes
  and compatibility with new Godot versions until the built-in module has parity (joint-related items
  were the remaining gap). Its project settings moved from `physics/jolt_3d` to
  `physics/jolt_physics_3d`, several renamed (see the migration list in the docs).
- This is the 3D physics engine; 2D physics is not affected.

## Behaviour differences to check
- **Joints**: several joint properties are unsupported and emit a warning when set to non-default
  values (for example PinJoint3D `bias`, `damping`, `impulse_clamp`; HingeJoint3D `bias`, `softness`,
  `relaxation`). Retest ragdolls and doors.
- **Single-body joints**: Godot Physics treats a lone body as `node_a`; Jolt treats it as `node_b`
  (with `node_a` as the world). The setting `Physics > Jolt Physics 3D > Joints > World Node` restores
  the old behaviour.
- **Collision margins**: Jolt's convex radius first shrinks the shape and then rounds it, so the shape
  does not grow. The project setting `physics/jolt_physics_3d/collisions/collision_margin_fraction`
  (multiplied with the smallest AABB axis) sets the margin, and the shape's `margin` is an upper bound.
- **Penetration recovery**: Baumgarte stabilization is applied to position only, so it cannot
  overshoot but may take longer; tune `simulation/baumgarte_stabilization_factor` (0.0 off, 1.0 resolves
  in one step but is often unstable).
- **Ghost collisions**: active edge detection (`collisions/active_edge_threshold`) for
  `ConcavePolygonShape3D` and `HeightMapShape3D`, and enhanced internal edge removal
  (`simulation/use_enhanced_internal_edge_removal`, plus the queries and motion_queries variants).
- **Ray-cast face index**: `face_index` from `intersect_ray()` and RayCast3D is -1 by default under
  Jolt; `queries/enable_ray_cast_face_index` enables it (about 25% more memory for
  `ConcavePolygonShape3D`).
- **Kinematic RigidBody3D contacts**: a RigidBody3D frozen in kinematic mode does not report contacts
  with static or kinematic bodies by default; `simulation/generate_all_kinematic_contacts` opts in.
- **Contact impulses**: `get_contact_impulse()` values are estimated ahead of time and are accurate
  only when the two bodies collide with nothing else.
- **Area3D and SoftBody3D**: Jolt also emits Area3D overlap signals for soft bodies (Godot Physics does
  not); set the area's mask to avoid the soft body's layer to revert to the old behaviour.
- **Areas and static bodies**: the setting is `physics/jolt_physics_3d/simulation/areas_detect_static_bodies`
  (previously `collisions/areas_detect_static_bodies` in the extension).
- **WorldBoundaryShape3D**: the effective plane size is much smaller under Jolt, configurable with
  `limits/world_boundary_shape_size`.
- **Memory and sleeping**: the stack allocator is sized by `limits/temporary_memory_buffer_size`; sleep
  settings are `simulation/allow_sleep`, `sleep_velocity_threshold` and `sleep_time_threshold`.

## Process
1. Branch, switch engine, run every physics-heavy scene; watch the Output for Jolt warnings.
2. Profile before and after (for example Debugger > Monitors).
3. Keep Godot Physics as fallback until gameplay tests pass.

## Verify
- [ ] No Jolt warnings about unsupported settings in Output.
- [ ] Character movement, ragdolls and vehicles pass playtests; physics time improved in Monitors.

## Checked

2026-10-25, against godot-docs master ("latest" docs, last commit 2026-10-24). Confirmed in the Using Jolt Physics page: added in 4.4, built in, default for new projects, the Physics Engine setting, extension in maintenance mode, unsupported joint properties, single-body joints and the World Node setting, collision margin fraction, Baumgarte stabilization, ghost collision settings, ray-cast face index, kinematic contacts, contact impulses, Area3D and SoftBody3D, WorldBoundaryShape3D, memory and sleep setting names and the project setting migration list. Removed unsourced performance claims, the pre-4.4 install steps and the CharacterBody3D remark.

Method: documentation only; no commands were run.

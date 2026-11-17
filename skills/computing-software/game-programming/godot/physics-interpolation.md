---
id: computing-software.game-programming.godot.physics-interpolation
name: physics-interpolation
category: computing-software
field: game-programming
product: godot
tags: [godot, godot-physics, physics-interpolation, fixed-timestep-smoothing, reset_physics_interpolation, game-programming]
level: practitioner
status: docs-checked
description: "Enable Godot physics interpolation to decouple physics tick from frame rate: project setting, moving objects in _physics_process, teleport resets and camera handling."
sources: ["https://docs.godotengine.org/en/stable/tutorials/physics/interpolation/physics_interpolation_introduction.html", "https://docs.godotengine.org/en/stable/tutorials/physics/interpolation/using_physics_interpolation.html", "https://docs.godotengine.org/en/stable/tutorials/physics/interpolation/advanced_physics_interpolation.html", "https://docs.godotengine.org/en/stable/tutorials/physics/interpolation/2d_and_3d_physics_interpolation.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Physics interpolation

**Goal:** smooth motion at any refresh rate (144 Hz monitors with 60 Hz physics, or low physics tick
rates) without jitter.

## Enable
Project Settings > Physics > Common > **Physics Interpolation** (`physics/common/physics_interpolation`,
default false). Physics Ticks Per Second stays e.g. 60; rendering interpolates node transforms between
the last two physics ticks. The jitter fix is automatically disabled at runtime when interpolation is
enabled (set `physics/common/physics_jitter_fix` to 0.0 only for a custom interpolation solution).

## Rules once enabled
1. Move physics-driven and gameplay objects **only in `_physics_process`** (or via physics). Setting
   the transform of interpolated objects outside the physics tick makes the interpolated position
   incorrect and causes jitter for some players; indirect movement (tweens, animation, navigation, moving a
   parent) should also run on the physics tick.
2. **Teleports**: after setting a position instantly (spawn, respawn, portal), call
   `reset_physics_interpolation()` on the node so it doesn't visibly streak from the old position.
   Order matters: set the transform first, then call it. For a projectile that should start moving at
   once, also set the transform expected after the first tick, right after the reset.
3. **Cameras**: Camera3D can use automatic interpolation like any node. For mouse look or a manually
   followed target, set the camera's `physics_interpolation_mode` to Off and update it in `_process`;
   use `get_global_transform_interpolated()` of the target (only for special cases such as cameras).
4. Per-node control: `physics_interpolation_mode` Inherit / On / Off. Turn it off for UI-like or
   per-frame-animated nodes.

## Reading interpolated transforms
`Node3D.get_global_transform_interpolated()` gives the interpolated transform during `_process` (3D
only; use it sparingly, for cases such as a manually-updated camera).

## Without the setting (manual)
Keep previous and current transforms per tick, and in `_process` lerp a visual child using
`Engine.get_physics_interpolation_fraction()`.

## Gotchas
- Interpolation effectively shows the past: expect a slight delay to input, which can matter in fast
  twitch games; a higher tick rate mitigates it.
- In 2D only `CPUParticles2D` are interpolated (GPU 2D particles are not); in 3D, bodies created
  through the low-level servers are not interpolated and need manual interpolation. MultiMeshes are
  supported in 2D and 3D.

## Verify
- [ ] Set physics ticks to 10 temporarily (the documented test): interpolated movement still looks smooth.
- [ ] Respawn shows no slide from death position.

## Checked

2026-10-25, against godot-docs master ("latest" docs, last commit 2026-10-24). Confirmed in the physics interpolation tutorials (introduction, quick start, using, advanced, 2D and 3D differences) and the ProjectSettings and Engine class pages: setting name and default, jitter fix disabled automatically when interpolation is enabled, move logic in _physics_process, reset_physics_interpolation order and the two usage patterns, camera guidance with physics_interpolation_mode and get_global_transform_interpolated, Engine.get_physics_interpolation_fraction for the manual method, input delay trade-off and the 10 tick test. The release version gates for 2D and 3D support and the slerp claim were removed as unconfirmed.

Method: documentation only; no commands were run.

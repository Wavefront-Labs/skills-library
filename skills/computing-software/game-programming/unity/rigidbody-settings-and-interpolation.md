---
id: computing-software.game-programming.unity.rigidbody-settings-and-interpolation
name: rigidbody-settings-and-interpolation
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-physics, unity-rigidbody, interpolation, collision-detection-mode, continuous-dynamic, kinematic-rigidbody, mass, linearvelocity, physx, game-programming]
level: practitioner
status: docs-checked
description: "Configure Unity Rigidbody: mass and damping, kinematic vs dynamic, interpolation for smooth visuals, and collision detection modes for fast objects."
sources: ["https://docs.unity3d.com/Manual/class-Rigidbody.html", "https://docs.unity3d.com/Manual/rigidbody-interpolation.html", "https://docs.unity3d.com/Manual/ContinuousCollisionDetection.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rigidbody settings and interpolation

**Goal:** physics objects that look smooth, do not tunnel through colliders, and respond predictably.

## Key properties (Rigidbody component reference)
| Property | What the Manual says |
|---|---|
| Mass | In kilograms, default 1. Mass does not affect how quickly an item falls under gravity; use damping for resistance. |
| Linear Damping / Angular Damping | Decay rate of linear / rotational velocity (drag, air resistance, friction). Low values decay slowly, high values decay fast. Angular Damping defaults to 0.05; infinite Angular Damping does not stop rotation. |
| Automatic Center Of Mass / Automatic Tensor | Use the physics system's predicted values from shape, scale and connected colliders; disable to set your own. |
| Use Gravity | On by default; force acts down the y axis by default. |
| Is Kinematic | Off by default. When on, the physics system cannot apply forces to move or rotate the object; Unity moves it via its Transform. |
| Interpolate | None (default), Interpolate, Extrapolate. |
| Collision Detection | Discrete (default), Continuous, Continuous Dynamic, Continuous Speculative. |
| Constraints | Freeze Position (world axes) and Freeze Rotation (local axes), selectively per axis. |
Layer Overrides (Layer Override Priority, Include Layers, Exclude Layers) override project-wide layer collision
settings for all colliders on that Rigidbody; the higher priority value wins when overrides conflict.

## Interpolation
Jitter appears when the physics rate (Fixed Timestep) is slower than the frame rate, and is most noticeable on a
physics-driven Rigidbody the camera tracks. Use interpolation or extrapolation only if you see jitter.
- **Interpolate** (`RigidbodyInterpolation.Interpolate`): uses the poses from the previous two physics updates;
  more accurate but lags one physics update. Best when velocity varies or other physics affects the body.
- **Extrapolate** (`RigidbodyInterpolation.Extrapolate`): predicts from the previous update's pose and velocity;
  appears slightly ahead, can visibly overshoot collision bounds and then correct. Suits constant-velocity
  bodies where accuracy is not important.
- With either enabled, the physics system controls the Rigidbody's transform: follow any direct (non-physics)
  transform change with `Physics.SyncTransforms`, otherwise Unity ignores transform changes that did not come
  from the physics system.

## Collision detection modes
| Mode | Documented use |
|---|---|
| Discrete | Not involved in fast-moving collisions; least computation. |
| Continuous | Sweep-based CCD against static colliders (no Rigidbody). |
| Continuous Dynamic | Sweep-based CCD against all other colliders except those set to Discrete. |
| Continuous Speculative | Speculative CCD against all colliders; for when accuracy is not important; cheaper than the sweep-based modes but costlier than Discrete. |
CCD supports Box, Sphere and Capsule colliders. It is a safety net, not always physically accurate; decreasing the
physics timestep may make the simulation more precise.

## Verify
- [ ] Camera-followed body shows no jitter when Interpolate is on.
- [ ] A fast test object does not pass through a thin collider with the chosen CCD mode.

## Checked
Date 2026-11-09. Read in full as fetched text: Rigidbody component reference, Apply interpolation to a Rigidbody,
Continuous collision detection overview. Confirmed all property defaults, interpolation behaviour,
`SyncTransforms` requirement, CCD mode semantics and collider support.
Removed as unconfirmed: the mass ratio limit, Unity 6 rename notes, force and velocity movement recipes,
`MovePosition` advice, the "never set transform.position" rule, thickness-per-step rule of thumb, sleeping and
solver iteration notes, mesh collider convexity, 50 Hz default and debris cost advice.
Method: documentation only; no commands were run.

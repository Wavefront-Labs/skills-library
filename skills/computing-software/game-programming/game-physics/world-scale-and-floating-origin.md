---
id: computing-software.game-programming.game-physics.world-scale-and-floating-origin
name: world-scale-and-floating-origin
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, floating-origin, world-scale, large-worlds, game-programming]
level: practitioner
status: gated
description: "Handle large worlds: float precision at distance, unit scale choices, floating origin rebasing, double-precision positions and physics engine options."
sources: ["https://docs.unrealengine.com/5.3/en-US/large-world-coordinates-in-unreal-engine-5/", "https://jrouwe.github.io/JoltPhysics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# World scale, units and floating origin

**Goal:** keep physics and rendering stable kilometres from the origin.

## Float precision
A 32-bit float has 24 bits of mantissa: precision is about `|x| * 6e-8`.
| Distance | Step |
|---|---|
| 1 km | ~0.06 mm |
| 10 km | ~1 mm |
| 100 km | ~8 mm |
(computed with `numpy.spacing(float32)`: 0.061 mm, 0.98 mm, 7.8 mm.)
Physics contact tolerances (slop ~5 mm), animation and camera jitter show up well before that.

## Units
- Use metres and kg (engines tune defaults for human-scale objects of 0.1-10 m). Unreal uses cm (gated: unconfirmed, source is paywalled or blocked),
  Box2D expects metres (don't use pixels; convert at render).
- Extremely small (cm-sized dice) or huge (100 m ships) objects need retuned slop, margins and sleep
  thresholds.

## Floating origin
Periodically shift the world so the player is near (0,0,0):
1. When player distance from origin exceeds a threshold (e.g. 1-5 km), choose offset = player position (snapped to a grid).
2. Subtract offset from every body, particle, transform, nav data and audio emitter; keep a global
   `worldOffset` (double) for absolute coordinates.
3. For physics engines: PhysX has `PxScene::shiftOrigin`; Jolt's `PhysicsSystem` has no shift call (not found in the
   headers), so move bodies directly between steps (for example with `BodyInterface::SetPosition`).
Do it between frames, not mid-step, and notify systems with cached world positions.

## Double precision
- Unreal 5 Large World Coordinates: 64-bit doubles in core data types and positions; the GPU-side handling is not
  described on the overview page (gated: unconfirmed, source is paywalled or blocked).
- Jolt: compile with `JPH_DOUBLE_PRECISION` for double body positions.
- Render relative to camera (camera-relative rendering) even when simulation uses doubles.

## Multiplayer
Each client can use its own floating origin; network positions in absolute (double or fixed-point
sector + local offset) coordinates.

## Verify
- Stack boxes at 0 and at 50 km; compare jitter. Walk across a rebase boundary: no visible pop.

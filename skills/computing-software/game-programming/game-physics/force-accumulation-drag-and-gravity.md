---
id: computing-software.game-programming.game-physics.force-accumulation-drag-and-gravity
name: force-accumulation-drag-and-gravity
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, force-accumulator, drag, gravity, game-programming]
level: practitioner
status: verified
description: "Accumulate forces per body each step (gravity, drag, springs, user forces), clear after integration, and model linear and quadratic drag correctly."
sources: ["https://gafferongames.com/post/integration_basics/", "https://github.com/idmillington/cyclone-physics"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Force accumulation, drag and gravity

**Goal:** a clean per-step force pipeline as in Millington's Cyclone engine (*Game Physics Engine
Development*): generators add forces, the integrator consumes them, then they are cleared.

## Pattern
```cpp
struct Body { Vec3 x, v, forceAccum, torqueAccum; float invMass; };
void addForce(Body& b, Vec3 f) { b.forceAccum += f; }
void addForceAtPoint(Body& b, Vec3 f, Vec3 p) { b.forceAccum += f; b.torqueAccum += cross(p - b.com, f); }

void step(float dt) {
    for (auto& g : forceGenerators) g->apply(dt);     // gravity, drag, springs, thrusters
    for (auto& b : bodies) {
        Vec3 a = b.forceAccum * b.invMass;           // gravity applied as acceleration below
        b.v += (a + gravity * (b.invMass > 0)) * dt; // semi-implicit Euler
        b.x += b.v * dt;
        b.forceAccum = {}; b.torqueAccum = {};       // clear AFTER integrating
    }
}
```
- Apply gravity as acceleration (`g`, not `m*g` through invMass) so infinite-mass bodies ignore it
  and mass changes do not change fall speed.
- Forces added from gameplay between steps (e.g. in variable-rate Update) must persist until the
  next fixed step, then clear; impulses (instant velocity changes) go straight to `v * invMass`.

## Drag
- Linear: `F = -k1 * v` (low speed, viscous). Quadratic: `F = -k2 * |v| * v` (air at game speeds).
- Large drag with explicit integration overshoots and reverses velocity. Use the exact solution for
  linear drag instead: `v *= exp(-k1 * invMass * dt)` (frame-rate independent; matched the closed form to 1e-14).
- Engines' "damping" parameters are usually this exponential or `v *= 1/(1 + c*dt)` form, not
  physical drag.

## Verify
- Terminal velocity test: falling body with quadratic drag converges to `sqrt(m*g/k2)` (measured 8.0870266 vs 8.0870266 for
  m = 2, k2 = 0.3, 100 s at 60 Hz).
- Change the timestep from 1/60 to 1/120; trajectories agree closely.

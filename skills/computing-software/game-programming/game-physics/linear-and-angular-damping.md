---
id: computing-software.game-programming.game-physics.linear-and-angular-damping
name: linear-and-angular-damping
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, angular-damping, linear-damping, rigid-body, game-programming]
level: practitioner
status: verified
description: "Set linear and angular damping correctly: exponential vs linear decay, timestep-independent formulas, engine conventions and damping as a stability tool."
sources: ["https://box2d.org/documentation/md_simulation.html", "https://nvidia-omniverse.github.io/PhysX/physx/5.4.1/docs/RigidBodyDynamics.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linear and angular damping

**Goal:** bleed off motion predictably for feel and stability without frame-rate dependence.

## Formulas
- Naive per-step `v *= 0.98` decays faster at higher step rates: frame-rate dependent.
- Exact exponential: `v *= exp(-c * dt)`. Timestep independent; `c` is in 1/s.
- Box2D v3 uses `v *= 1 / (1 + dt * linearDamping)` (confirmed in `solver.c`), close to exponential for
  small `c*dt` and stable for any dt. Its docs say the damping is approximated, so results depend slightly on the step:
  c = 0.5 for 1 s from 10 gives 6.090 at 30 Hz, 6.078 at 60 Hz, 6.072 at 120 Hz vs 6.065 exact.
- PhysX: `PxRigidBody::setLinearDamping` / `setAngularDamping` (defaults 0.0 linear and 0.05 angular for a
  `PxRigidDynamic`). Unity 6 exposes these as `Rigidbody.linearDamping`/`angularDamping` (formerly drag/angularDrag).
  Jolt's `BodyCreationSettings` default both to 0.05.

Half-life form for designers: `c = ln(2) / halfLife`.

## Uses
- **Feel:** space games use low linear damping; arcade objects use higher damping to settle fast.
- **Stability:** a little angular damping stops numerical spin-up of long bodies and jittery
  stacks; ragdolls usually want more angular damping than rigid props (tune per rig; Box2D's own example uses 0.1).
- **Fake air drag:** linear damping approximates viscous drag; use quadratic drag when speed matters
  (projectiles, parachutes).
- **Sleeping:** damping helps bodies reach the sleep velocity threshold sooner.

## Pitfalls
- Damping slows falling too (it damps gravity-driven velocity), so heavily damped objects fall like
  feathers; damp only horizontal velocity if needed, by hand.
- Angular damping on wheels kills rolling; set per body type.
- High damping masks solver problems; fix the root cause first.

## Verify
- Spin a body at 10 rad/s, measure time to half speed at 30, 60, 120 Hz: identical with the
  exponential form (and within about 0.4% at 30 Hz with Box2D's form for c = 0.5).

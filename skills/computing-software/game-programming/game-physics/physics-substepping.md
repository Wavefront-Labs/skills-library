---
id: computing-software.game-programming.game-physics.physics-substepping
name: physics-substepping
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, physics-substepping, substeps, solver-iterations, timestep, stability, game-programming]
level: advanced
status: gated
description: "Use physics substepping to stabilise stiff joints, stacks and fast objects: substeps vs solver iterations, Box2D v3/Jolt/Chaos/PhysX settings, and the CPU cost."
sources: ["https://box2d.org/posts/2024/02/solver2d/", "https://jrouwe.github.io/JoltPhysics/", "https://dev.epicgames.com/documentation/en-us/unreal-engine/physics-sub-stepping-in-unreal-engine", "https://matthias-research.github.io/pages/publications/smallsteps.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Physics substepping

**What it is:** splitting one game physics step `dt` into `n` smaller steps of `dt/n`, each doing
integration and (some) constraint solving. Research (Macklin et al., "Small Steps in Physics
Simulation") and Box2D v3's soft-step solver show that **more substeps with fewer iterations each
beats many iterations in one big step** for stiffness and stability.

## Substeps vs iterations
| Knob | Effect | Cost |
|---|---|---|
| Solver iterations (velocity/position) | Better convergence within a step; stacks less soft | per iteration over all contacts |
| Substeps | Smaller dt: stiff springs and joint chains stable, less tunnelling, better high mass ratios | full pipeline per substep (often broadphase/contact gen reused) |
| Smaller global fixed step | Same benefit for everything including gameplay | gameplay code runs more often too |

## Engine knobs
- **Box2D v3:** `b2World_Step(world, timeStep, subStepCount)`; default 4 substeps is the intended
  setting; contacts are generated once per step, solved with relaxation across substeps.
- **Jolt:** `PhysicsSystem::Update(dt, collisionSteps, tempAllocator, jobSystem)`; its docs say the system is stable at 60 Hz
  with 1 collision step (so 2 at a 1/30 s step). Velocity/position iteration counts in `PhysicsSettings`.
- **Unreal (Chaos):** Project Settings > Physics: *Substepping* (with Max Substep Delta Time, Max
  Substeps) or *Async Physics* with a fixed tick; per-substep custom force callbacks exist in Chaos (`FCalculateCustomPhysics`) (gated: unconfirmed, source is paywalled or blocked).
- **Unity (PhysX):** no per-body substeps; lower `Time.fixedDeltaTime` or raise
  `Physics.defaultSolverIterations`/`defaultSolverVelocityIterations` (per body via
  `Rigidbody.solverIterations`); Unity has no per-body substep setting (gated: unconfirmed, source is paywalled or blocked).
- **Godot:** raise `physics/common/physics_ticks_per_second`; the Jolt module exposes
  `physics/jolt_physics_3d/simulation/velocity_steps`.

## Forces in substeps
Forces you apply once per game step are held constant across substeps. Springs or controllers that
depend on state (suspension, PD controllers for active ragdolls) must be evaluated **per substep**
(Unreal custom physics callback, Jolt step listener `PhysicsStepListener`) or they become unstable.

## When to use what
- Joint chains (ropes, ragdolls, vehicles) stretching: substeps first.
- Tall stacks jittering: substeps or more position iterations plus sleeping.
- Fast thin bullets tunnelling: CCD or ray casts, not substeps.
- Whole game feels floaty at 30 Hz: raise the base rate.

## Verify
- [ ] Profile CPU per substep count; pick the lowest that passes the stability test scene.
- [ ] Stress scene (10-box stack, 20-link chain with heavy end, vehicle at top speed) stable at target fps.

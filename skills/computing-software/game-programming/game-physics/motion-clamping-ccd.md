---
id: computing-software.game-programming.game-physics.motion-clamping-ccd
name: motion-clamping-ccd
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, motion-clamping, ccd, tunnelling, game-programming]
level: practitioner
status: verified
description: "Implement motion clamping CCD: sweep fast bodies, clamp their step to time of impact, then resolve, with the time-loss and multi-hit trade-offs."
sources: ["https://github.com/bulletphysics/bullet3", "https://github.com/erincatto/box2d", "https://nvidia-omniverse.github.io/PhysX/physx/5.4.1/docs/AdvancedCollisionDetection.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Motion clamping

**Goal:** the simplest robust CCD: never let a fast body move past its first time of impact this step.

## Algorithm
1. Integrate velocities as usual.
2. For bodies flagged fast (speed * dt > fraction of their smallest extent), sweep the shape (or a
   smaller inner sphere) from current to predicted position.
3. If the sweep hits at fraction `t < 1`, move the body only to `t` (minus a small skin), keep its
   velocity, and let next step's discrete contact resolve the collision.

Bullet's version: `setCcdMotionThreshold(threshold)` and `setCcdSweptSphereRadius(r)` on
`btCollisionObject` (so on `btRigidBody` too); CCD is skipped when the motion in one step is below the threshold, and
otherwise a swept sphere of radius `r` (default 0) clamps the motion to the first hit. Box2D decides a body is
'fast' when its motion over a step exceeds `safetyFactor` (default 0.5, recommended 0.01 to 0.5) times the distance that risks tunnelling.

## Trade-offs
- **Time loss:** the body loses the remaining `(1 - t) * dt` of motion this frame and appears to
  stall briefly at impact (Jolt's LinearCast comments: time is stolen; PhysX with `ccdMaxPasses` = 1: remaining time is dropped).
  In a 300 m/s test at 60 Hz the mean lost time was 0.99 ms of the 16.7 ms step.
- **Only first hit:** two walls hit in one step still resolve one per frame (PhysX: raise `ccdMaxPasses`).
- **Static-only by default:** Box2D's continuous mode is against static bodies, with `isBullet` adding dynamic and kinematic ones;
  the header warns that two fast bodies can still be missed.
- Inner swept sphere smaller than the shape avoids clamping against things the shape grazes (Bullet's swept sphere radius).

## Tuning
- Jolt's LinearCast defaults: cast only when the body moves more than 0.75 of its inner radius per step, allow 0.25 of the inner radius of penetration; start from engine defaults and tune against a tunnelling test.
- Restrict to classes that need it (projectiles, player at high speed) to bound cost.

## Verify
- Fire a body at 300 m/s into a 5 cm wall 1,000 times; zero tunnels, measure average stall time.

## Checked (2026-10-22)
- Python test of the algorithm (0.1 m sphere at 300 m/s, 60 Hz, 5 cm wall 10 m away, 1000 random start offsets): discrete detection tunnelled in 799 of 1000 shots, motion clamping in 0; mean time lost 0.99 ms.
- Bullet `btCollisionObject.h` (fetched from master): `setCcdMotionThreshold`, `setCcdSweptSphereRadius` live there, motion threshold comment, swept sphere radius default 0. Box2D `solver.c` fast-body test with `safetyFactor * minExtent`, `types.c` default 0.5, `types.h` recommended range and `isBullet` warning. Jolt `MotionQuality.h` ('time is stolen') and `PhysicsSettings.h` defaults. PhysX AdvancedCollisionDetection page: remaining time dropped with one pass.
- Removed the attribution to Erin Catto's GDC 2013 talk (the GDC Vault page is not retrievable here; all deep GDC links return the same placeholder page) and the unverified tuning ratios.

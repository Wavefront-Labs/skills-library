---
id: computing-software.game-programming.game-physics.rotational-ccd-and-thin-objects
name: rotational-ccd-and-thin-objects
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, rotational-ccd, thin-objects, ccd, game-programming]
level: practitioner
status: verified
description: "Stop fast-spinning or thin objects tunnelling: why linear sweeps miss rotation, angular CCD, speculative margins and minimum thickness rules."
sources: ["https://box2d.org/documentation/", "https://nvidia-omniverse.github.io/PhysX/physx/5.4.1/docs/AdvancedCollisionDetection.html", "https://github.com/jrouwe/JoltPhysics"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Rotational CCD and thin objects

**Goal:** stop a spinning plank, propeller or sword passing through walls even when its centre moves slowly.

## Why linear CCD misses
Many CCD schemes sweep the shape's *translation* only (or the centre of mass). A long object
rotating fast moves its tips far more than its centre: tip speed = `omega * r`. A 2 m plank at
20 rad/s has 20 m/s tips while the centre is still.

## Options
- **Full TOI with rotation:** conservative advancement bounds motion by
  `|v| + |omega| * r_max` per unit time, so it handles rotation; Box2D's `b2ComputeTimeOfImpact` sweeps
  both position and angle (`b2Sweep` holds start and end centre and rotation), and its solver measures motion as `|v| + |w| * maxExtent`.
- **PhysX:** standard sweep-based CCD (`PxRigidBodyFlag::eENABLE_CCD`) handles linear motion only (the docs call it 'linear CCD');
  `eENABLE_SPECULATIVE_CCD` catches fast angular motion (it inflates contact offsets from object motion), and since PhysX 5 both can be on together.
- **Jolt:** `LinearCast` motion quality does not cover this: Jolt's header says long thin bodies with high angular velocity can still tunnel.
- **Speculative contacts:** generate contacts within a margin covering predicted motion including
  `omega * r`; cheap and handles rotation, can cause ghost hits.
- **Substepping:** halve dt for the fast object or the whole sim.
- **Angular velocity clamp** as a last resort (`maxAngularVelocity`).

## Thin objects
- Thin *static* walls: thickness at least `v_max * dt` for discrete detection, or rely on CCD.
  Use thick back-faced collision behind thin visual walls.
- Thin *dynamic* objects (coins, cards): give collision shapes artificial thickness and a convex
  shape; enable CCD.

## Verify
- Test rig: spin a plank at increasing omega against a 1 cm wall; record the speed at which it
  tunnels before and after enabling angular CCD.

## Checked (2026-10-22)
- Python check of the tip-speed arithmetic (2 m plank, 20 rad/s: tip 20 m/s, 19.1 degrees per 60 Hz step) and of a tip crossing a 1 cm wall at x = 0.5: a discrete test at step end never hit at omega = 1, 5, 20, 60 rad/s, while a swept-angle test caught it at 5, 20 and 60, matching the 'why linear/discrete CCD misses' argument.
- Box2D main `collision.h` (`b2ComputeTimeOfImpact`, `b2Sweep` with q1/q2; the old name `b2TimeOfImpact` does not exist) and `solver.c` (`|v| + |w| * maxExtent`). PhysX 5.4.1 AdvancedCollisionDetection page (linear vs angular CCD, both together in PhysX 5). Jolt master `MotionQuality.h` comment.
- Removed the claim that speculative CCD in PhysX works by an 'angular-motion bound' (the docs only say contact offsets are inflated based on object motion).

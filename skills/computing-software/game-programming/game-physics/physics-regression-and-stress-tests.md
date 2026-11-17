---
id: computing-software.game-programming.game-physics.physics-regression-and-stress-tests
name: physics-regression-and-stress-tests
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, physics-regression-test, stress-test, determinism, game-programming]
level: practitioner
status: verified
description: "Build physics regression and stress tests: scripted scenes with state hashes, tolerance checks, performance budgets and CI runs across platforms."
sources: ["https://github.com/erincatto/box2d/tree/main/samples", "https://github.com/jrouwe/JoltPhysics"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Physics regression and stress tests

**Goal:** catch physics behaviour and performance regressions before players do.

## Test scenes
Keep a library of headless scenes, each a pure function of code + seed:
- Pyramid/stack (stability), domino chain (sequencing), ragdoll pile (joints), vehicle on a track,
  fast projectiles vs thin walls (CCD), character walking a gauntlet (slopes, steps, moving platforms).
- Box2D's `samples` and Jolt's Samples app/PerformanceTest are good models; Jolt's
  PerformanceTest hashes all body positions and rotations (plus scene state), prints the hash per motion quality and thread count,
  and `-validate_hash=<hash>` returns 0 on a match and 1 on a mismatch.

## Checks
1. **Determinism hash:** run N steps, hash positions/velocities bitwise; compare to golden per
   platform/compiler. Any change means behaviour changed; intentional changes update the golden.
2. **Tolerance assertions:** for behaviour tests that can legitimately drift, assert outcomes
   (stack still standing: top box height within 1 cm; projectile hit count 1000/1000).
3. **Invariants every step:** no NaN, max penetration under threshold, energy not increasing in
   closed scenes, sleeping count eventually equals body count.
4. **Performance budget:** step time median and p99 for each scene, fail if worse than baseline by X%.

## Running
- Headless executable with `--scene name --steps 3000 --hash`; run in CI on each target platform.
- Run determinism tests at a fixed thread count first, then at other thread counts to catch races (Box2D's docs claim multithreaded
  determinism from creation order; Jolt's PerformanceTest prints one hash per thread count).
- Store reports as artifacts; graph step time over commits.

## Debugging failures
Record the scene for physics visual debuggers (PVD, Jolt `DebugRenderer` recorder) when a test
fails and attach it to the CI run.

## Verify
- Introduce a deliberate change (solver iteration count) and confirm the hash test fails (a pymunk pyramid hashed identically on two runs
  and differently when `iterations` went from 10 to 4).

## Checked (2026-10-22)
- Ran a pymunk 7.3.1 pyramid (30 boxes, 600 steps, positions and velocities hashed with sha256): two runs give the same hash (944d05249390b863), `space.iterations = 4` gives a different one (335f29cd3a7aed46), so the skill's 'change the iteration count and expect a golden mismatch' check works.
- Jolt master `PerformanceTest/PerformanceTest.cpp`: `-validate_hash=` option, hash of positions and rotations, output column header 'Motion Quality, Thread Count, Steps / Second, Hash'. Box2D docs (`simulation.md`): determinism from creation order across threads, custom trig, compiler flags; Box2D `samples` directory exists. JoltViewer and the Jolt debug-renderer recorder exist (see physics-debug-visualisation).

---
id: computing-software.game-programming.game-physics.stack-stability-in-rigid-body-solvers
name: stack-stability-in-rigid-body-solvers
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, stacking-stability, warm-starting, solver-iterations, game-programming]
level: practitioner
status: verified
description: "Make box stacks and piles stable: warm starting, contact ordering, iterations vs substeps, relax and restitution handling, and sleeping."
sources: ["https://box2d.org/files/ErinCatto_SequentialImpulses_GDC2006.pdf", "https://box2d.org/posts/2024/02/solver2d/", "https://github.com/erincatto/box2d"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stack stability

**Goal:** a tower of boxes that stands still instead of jittering, sinking or exploding.

## What makes stacks hard
Iterative solvers propagate impulses one contact at a time; a 10-high stack needs many iterations
for the bottom contact to "feel" the top box. Position correction adds energy; mass ratios worsen it.

## Techniques
1. **Persistent contact manifolds** with matched contact ids across frames (feature ids), so impulses
   can be reused.
2. **Warm starting:** apply last frame's accumulated impulses at the start of the solve. The single
   biggest win for stacks (1D 10-box stack, 4 iterations: residual speed 1.78 m/s without it, 0.0004 with it).
3. **Accumulated impulse clamping** (not per-iteration clamping) so impulses can decrease without
   going negative (with warm starting, per-iteration clamping left 9.9 m/s residual after 10 iterations, accumulated clamping 1e-7).
4. **Soft step / substepping** (Box2D v3, from Erin Catto's Solver2D comparison): several substeps
   with one iteration each plus a relax pass beats many iterations in one step; soft contacts
   avoid Baumgarte energy injection (Box2D v3 README: 'Soft Step' solver; docs recommend 4 sub-steps).
5. **Split impulses / pseudo-velocities** for penetration recovery so recovery velocity does not
   become real velocity.
6. **Restitution threshold:** ignore restitution below a relative speed threshold (Jolt `mMinVelocityForRestitution` defaults to 1 m/s), or resting
   contacts bounce forever.
7. **Sleeping islands** to freeze settled stacks.
8. **Contact solve order:** solving bottom-up (sorted by height) helped a little in the 1D test (residual 0.00035 vs 0.00044 m/s with warm starting, 1.78 vs 2.15 cold)
   and graph colouring is used by Box2D v3 (24 colours), but order-dependence also hurts determinism; prefer warm starting.

## Tuning signals
- Sinking: penetration slop too large or too few iterations (without warm starting the fastest-sinking box moved 1.49 m in 1 s at 4 iterations, 0.62 at 10, 0.17 at 30; with warm starting 0.028, 0.011, 0.003).
- Jitter: no warm starting, contact points not persistent, or restitution on resting contacts.
- Explosion: overlapping spawns; spawn with separation or limit `maxDepenetrationVelocity`.

## Verify
- Pyramid of 20 rows settles and sleeps within a few seconds at 60 Hz; record top-box drift.

## Checked (2026-10-22)
- 1D sequential-impulse stack in Python (10 unit boxes, 60 Hz): warm start on/off, iteration counts 1/4/10/30, accumulated vs per-iteration clamping, bottom-up vs top-down order, heavy top box ratios 1 to 1000, sink distance over 1 s; all numbers above are from these runs (see constraint-solvers-and-joints for the mass-ratio figures).
- Erin Catto GDC 2006 PDF (pypdf): contact ids matched across frames, persistence of accumulated impulses, accumulated impulse clamping, bias impulse. Box2D main: `B2_GRAPH_COLOR_COUNT 24`, README 'Soft Step', docs on sub-steps (recommended 4). Jolt `PhysicsSettings.h`: `mMinVelocityForRestitution = 1.0`, `mConstraintWarmStart`.
- Only Jolt's restitution threshold value is stated (no Box2D equivalent was matched). Pyramid-of-20-rows verify item was not run (it needs a full 2D engine); it is a benchmark suggestion, not a claim.

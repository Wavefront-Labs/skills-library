---
id: computing-software.game-programming.game-engine-architecture.two-bone-ik-and-fabrik-solvers
name: two-bone-ik-and-fabrik-solvers
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, two-bone-ik-solver, fabrik, inverse-kinematics, game-programming]
level: practitioner
status: draft
description: "Implement IK solvers: analytic two-bone IK with pole vectors for limbs, FABRIK for chains, foot placement and look-at, plus joint limits and blending."
sources: ["https://theorangeduck.com/page/simple-two-joint"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IK solvers: two-bone and FABRIK

**Goal:** adjust animated poses so feet land on terrain, hands reach targets, heads look at things.

## Two-bone analytic IK (arms, legs)
Given root A, mid B, end C, target T, upper length `l1 = |B-A|`, lower `l2 = |C-B|`:
1. Clamp target distance `d = clamp(|T-A|, eps, l1 + l2 - eps)`.
2. Law of cosines for desired interior angles:
   `angleA = acos((l1^2 + d^2 - l2^2) / (2*l1*d))`, `angleB = acos((l1^2 + l2^2 - d^2) / (2*l1*l2))`.
3. Rotate B so the knee angle matches, then rotate A to point the chain at T.
4. **Pole vector** defines the bend plane (knee forward, elbow back): compute the plane from A, T and
   the pole position.
Closed form, exact, stable (Daniel Holden's *Simple Two Joint IK* is a compact implementation).

## FABRIK (Aristidou and Lasenby)
Iterative for any chain length:
```text
repeat until |end - T| < tol or max iters:
  backward: set end = T; for i from end-1 down to 0: p[i] = p[i+1] + normalize(p[i]-p[i+1]) * len[i]
  forward:  set p[0] = root; for i from 1..n: p[i] = p[i-1] + normalize(p[i]-p[i-1]) * len[i-1]
```
Then convert positions back to joint rotations. Add joint limits by constraining each direction
within a cone after each step. Good for tails, tentacles, spines.

## Foot placement
Raycast down from each foot's animated position, set IK target to the hit plus ankle height, align
foot to the surface normal, lower the pelvis by the largest needed drop, blend IK weight with
animation curves (0 when foot is lifted).

## Pitfalls
- Unreachable targets: clamp, don't let the solver snap joints straight and pop.
- Knee flipping when target passes through the pole plane; smooth the pole.
- Solve in model space after animation sampling, before skinning.

## Verify
- Debug draw targets and pole vectors; walk up stairs and slopes, no foot penetration or knee pops.

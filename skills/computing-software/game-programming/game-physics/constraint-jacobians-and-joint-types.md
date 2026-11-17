---
id: computing-software.game-programming.game-physics.constraint-jacobians-and-joint-types
name: constraint-jacobians-and-joint-types
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, constraint-jacobian, joints, sequential-impulses, game-programming]
level: practitioner
status: verified
description: "Derive joint constraints as Jacobians: position constraint, velocity constraint, effective mass and impulses for ball, hinge, slider and distance joints."
sources: ["https://box2d.org/files/ErinCatto_SequentialImpulses_GDC2006.pdf", "https://www.cs.cmu.edu/~baraff/sigcourse/notesf.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Joint types and constraint Jacobians

**Goal:** implement joints in a sequential-impulse solver by deriving each as a Jacobian row
(Erin Catto, *Fast and Simple Physics using Sequential Impulses*, GDC 2006).

## Recipe
1. Position constraint `C(x) = 0` (e.g. distance minus rest length).
2. Differentiate: `dC/dt = J * V = 0`, where `V = [v1, w1, v2, w2]`. `J` is the Jacobian row.
3. Effective mass: `m_eff = 1 / (J * M^-1 * J^T)`.
4. Impulse: `lambda = -m_eff * (J*V + b)`, with bias `b = beta/dt * C` (Baumgarte) or soft terms.
5. Apply: `V += M^-1 * J^T * lambda`; accumulate and clamp for inequality constraints.

## Common joints
- **Distance (rod):** `C = |p2 - p1| - L`, `n = (p2-p1)/|p2-p1|`,
  `J = [-n, -(r1 x n), n, (r2 x n)]`.
- **Ball-socket (point):** three rows, `C = p2 - p1` (vector); solve as a 3x3 block:
  `K = (1/m1 + 1/m2) I - [r1]x I1^-1 [r1]x - [r2]x I2^-1 [r2]x`, `impulse = -K^-1 * (vrel + bias)`.
- **Hinge (revolute, 3D):** point constraint + two angular rows keeping hinge axes aligned
  (`C = a1 . b2`, `a1 . c2` for perpendiculars b2, c2 of the axis on body 2).
- **Slider (prismatic):** two linear rows perpendicular to the axis + three angular rows (lock rotation).
- **Weld:** point + three angular rows.

## Solver notes
- Precompute `J`, `m_eff` and bias in a prepare step; iterate velocity rows 4-10 times.
- Warm start with last frame's accumulated lambda.
- Solve block constraints (3x3) directly for faster convergence than three scalar rows.

## Verify
- Pendulum on a distance joint: length error stays small at 60 Hz, 8 iterations (a 1 m pendulum released horizontally with
  Baumgarte beta 0.2 and no slop measured a 1.3% peak error, so a 1% budget needs warm starting, soft constraints or
  substeps).
- Numerically check `J` against finite differences of `C`. (Done here: the distance-joint row and the ball-socket
  `K = J M^-1 J^T` matched to 1e-16.)

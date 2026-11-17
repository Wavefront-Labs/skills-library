---
id: engineering-technology.aerospace-engineering.orbital-mechanics.lambert-problem-solver
name: lambert-problem-solver
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [orbital-mechanics, orbit-transfers, transfers, lambert, universal-variables, targeting, transfer-time, izzo]
level: advanced
status: draft
description: "Solve Lambert's problem for transfer velocities between two position vectors in a given time with universal variables, covering short and long way and multi-revolution cases."
sources:
  - "Battin, An Introduction to the Mathematics and Methods of Astrodynamics"
  - "Izzo, Revisiting Lambert's problem (Celestial Mechanics and Dynamical Astronomy 2015)"
  - "Curtis, Orbital Mechanics for Engineering Students"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Lambert problem solver

**Goal:** the velocity vectors `v1`, `v2` of the conic connecting `r1` and `r2` in time `t`.

## Procedure
1. Compute the transfer angle `Delta nu` from `r1`, `r2` and the direction (prograde or retrograde; short way if `Delta nu < pi`).
2. Solve with a universal-variable (Stumpff) iteration or Izzo's algorithm; the unknown is a single variable (for example `z` or `x`) such that the time of flight matches `t`.
3. Recover `v1` and `v2` from the Lagrange coefficients (`f, g, g_dot`).
4. Multi-revolution: for `N` complete revolutions there are up to two solutions (high and low energy); Izzo's solver handles these.
5. Departure and arrival delta-v: subtract the body velocities at the endpoints.

## Practice
- Use Lambert over a grid of departure and arrival dates for porkchop plots.
- Use for interception, rendezvous targeting, and orbit determination from two positions.

## Gotchas
- 180-degree transfers are singular (the orbital plane is undefined): perturb the geometry or pick the plane.
- Convergence failures near parabolic transfer; use robust solvers.

## Verify
- [ ] Propagating `r1, v1` for time `t` returns `r2` to numerical tolerance.

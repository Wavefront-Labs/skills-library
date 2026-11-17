---
id: computing-software.game-programming.game-physics.implicit-integration-for-stiff-springs
name: implicit-integration-for-stiff-springs
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, implicit-euler, stiff-springs, cloth, game-programming]
level: practitioner
status: verified
description: "Integrate stiff springs and cloth with implicit (backward) Euler: linearised system, conjugate gradient solve, artificial damping and cost trade-offs."
sources: ["https://www.cs.cmu.edu/~baraff/papers/sig98.pdf", "https://www.cs.cmu.edu/~baraff/sigcourse/notesd2.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Implicit integration for stiff springs

**Goal:** keep very stiff springs (cloth stretch, hair, suspension) stable at game timesteps,
following Baraff and Witkin, *Large Steps in Cloth Simulation* (SIGGRAPH 98).

## Backward Euler
Evaluate forces at the *end* of the step:
`v1 = v0 + dt * M^-1 * f(x0 + dt*v1, v1)`. Linearise with the force Jacobians
`K = df/dx`, `D = df/dv`:
```text
(M - dt*D - dt^2*K) * dv = dt * ( f0 + dt*K*v0 )
v1 = v0 + dv ;  x1 = x0 + dt*v1
```
For a spring between i and j with rest length L, the stiffness block is
`K_ij = -k * ( (1 - L/l) * (I - n n^T) + n n^T )`, `n` the unit direction, `l` current length.

## Solving
- The system is sparse, symmetric (positive definite when you drop the indefinite compression
  term, i.e. the `(1 - L/l)` factor when `l < L`), so use **conjugate gradient**, warm started with last frame's dv.
  Baraff-Witkin use a modified CG that enforces constraints exactly, independent of the iteration count.
- A single spring on one body: solve the 1D version in closed form; no matrix needed:
  `v1 = (v0 - dt*(k/m)*x0) / (1 + dt*c/m + dt^2*k/m)`, `x1 = x0 + dt*v1` (identical to the 2x2 backward-Euler solve;
  checked numerically).

## Trade-offs
- Unconditionally stable but adds numerical damping: motion looks overdamped at large dt.
- Each step costs a linear solve; for real-time cloth today, XPBD or projective dynamics is
  usually cheaper with similar stability. Use implicit Euler when you need physically meaningful
  stiffness and damping.

## Middle ground
The 1D closed form above, applied per spring along its axis, is the cheap stable option for suspensions;
see `soft-constraints-and-stable-springs` for the frequency/damping-ratio form.

## Verify
- Stiffness of 1e6 N/m at 60 Hz on a 1 kg mass: implicit stays bounded, symplectic Euler explodes (measured). Symplectic
  Euler is stable only while `dt < 2*sqrt(m/k)`: at 1e6 N/m and 60 Hz that fails below about 69 kg (70 kg stayed stable, 60 kg blew up).
- Compare stretch percentage vs XPBD at equal cost.

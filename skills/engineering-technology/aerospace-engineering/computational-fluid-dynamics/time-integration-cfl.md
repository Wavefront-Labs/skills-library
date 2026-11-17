---
id: engineering-technology.aerospace-engineering.computational-fluid-dynamics.time-integration-cfl
name: time-integration-cfl
category: engineering-technology
field: aerospace-engineering
product: computational-fluid-dynamics
tags: [cfd, numerical-methods, discretisation, numerical-schemes, cfl-number, time-stepping, implicit-solver, dual-time-stepping, courant-number]
level: advanced
status: draft
description: "Choose time stepping and CFL: explicit stability limits, implicit CFL ramping, dual-time stepping for unsteady flows and how to pick the physical time step."
sources:
  - "Blazek, Computational Fluid Dynamics Principles and Applications"
  - "Ferziger and Peric, Computational Methods for Fluid Dynamics"
  - "Solver theory guides"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Time integration and CFL

**Goal:** stable and efficient steady and unsteady runs.

## Definitions
`CFL = (|u| + c) dt / dx` for compressible solvers, `|u| dt / dx` for incompressible.

## Practice
- **Explicit (Runge-Kutta):** stability limit CFL of order 1-3 depending on stages; local time stepping accelerates steady convergence.
- **Implicit:** CFL 10 to several hundred or more; ramp from a low start (for example 1-5) to the target over the first hundreds of iterations, and reduce if residuals blow up.
- **Unsteady (dual time stepping):** physical time step set by the physics: at least about 100 steps per shedding period or buffet cycle; inner iterations 20-50 per step until residuals drop 2-3 orders.
- Estimating the time scale: convective time `c/U`; shedding `St = f c / U` about 0.2 for bluff bodies.

## Gotchas
- A CFL ramp too fast crashes on shocks: begin with first-order and low CFL.
- Fixed physical dt that is too large smears the frequency of interest; check by halving.
- Local time stepping gives no physical transient: do not use it for unsteady simulations.

## Verify
- [ ] Steady run: residual drop and force convergence at final CFL.
- [ ] Unsteady run: halving dt changes the period and amplitude by less than the target tolerance.

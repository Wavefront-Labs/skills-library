---
id: engineering-technology.aerospace-engineering.ansys-fluent.fluent-pseudo-transient-method
name: fluent-pseudo-transient-method
category: engineering-technology
field: aerospace-engineering
product: ansys-fluent
tags: [fluent, ansys, fluent-solver, pseudo-transient, pseudo-time-stepping, time-scale-factor, steady-state-solution, convergence]
level: practitioner
status: draft
description: "Use pseudo-transient steady-state solving in Fluent, set the time-scale method, and understand the trade-off with explicit relaxation."
sources:
  - "Ansys Fluent user guide (pseudo transient under-relaxation)"
  - "Fluent theory guide"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Fluent: pseudo-transient method

**Goal:** robust convergence of steady problems through implicit under-relaxation based on a pseudo time step.

## Idea
Adds a pseudo time-derivative term to each equation, with a local pseudo time step derived from a length scale and velocity scale. Larger Courant number means a larger pseudo time step. The user controls the **Time Step Method** (Automatic or User Specified), **Length Scale Method** (Conservative or Aggressive), and **Time Scale Factor**.

## Settings
1. **Solution Methods > Pseudo Transient** on (enabled by default for the coupled scheme in many versions).
2. Time Step Method: Automatic with Conservative length scale for first runs; Aggressive speeds convergence if stable.
3. Time Scale Factor: raise above 1 to accelerate, lower below 1 to stabilise.
4. Under-relaxation factors for variables are the "implicit under-relaxation factors" (typically 0.5-1 for pseudo transient, density and body forces 1.0).

## Gotchas
- Physical unsteadiness: pseudo time stepping gives a steady solution, not a physical time history.
- A solution that continues to oscillate indicates an unsteady flow; switch to transient.

## Verify
- [ ] Residual decreases monotonically and force coefficients plateau.
- [ ] Changing the time scale factor gives the same converged forces.

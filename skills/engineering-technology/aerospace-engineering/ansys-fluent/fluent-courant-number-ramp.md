---
id: engineering-technology.aerospace-engineering.ansys-fluent.fluent-courant-number-ramp
name: fluent-courant-number-ramp
category: engineering-technology
field: aerospace-engineering
product: ansys-fluent
tags: [fluent, ansys, fluent-solver, courant-ramp, courant-number, cfl-ramp, solution-stability, tui-commands]
level: practitioner
status: draft
description: "Ramp the Fluent flow Courant number from a conservative value to the target for stable convergence on compressible external aerodynamics."
sources:
  - "Ansys Fluent user guide (solution controls, Courant number)"
  - "Fluent TUI reference"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Fluent: Courant number ramping

**Goal:** avoid divergence in the first iterations without wasting time later.

## Procedure
1. Initialise (see hybrid initialisation), first-order discretisation.
2. Set **Flow Courant Number** low (for example 1 to 5) for the first 50-100 iterations; this is in the Solution Controls panel, or by TUI `/solve/set/courant-number <value>`.
3. Increase stepwise (5, 20, 50, 100, up to 200) as residuals fall, keeping an eye on residual spikes and report definitions.
4. Switch to second-order after the first-order solution has settled.
5. For stubborn cases (strong shocks), drop the Courant number and the explicit relaxation of the momentum and pressure, or use the density-based solver with a CFL of 1 to 5 ramped to 50.

## Automation
Use a journal: set the Courant number, iterate, repeat:
```
/solve/set/courant-number 5
/solve/iterate 100
/solve/set/courant-number 50
/solve/iterate 200
```

## Gotchas
- A Courant number that is too high at start produces negative temperature or pressure errors.
- Residual spikes after raising the Courant number are normal for a few iterations; persistent growth is not.

## Verify
- [ ] Residuals and forces remain smooth through each ramp step.

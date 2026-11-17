---
id: engineering-technology.aerospace-engineering.ansys-fluent.pressure-based-vs-density-based-solver
name: pressure-based-vs-density-based-solver
category: engineering-technology
field: aerospace-engineering
product: ansys-fluent
tags: [density-based-solver, pressure-based-solver, solver-selection, compressible-flow, fluent]
level: practitioner
status: draft
description: "Choose between Fluent's pressure-based and density-based solvers for external aero and compressible flows, with the setup consequences of each choice."
sources:
  - "Ansys Fluent user guide (solver chapters)"
  - "Blazek, Computational Fluid Dynamics Principles and Applications"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Pressure-based vs density-based solver

**Goal:** pick the Fluent solver family that converges reliably for the Mach range at hand.

## Decision guide
- **Pressure-based (coupled)**: the usual first choice for subsonic and transonic external aerodynamics, incompressible and mildly compressible flow, and anything with multiphase, combustion or heavy physics models. Both segregated and coupled algorithms exist; the coupled one is the robust option for aero.
- **Density-based**: aimed at high-speed compressible flow with strong shocks (supersonic and hypersonic, strongly shocked internal flows). It offers implicit and explicit formulations and Roe-FDS or AUSM flux types.
- The old rule "pressure-based means low speed" is outdated: modern pressure-based coupled handles transonic wings well. Choose by robustness and physics, then compare on a coarse case.

## Procedure
1. Set the solver type in the General task (Solver Type), before initialising.
2. Pressure-based coupled: use pseudo-transient with a Courant-number ramp (see fluent-courant-number-ramp).
3. Density-based implicit: start with a low Courant number and raise it as residuals fall; first-order flux, then second order once stable.
4. Use the ideal-gas law with the energy equation on for both (see fluent-ideal-gas-energy-equation).
5. Boundary conditions differ in availability: pressure-far-field suits both; check the boundary list after switching solvers.

## Gotchas
- Default Courant numbers differ between solvers and versions; read the current defaults in your release rather than assuming.
- Switching the solver after setup can reset or hide boundary condition choices; recheck every zone.
- Compare lift and drag from both solvers on one mesh as a sanity check of the setup, not as validation.

## Verify
- [ ] Force coefficients agree between solvers within discretisation scatter on the same mesh.

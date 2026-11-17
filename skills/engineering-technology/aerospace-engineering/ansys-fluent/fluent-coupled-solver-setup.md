---
id: engineering-technology.aerospace-engineering.ansys-fluent.fluent-coupled-solver-setup
name: fluent-coupled-solver-setup
category: engineering-technology
field: aerospace-engineering
product: ansys-fluent
tags: [fluent, ansys, fluent-solver, coupled-solver, pressure-velocity-coupling, second-order-upwind, least-squares-gradient, flow-courant-number]
level: practitioner
status: draft
description: "Configure Fluent's pressure-based coupled solver for steady aerodynamics, with spatial discretisation, gradient and pseudo-transient options that converge reliably."
sources:
  - "Ansys Fluent user guide (solution methods and pressure-based coupled solver)"
  - "Fluent theory guide"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Fluent: coupled solver setup

**Goal:** a robust steady solution method.

## Steps
1. **Solution Methods > Scheme:** Coupled. For high Mach and shocks, consider the density-based solver instead (implicit, Roe-FDS or AUSM flux).
2. **Spatial Discretization:** Gradient = Least Squares Cell Based (or Green-Gauss node-based for tetrahedral meshes); Pressure = Second Order; Density, Momentum, Energy, Turbulence = Second Order Upwind (start First Order Upwind if the run is unstable).
3. **Pseudo Transient** option on for steady runs (see that skill); use the default under-relaxation factors, then adjust.
4. **Controls:** Flow Courant Number (default 200 for the pressure-based coupled solver) and explicit relaxation factors for momentum and pressure around 0.5-0.75 where pseudo transient is off.
5. **Monitors:** residuals plus drag, lift and moment report definitions with convergence criteria.

## Practice
- Start first-order for 100-200 iterations then switch to second-order.
- Reduce Courant number to 5-20 if the run diverges near shocks.

## Gotchas
- Switching order mid-run changes residual levels; plot forces too.
- Density-based solver needs ideal gas and typically a lower CFL ramp.

## Verify
- [ ] Forces flat over the last several hundred iterations at second order.

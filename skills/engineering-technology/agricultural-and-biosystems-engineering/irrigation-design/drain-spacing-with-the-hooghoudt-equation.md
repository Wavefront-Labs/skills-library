---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.drain-spacing-with-the-hooghoudt-equation
name: drain-spacing-with-the-hooghoudt-equation
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, hooghoudt, drain-spacing, subsurface-drainage, water-table-control, equivalent-depth, steady-state-drainage]
level: advanced
status: verified
description: "Compute subsurface drain spacing using the steady-state Hooghoudt equation with equivalent depth, soil hydraulic conductivity, drainage coefficient and water-table target."
sources:
  - "USDA NRCS National Engineering Handbook, Part 650 Engineering Field Handbook (https://www.nrcs.usda.gov)"
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Drain spacing with the Hooghoudt equation

**Goal:** a drain spacing that holds the mid-spacing water table at the target depth for the design drainage rate.

## Equation
For steady recharge q (drainage coefficient, in length per time) and drains on an impermeable layer with flow above and below drain level: L^2 = (8 x K2 x d x m + 4 x K1 x m^2) / q (the same as the Wikipedia form Q L^2 = 8 Kb d (Dd - Dw) + 4 Ka (Dd - Dw)^2, with m = Dd - Dw), where L is the spacing, m the height of the water table at mid-spacing above the drain level, K1 and K2 the hydraulic conductivity above and below drain depth, and d the Hooghoudt equivalent depth (accounts for convergence of flow near the drain; read it from Hooghoudt tables or the formulas in the drainage manual for the drain radius, the spacing and the depth to the barrier). Use consistent units.

## Procedure
1. Measure soil hydraulic conductivity by auger-hole method or similar in each layer; it varies by orders of magnitude, so sample widely.
2. Locate the impermeable layer (depth to barrier).
3. Choose drain depth and required drawdown (m) from crop root depth and the water table design.
4. Choose q (`drainage-coefficient-selection`).
5. Iterate L and d (d depends on L) until consistent.
6. Check the result against practical limits (machine depth, cost) and against the conditions in your region.

## Limits
Steady-state is a simplification; use a transient method for rainfall-driven systems if applicable (see the drainage manual). Spacing is very sensitive to K.

## Verify
- [ ] K measurements recorded with method and location.
- [ ] Observation wells at mid-spacing after installation.
- The equivalent depth d is not tabulated here; use the closed form or tables in the drainage manual.

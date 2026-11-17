---
id: engineering-technology.aerospace-engineering.propulsion-engineering.ideal-rocket-nozzle-performance
name: ideal-rocket-nozzle-performance
category: engineering-technology
field: aerospace-engineering
product: propulsion-engineering
tags: [ideal-nozzle, rocket-nozzle, thrust-coefficient, characteristic-velocity, specific-impulse, rocket-performance]
level: practitioner
status: verified
description: "Compute ideal rocket nozzle exit velocity, thrust coefficient, characteristic velocity and specific impulse, and judge over- and under-expansion."
sources:
  - "Sutton and Biblarz, Rocket Propulsion Elements"
  - "Hill and Peterson, Mechanics and Thermodynamics of Propulsion"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Ideal nozzle performance

**Goal:** thrust and specific impulse from chamber conditions and nozzle area ratio, for an ideal (isentropic, perfect-gas, 1D) nozzle.

## Relations
- Exit velocity: `Ve = sqrt( (2 g/(g-1)) R Tc [1 - (pe/pc)^((g-1)/g)] )`.
- Thrust: `F = mdot Ve + (pe - pa) Ae`.
- Characteristic velocity `c* = pc At / mdot`, determined by chamber conditions only.
- Thrust coefficient `CF = F / (pc At)`; `Isp = F / (mdot g0) = CF c* / g0`.
- The expansion ratio `Ae/At` fixes `pe/pc` through the area-Mach relation (see quasi-1d-area-mach-relation).

## Expansion
- Optimum when `pe = pa`. Over-expanded (`pe < pa`) risks flow separation inside the nozzle at large overexpansion; under-expanded (`pe > pa`) wastes potential.
- Vacuum `CF` rises with area ratio with diminishing returns while nozzle mass and length grow.

## Procedure
1. Get `pc`, `Tc`, `g`, molecular mass `M` (so `R = Ru/M`) from combustion equilibrium software or the engine data sheet.
2. Choose `Ae/At` from altitude profile and mass budget.
3. Compute `CF`, `c*` and `Isp`; apply real-engine efficiency factors (combustion, nozzle divergence, boundary layer) from data, typically a few percent in total (gated: unconfirmed, source is paywalled or blocked).

## Gotchas
- Frozen vs equilibrium flow gives different `Isp`; state which.
- Nozzle half-angle loss for conical nozzles is a divergence correction, about 1.7 percent for a 15 degree half-angle, from `lambda = (1 + cos(alpha))/2 = 0.983` (computed).
- Altitude-compensating nozzles trade complexity for sea-level to vacuum performance.

## Verify
- [ ] (Checked numerically for gamma 1.2, pc/pe = 100: the closed-form `CF` equals `F/(pc At)` and `CF c*/g0` equals `F/(mdot g0)`.) At `pe = pa`, `CF` from the formula matches `F/(pc At)` computed by the thrust equation.

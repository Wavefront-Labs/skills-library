---
id: engineering-technology.aerospace-engineering.orbital-mechanics.sutton-graves-stagnation-heating
name: sutton-graves-stagnation-heating
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [sutton-graves, stagnation-point-heating, convective-heating, entry-heating, heat-load, atmospheric-entry]
level: practitioner
status: gated
description: "Estimate convective stagnation-point heat flux with the Sutton-Graves correlation, integrate heat load along a trajectory, and know its limits."
sources:
  - "Sutton and Graves, NASA TR R-376 (general stagnation-point convective heating)"
  - "Anderson, Hypersonic and High Temperature Gas Dynamics"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Sutton-Graves heating

**Goal:** a quick estimate of peak heat flux and total heat load for an entry body.

## Correlation
`q_s = k * sqrt(rho / R_n) * V^3` (SI units: `rho` in kg/m^3, `R_n` effective nose radius in m, `V` in m/s, `q_s` in W/m^2), with `k` about `1.7415e-4` for Earth air (gated: unconfirmed, source is paywalled or blocked). NASA TR R-376 (Sutton and Graves 1971) derives a general equation for arbitrary gas mixtures, enthalpies 2.3 to 116.2 MJ/kg, 0.001 to 100 atm; the Earth-air constant is a commonly quoted reduction of it. The constant depends on the atmosphere; Mars and other gases have their own values.

## Example
`V = 7500 m/s`, `rho = 1e-4 kg/m^3`, `R_n = 1 m` gives `q_s` about 7.3e5 W/m^2 (73 W/cm^2; recomputed 7.35e5).

## Procedure
1. Get the trajectory `V(t)`, `rho(t)` from entry simulation (see ballistic-coefficient-and-entry-trajectory).
2. Choose the nose radius (larger radius lowers convective flux, a reason for blunt capsules).
3. Compute `q_s(t)`; the peak is typically near the point of high density-velocity product.
4. Heat load `Q = integral(q_s dt)`; size the thermal protection from `Q` and the peak flux.
5. Add radiative heating for high-speed entry (above roughly 10 km/s for Earth (gated: unconfirmed, source is paywalled or blocked)) with a separate correlation.
6. Convert to wall heat flux with a cold-wall to hot-wall correction as needed.

## Gotchas
- This is a stagnation-point correlation; off-stagnation heating, transition to turbulence, and surface catalysis need CFD or other correlations.
- The correlation assumes a cold wall; a hot ablating wall reduces the net flux.
- Do not use for non-blunt bodies, sharp leading edges (heating scales differently).

## Verify
- [ ] The estimate is within the scatter expected of a stagnation correlation (tens of percent) of a CFD or flight data point.

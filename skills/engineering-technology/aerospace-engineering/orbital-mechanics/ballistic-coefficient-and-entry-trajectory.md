---
id: engineering-technology.aerospace-engineering.orbital-mechanics.ballistic-coefficient-and-entry-trajectory
name: ballistic-coefficient-and-entry-trajectory
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [orbital-mechanics, atmospheric-entry, re-entry, ballistic-coefficient, entry-deceleration, allen-eggers, exponential-atmosphere, capsule]
level: practitioner
status: verified
description: "Compute ballistic coefficient and ballistic entry deceleration and peak heating altitude for capsule-class vehicles using the exponential atmosphere."
sources:
  - "Regan and Anandakrishnan, Dynamics of Atmospheric Re-Entry"
  - "Vinh, Busemann and Culp, Hypersonic and Planetary Entry Flight Mechanics"
  - "Wertz and Larson, SMAD"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Ballistic coefficient and entry trajectory

**Goal:** first-order peak deceleration and the altitude where it occurs.

## Definitions
- Ballistic coefficient `beta = m/(C_D A)` (kg/m^2); high `beta` penetrates deeper before decelerating.
- Exponential atmosphere: `rho = rho0 exp(-h/H)`, with scale height `H = R T / g` (isothermal atmosphere), which is 8.4 km at 288 K and 6.3 km at 217 K (computed), so about 6.3 to 8.4 km through the lower atmosphere; the right value depends on the altitude range of the peak deceleration.

## Allen-Eggers results (ballistic, steep entry, constant flight path angle `gamma`)
- Velocity: `V = V_e exp( - rho H /(2 beta sin(gamma)) )`.
- Peak deceleration: `a_max = V_e^2 sin(gamma) /(2 e H)` (independent of `beta`), occurring at velocity `V_e/sqrt(e)` (about 0.61 `V_e`).
- Altitude of peak deceleration depends on `beta`: `rho_peak = beta sin(gamma)/H`.

## Example
Earth entry at about 7.8 km/s (LEO return) and `gamma = 5` degrees gives 13.3 g for a purely ballistic profile (H = 7.5 km; computed 13.26 g, at V = 0.607 V_e = 4.73 km/s). A numerical integration of dV/dt = -rho V^2/(2 beta) with the exponential atmosphere gave 13.26 g for beta = 100, 300 and 1000 kg/m^2, confirming independence of beta. Lifting entry reduces it.

## Use
1. Choose `beta` and entry angle; compute peak g and heating location.
2. Check against crew or equipment limits.
3. Refine with 3-DOF numerical integration and a real atmosphere model.

## Gotchas
- The Allen-Eggers solution assumes constant `gamma` and exponential density: valid for steep entries.
- Shallow entries skip out or take long; the entry corridor limits angles.

## Verify
- [ ] Peak g from the formula and a numerical integration agree within about 15%.

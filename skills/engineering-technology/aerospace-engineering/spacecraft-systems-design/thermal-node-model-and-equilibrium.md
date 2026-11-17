---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.thermal-node-model-and-equilibrium
name: thermal-node-model-and-equilibrium
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [spacecraft, thermal-control, spacecraft-thermal, thermal-node-model, equilibrium-temperature, radiator-sizing, absorptivity-emissivity, lumped-parameter]
level: practitioner
status: gated
description: "Build a first spacecraft thermal model: equilibrium temperature from absorbed solar, albedo, Earth IR and internal power, and a lumped-node transient with radiator sizing."
sources:
  - "Gilmore, Spacecraft Thermal Control Handbook"
  - "Wertz and Larson, Space Mission Analysis and Design"
  - "Fortescue et al., Spacecraft Systems Engineering"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Thermal node model and equilibrium

**Goal:** hot and cold case temperatures for early design.

## Equilibrium
`alpha A_s S + alpha A_a S rho_alb F + epsilon A_e q_IR F + Q_int = epsilon sigma A_r T^4`
- Solar flux `S` about 1361 W/m^2 at 1 AU (varies about +3.4/-3.3% over the year from NASA perihelion 147.095 and aphelion 152.100 million km, computed); Earth IR about 237 W/m^2 average (range roughly 200-300 depending on location and season) (gated: unconfirmed, source is paywalled or blocked); albedo about 0.3 (NASA Earth fact sheet Bond albedo 0.294; the 0.25-0.35 range is unconfirmed (gated: unconfirmed, source is paywalled or blocked)).
- `alpha` absorptivity, `epsilon` emissivity, `A_s`, `A_a`, `A_e` projected areas to the Sun, albedo and Earth, `F` view factors, `A_r` radiating area, `Q_int` internal dissipation.
- Sphere in sunlight with `alpha/epsilon = 1`: `T = (S/(4 sigma))^(1/4)` about 278 K (278.3 K computed).

## Lumped transient
Per node `C_i dT_i/dt = Q_i - sum_j G_ij (T_i - T_j) - epsilon_i sigma A_i T_i^4 + ...`; solve with an ODE integrator; use conductive couplings `G_ij` for joints and radiative couplings for facing surfaces.

## Radiator sizing
`A_r = Q_reject / (epsilon sigma (T_r^4 - T_sink^4))` with margin for degradation of optical properties over life.

## Practice
1. Define hot and cold cases (beta angle, eclipse, power modes, end-of-life optical properties).
2. Size radiators for the hot case and heaters for the cold case; check temperature limits with margin.
3. Correlate the model against thermal-balance test data and update.

## Gotchas
- Optical properties degrade (UV, contamination); use beginning-of-life for cold and end-of-life for hot cases.
- Multi-layer insulation effective emittance in orbit is much lower than ground values.

## Verify
- [ ] Sphere check returns about 278 K; node energy balance closes to numerical tolerance.

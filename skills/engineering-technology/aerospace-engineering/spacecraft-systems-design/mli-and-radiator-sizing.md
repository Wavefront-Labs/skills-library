---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.mli-and-radiator-sizing
name: mli-and-radiator-sizing
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [mli, radiators, multilayer-insulation, radiator-sizing, optical-solar-reflector, thermal-control]
level: practitioner
status: verified
description: "Size multilayer insulation and radiators: effective emittance for heat leak, radiator area from heat rejection, and the effect of degradation."
sources:
  - "Gilmore, Spacecraft Thermal Control Handbook"
  - "Wertz and Larson, Space Mission Analysis and Design"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# MLI and radiators

**Goal:** limit heat leak where you want insulation, and reject heat where you need to.

## MLI
- Typical blankets stack aluminised polyimide or polyester layers separated by low-conductance spacers (netting), vented to space, with an outer layer chosen for optical properties.
- Heat leak `Q = A * sigma * eps_eff * (T_hot^4 - T_cold^4)`. Ideal laboratory `eps_eff` is of order 0.01 or less (gated: unconfirmed, source is paywalled or blocked); installed blankets with seams, closeouts, fasteners and penetrations are worse, so analysts commonly use values several times higher (for example 0.03 to 0.1 (gated: unconfirmed, source is paywalled or blocked)) unless they have test data.
- Ground bonded layers to avoid charging; vent for ascent depressurisation.

## Radiators
- Heat rejection `Q_rad = eps * sigma * A * (T^4 - T_sink^4) - alpha * A * q_absorbed` (solar, albedo, Earth infrared).
- Surfaces: optical solar reflectors (glass second-surface mirrors; low solar absorptance, high emittance), white paint (degrades under radiation and contamination), silvered or aluminised Teflon.
- Design for end-of-life absorptance, which is higher than beginning-of-life.

## Procedure
1. Compute the dissipated heat at hot and cold cases.
2. Choose radiator temperature and the sink environment (cold and hot cases, orbit and attitude).
3. Size `A` for the hot case with end-of-life optical properties.
4. Check the cold case heater power with beginning-of-life properties and MLI leak (see spacecraft-heaters-and-thermostats).
5. Verify in thermal model and in thermal vacuum test (see thermal-vacuum-testing).

## Gotchas
- MLI performance degrades when compressed or when edges and seams are poor; leak path dominated by edges.
- Radiators view other spacecraft surfaces; include view factors.

## Verify
- [ ] The thermal model hot and cold cases keep every unit inside its allowable range with the stated uncertainty margin.

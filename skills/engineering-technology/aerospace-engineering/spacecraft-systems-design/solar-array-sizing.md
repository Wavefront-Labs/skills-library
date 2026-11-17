---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.solar-array-sizing
name: solar-array-sizing
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [spacecraft, power-subsystem, eps, solar-array-sizing, solar-cells, beginning-of-life, end-of-life, degradation, sunlight-fraction]
level: practitioner
status: verified
description: "Size a spacecraft solar array from orbit-average power, eclipse fraction, path efficiencies, cell performance and life degradation using the standard SMAD relations."
sources:
  - "Wertz and Larson, Space Mission Analysis and Design"
  - "Larson and Wertz, power subsystem chapter"
  - "Patel, Spacecraft Power Systems"
  - "Kopp and Lean 2011, total solar irradiance 1360.8 W/m^2: https://link.springer.com/doi/10.1007/s11207-011-9867-6"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Solar array sizing

**Goal:** array area and beginning-of-life power for the end-of-life load.

## Method
1. **Required array power:** `P_sa = (P_e T_e / X_e + P_d T_d / X_d) / T_d` with `P_e, P_d` eclipse and daylight loads, `T_e, T_d` durations, and path efficiencies `X_e` (battery path) and `X_d` (direct path). SMAD gives typical values (gated: unconfirmed, source is paywalled or blocked): for a peak-power-tracking system `X_e = 0.65`, `X_d = 0.85`; for direct energy transfer `X_e = 0.60`, `X_d = 0.80`.
2. **Cell output:** `P_0 = eta_cell x S x ...` (for example a triple-junction cell at about 28-30% efficiency under 1361 W/m^2 AM0 (total solar irradiance 1360.8 W/m^2, Kopp and Lean 2011, SORCE TIM) gives 381-408 W/m^2 (computed), roughly 380-400 W/m^2 at cell level before packing, temperature and other losses).
3. **BOL power per area:** `P_BOL = P_0 I_d cos(theta)`, where `I_d` is inherent degradation (about 0.77-0.80 typical (gated: unconfirmed, source is paywalled or blocked)) from packing, mismatch, wiring and temperature, and `theta` the sun incidence angle.
4. **EOL:** `P_EOL = P_BOL (1 - D)^L` with annual degradation `D` and life `L` years; `D` depends on cell technology and radiation environment, so take it from cell data for the orbit.
5. Area `A = P_sa / P_EOL`.

## Practice
- Add margin (see margin philosophy skill) and check at worst beta angle and temperature, plus off-pointing during safe mode.
- Account for eclipse length from the orbit (see eclipse skill).

## Gotchas
- Cell temperature at hot case reduces efficiency.
- Array sizing must tie to battery sizing; do not size separately.

## Verify
- [ ] Recomputing the array output at EOL, worst-case geometry meets the load plus margin.

---
id: engineering-technology.chemical-engineering.heat-exchanger-design.boiling-heat-transfer-and-critical-heat-flux
name: boiling-heat-transfer-and-critical-heat-flux
category: engineering-technology
field: chemical-engineering
product: heat-exchanger-design
tags: [chemical-engineering, heat-exchanger-design, hx-condensers-reboilers, boiling-heat-transfer-and-critical-heat-flux, nucleate-boiling, critical-heat-flux, zuber, mostinski, pool-boiling, film-boiling, reboiler-heat-flux, boiling-curve]
level: advanced
status: gated
description: "Estimate nucleate boiling coefficients (Mostinski) and critical heat flux (Zuber), and set design heat flux limits for kettle and thermosiphon reboilers."
sources:
  - "Kern Process Heat Transfer, Perry Handbook heat transfer section, TEMA Standards, Heat Exchanger Design Handbook (HEDH), Kemp Pinch Analysis and Process Integration, Smith Chemical Process Design and Integration"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Boiling heat transfer and critical heat flux

**Goal:** a boiling-side coefficient and a heat-flux limit that avoids film boiling and fouling.

## Boiling regimes
Natural convection, nucleate boiling (efficient, coefficient rises with flux), transition and film boiling (very low coefficient, high wall temperature). The peak between nucleate and transition is the **critical heat flux** (CHF).

## Correlations (screening grade)
- **Mostinski (pool nucleate boiling; form and constants unconfirmed (gated: unconfirmed, source is paywalled or blocked))**: h = 0.00417 P_c^0.69 q^0.7 F_p, with h in W/m2/K, critical pressure P_c in kPa, heat flux q in W/m2, and F_p = 1.8 P_r^0.17 + 4 P_r^1.2 + 10 P_r^10 (reduced pressure P_r).
- **Zuber (pool CHF; Zuber 1959 UCLA thesis, OSTI 4175511; constant is pi/24 = 0.1309, and water at 1 atm gives about 1.1 MW/m2, computed)**: q_c = 0.131 lambda rho_v^0.5 [sigma g (rho_L - rho_v)]^0.25. Bundle effects lower the practical CHF; designers apply a bundle factor and operate well below the limit.

## Design practice
1. Compute the nucleate boiling coefficient at the design flux.
2. Set the design heat flux at no more than about 70% of the CHF (and use vendor or company limits: values of order 25 to 40 kW/m2 for typical organic services in thermosiphon reboilers, higher for water, are often quoted; confirm (gated: unconfirmed, source is paywalled or blocked)).
3. Check the wall temperature: T_wall = T_sat + q/h; limit to avoid thermal degradation or scaling.
4. For mixtures boiling over a range, the effective coefficient is lower than the ideal mixing prediction (mass-transfer resistance); apply a mixture correction.
5. If the flux exceeds the limit, increase area (lower flux), reduce steam pressure, or change type.

## Gotchas
- Heat-flux limits protect against vapour blanketing that causes instability and burnout.
- Steam at too high pressure makes the wall temperature excessive and the exchanger over-driven, a common cause of reboiler trouble.

## Verify
- [ ] q/q_c below 0.7 and wall temperature below the limit.
- [ ] Sensitivity to heating medium temperature checked.

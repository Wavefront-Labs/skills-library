---
id: engineering-technology.chemical-engineering.heat-exchanger-design.effectiveness-ntu-method
name: effectiveness-ntu-method
category: engineering-technology
field: chemical-engineering
product: heat-exchanger-design
tags: [chemical-engineering, heat-exchanger-design, hx-thermal-fundamentals, effectiveness-ntu-method, effectiveness-ntu, ntu-method, capacity-rate-ratio, exchanger-effectiveness, heat-exchanger-rating, outlet-temperature, cmin, performance-prediction]
level: practitioner
status: verified
description: "Rate an existing exchanger with the effectiveness-NTU method: capacity ratio, NTU, counterflow and other arrangements, outlet temperature prediction without iteration."
sources:
  - "Kern Process Heat Transfer, Perry Handbook heat transfer section, TEMA Standards, Heat Exchanger Design Handbook (HEDH), Kemp Pinch Analysis and Process Integration, Smith Chemical Process Design and Integration"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Effectiveness-NTU method

**Goal:** outlet temperatures and duty when area and U are known (rating), without iterating on LMTD.

## Definitions
- C = m c_p for each stream; C_min is the smaller, C_max the larger; C_r = C_min/C_max.
- NTU = U A / C_min.
- Effectiveness epsilon = Q/Q_max = Q/[C_min (T_h,in - T_c,in)].

## Relations (counterflow, parallel, C_r = 0 and the worked check recomputed in Python; one shell pass with 2 tube passes cross-checked against the LMTD-F relation in `lmtd-and-f-correction-factor`)
- **Counterflow**: epsilon = [1 - exp(-NTU(1 - C_r))]/[1 - C_r exp(-NTU(1 - C_r))]; for C_r = 1, epsilon = NTU/(1 + NTU).
- **Parallel flow**: epsilon = [1 - exp(-NTU(1 + C_r))]/(1 + C_r).
- **Phase change** on one side (C_r = 0): epsilon = 1 - exp(-NTU).
- **One shell pass, 2, 4, ... tube passes**: use the published relation involving sqrt(1 + C_r^2).

## Procedure
1. Compute C for each stream and C_r.
2. NTU from U A / C_min (U from the `overall-u-build-up` skill).
3. Get epsilon from the relation for the geometry.
4. Q = epsilon C_min (T_h,in - T_c,in); outlet temperatures from energy balances.
5. Compare with the measured plant outlets to detect fouling (the actual epsilon is lower than the clean prediction).

## Worked check
Counterflow, C_r = 0.5, NTU = 2: epsilon = (1 - exp(-1))/(1 - 0.5 exp(-1)) = 0.632/0.816 = 0.775.

## Gotchas
- NTU method requires U constant; for large property changes divide into zones.
- Effectiveness has a ceiling for given C_r (counterflow can reach 1 only for infinite area).

## Verify
- [ ] Energy balance both sides.
- [ ] Limits: NTU -> 0 gives epsilon -> 0; C_r = 0 gives 1 - exp(-NTU).

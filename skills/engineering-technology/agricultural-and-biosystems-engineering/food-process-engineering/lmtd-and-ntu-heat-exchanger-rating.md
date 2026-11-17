---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.lmtd-and-ntu-heat-exchanger-rating
name: lmtd-and-ntu-heat-exchanger-rating
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, lmtd, ntu, heat-exchanger-rating, effectiveness-ntu, overall-heat-transfer-coefficient, shell-and-tube, correction-factor, food-heat-transfer]
level: advanced
status: verified
description: "Rate or size a food-plant heat exchanger with LMTD and effectiveness-NTU: duty, overall U, correction factor, and when to prefer NTU."
sources:
  - "Singh & Heldman, Introduction to Food Engineering"
  - "Toledo, Fundamentals of Food Process Engineering"
  - "ASHRAE Handbook (Fundamentals and Refrigeration volumes) (https://www.ashrae.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LMTD and NTU heat exchanger rating

**Goal:** the area needed for a duty, or the outlet temperatures of an existing exchanger.

## LMTD method (outlet temperatures known)
- Duty Q = m x cp x dT on either stream (use the product cp at the mean temperature; check phase change).
- Q = U x A x F x LMTD, where LMTD = (dT1 - dT2) / ln(dT1/dT2) for the end temperature differences (counter-current), and F is the correction for multipass or cross-flow, read from charts or formulas (F = 1 for pure counter or parallel flow).
- If dT1 equals dT2, the LMTD is that value (avoid dividing by zero).
- Overall U: 1/U = 1/h_hot + R_wall + R_fouling + 1/h_cold (referenced to the same area). See `heat-exchanger-fouling-allowance-and-cleaning-cycles`.

## NTU method (outlet temperatures unknown)
Effectiveness e = Q / Qmax, Qmax = Cmin x (T_hot,in - T_cold,in); NTU = U x A / Cmin; Cr = Cmin/Cmax. Counter-current: e = (1 - exp(-NTU(1 - Cr))) / (1 - Cr x exp(-NTU(1 - Cr))), and for Cr = 1, e = NTU/(1+NTU). Use NTU when rating an existing exchanger at new flows.

## Check run
Counter-current example (Ch = 2, Cc = 3 kW/K, UA = 4 kW/K, 100 C and 20 C inlets): NTU = 2, e = 0.7398, Q = 118.37 kW from the effectiveness formula and UA x LMTD = 118.37 kW; the Cr = 1 limit e = NTU/(1+NTU) also reproduced (python, this session).

## Checks
- Temperature cross: F falling toward low values means the design is poor; add shells or use counter-current.
- Check pressure drop on both sides.
- For viscous products U is controlled by the product-side film.

## Verify
- [ ] Energy balance closes on both streams.
- [ ] Measured outlet temperatures versus predicted at commissioning.
- Unconfirmed: correlations for h depend on geometry; use the maker's data.

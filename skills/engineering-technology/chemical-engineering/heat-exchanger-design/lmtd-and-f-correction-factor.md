---
id: engineering-technology.chemical-engineering.heat-exchanger-design.lmtd-and-f-correction-factor
name: lmtd-and-f-correction-factor
category: engineering-technology
field: chemical-engineering
product: heat-exchanger-design
tags: [chemical-engineering, heat-exchanger-design, hx-thermal-fundamentals, lmtd-and-f-correction-factor, lmtd, f-correction-factor, log-mean-temperature-difference, temperature-cross, shell-passes, heat-exchanger-rating, bowman, counterflow]
level: practitioner
status: gated
description: "Compute LMTD and the F correction factor for shell-and-tube exchangers, check temperature cross and F limits, and decide when to add shell passes."
sources:
  - "Kern Process Heat Transfer, Perry Handbook heat transfer section, TEMA Standards, Heat Exchanger Design Handbook (HEDH), Kemp Pinch Analysis and Process Integration, Smith Chemical Process Design and Integration"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LMTD and F correction factor

**Goal:** the effective mean temperature difference for sizing: Q = U A F LMTD.

## Counterflow LMTD
LMTD = (DT1 - DT2)/ln(DT1/DT2) with DT1 = T_h,in - T_c,out and DT2 = T_h,out - T_c,in (counterflow arrangement). If DT1 = DT2 the LMTD equals that value. Parallel flow uses T_h,in - T_c,in and T_h,out - T_c,out.

## F factor
Define R = (T_h,in - T_h,out)/(T_c,out - T_c,in) and P = (T_c,out - T_c,in)/(T_h,in - T_c,in). For one shell pass and an even number of tube passes (Bowman, Mueller and Nagle, Trans ASME 62:283, 1940, Crossref 10.1115/1.4021450; the formula was cross-checked numerically against the 1-2 effectiveness relation):
F = [sqrt(R^2 + 1)/(R - 1)] ln[(1 - P)/(1 - P R)] / ln{ [2 - P(R + 1 - sqrt(R^2 + 1))] / [2 - P(R + 1 + sqrt(R^2 + 1))] }
(R = 1 uses the limiting form). F = 1 for pure counterflow and for condensing or boiling at constant temperature.

## Design rules
1. Aim for F at least about 0.75 to 0.8 (rule of thumb (gated: unconfirmed, source is paywalled or blocked)); below this the exchanger is inefficient and the slope of F against P is steep, so small errors cause big area errors.
2. A **temperature cross** (cold outlet hotter than hot outlet) is impossible with one shell pass (the F formula has no real solution, so F is zero or undefined); use two or more shells in series or a true-counterflow design.
3. To raise F: add shells in series (each shell uses its own P and R), use a plate exchanger (nearly countercurrent), or alter the temperatures.

## Procedure
1. Compute P and R from the process temperatures.
2. Compute F for the number of shells (use equal-size shell formulas, or read charts).
3. A = Q/(U F LMTD); iterate with the U build-up.
4. Check that no stream is phase-changing across a wide range without segmenting the calculation (use zone analysis).

## Gotchas
- LMTD assumes constant U and constant heat capacity; use zones if either varies strongly.
- Rating software computes F rigorously, but sanity-check by hand.

## Verify
- [ ] F above 0.75 or justified.
- [ ] Energy balance Q_hot = Q_cold within 1%.

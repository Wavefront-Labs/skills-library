---
id: engineering-technology.chemical-engineering.heat-exchanger-design.overall-u-build-up
name: overall-u-build-up
category: engineering-technology
field: chemical-engineering
product: heat-exchanger-design
tags: [chemical-engineering, heat-exchanger-design, hx-thermal-fundamentals, overall-u-build-up, overall-heat-transfer-coefficient, u-value, fouling-resistance, wall-resistance, film-coefficient, thermal-resistance-network, typical-u-values]
level: practitioner
status: verified
description: "Build up the overall heat transfer coefficient from film coefficients, fouling resistances and wall resistance, referencing the outside area."
sources:
  - "Kern Process Heat Transfer, Perry Handbook heat transfer section, TEMA Standards, Heat Exchanger Design Handbook (HEDH), Kemp Pinch Analysis and Process Integration, Smith Chemical Process Design and Integration"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Overall heat transfer coefficient build-up

**Goal:** U referred to the outside tube area from resistances in series.

## Equation
1/U_o = 1/h_o + R_fo + (d_o ln(d_o/d_i))/(2 k_w) + R_fi (d_o/d_i) + (1/h_i)(d_o/d_i)
with h film coefficients, R_f fouling resistances (m2 K/W), k_w wall conductivity, d_o and d_i tube diameters.

## Steps
1. Estimate h_i and h_o from correlations (see the film-coefficient skill).
2. Select fouling resistances: from the TEMA tables, client standards or experience; typical treated cooling water is of the order of 0.0002 to 0.0004 m2 K/W and clean light hydrocarbons about 0.0001 to 0.0002 (indicative only; confirm in the current TEMA text (gated: unconfirmed, source is paywalled or blocked)).
3. Wall resistance: carbon steel k about 45 W/m/K, stainless about 15 to 20 (typical handbook values (gated: unconfirmed, source is paywalled or blocked)), copper alloys higher; wall resistance is usually small unless the wall is stainless and thick.
4. Compute U_clean (no fouling) and U_dirty (with fouling).
5. Compare with typical ranges as a sanity check: water-to-water about 800 to 1,500 W/m2/K; organic-to-organic about 100 to 400; steam to water about 1,500 to 4,000; gas-to-gas about 10 to 50 (rough, depends on service (gated: unconfirmed, source is paywalled or blocked)).
6. Excess area = A_dirty/A_clean - 1 shows the margin built for fouling.

The series formula was sanity-checked numerically (h_o 1000, h_i 2000 W/m2/K, 25 x 21 mm tube, k_w 45, R_f 0.0002 both sides gives U_o = 480 W/m2/K).

## Practice
Identify the controlling resistance: if one film coefficient dominates (the low one), improving the other side is pointless.

## Gotchas
- Mixing areas (inside vs outside) in the resistance sum.
- Using fouling factors that are too large can mask poor design and cost area; too small causes early cleaning.

## Verify
- [ ] U within the expected range for the service.
- [ ] Controlling resistance identified and explained.

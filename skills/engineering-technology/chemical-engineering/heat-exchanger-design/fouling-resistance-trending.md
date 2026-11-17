---
id: engineering-technology.chemical-engineering.heat-exchanger-design.fouling-resistance-trending
name: fouling-resistance-trending
category: engineering-technology
field: chemical-engineering
product: heat-exchanger-design
tags: [chemical-engineering, heat-exchanger-design, hx-fouling-and-operations, fouling-resistance-trending, fouling-resistance, performance-monitoring, u-trend]
level: practitioner
status: draft
description: "Trend fouling resistance from plant data: compute U from measured duty and temperatures, then Rf = 1/U - 1/U_clean."
sources:
  - "Kern Process Heat Transfer, Heat Exchanger Design Handbook, TEMA Standards, Kemp Pinch Analysis and Process Integration"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fouling resistance trending

**Goal:** Trend fouling resistance from plant data: compute U from measured duty and temperatures, then Rf = 1/U - 1/U_clean.

## Steps
1. Collect inlet and outlet temperatures and flows for both streams, and compute the duty from each side to check the balance.
2. Compute LMTD (with the F correction) and U = Q / (A LMTD).
3. Fouling resistance Rf = 1/U_fouled - 1/U_clean, where U_clean is from the design or the post-cleaning data.
4. Trend over time and correct for flow changes since U depends on velocity; use normalised data.
5. Use the trend to schedule cleaning where cost of lost performance equals the cost of cleaning.

## Gotchas
- Instrument error is large when temperature approaches are small.
- Heat balance imbalance signals bad data.

## Verify
- [ ] Heat balance closes within a few percent.
- [ ] Trend is smoothed and flow-normalised.

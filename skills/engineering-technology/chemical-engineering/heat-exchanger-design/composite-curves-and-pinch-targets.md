---
id: engineering-technology.chemical-engineering.heat-exchanger-design.composite-curves-and-pinch-targets
name: composite-curves-and-pinch-targets
category: engineering-technology
field: chemical-engineering
product: heat-exchanger-design
tags: [chemical-engineering, heat-exchanger-design, hx-pinch-and-integration, composite-curves-and-pinch-targets, pinch-analysis, composite-curves, problem-table-algorithm, minimum-utility, pinch-temperature, delta-t-min, heat-integration, energy-targeting]
level: practitioner
status: verified
description: "Build hot and cold composite curves and the problem table to find minimum hot and cold utilities and the pinch temperatures for a chosen minimum approach."
sources:
  - "Kern Process Heat Transfer, Perry Handbook heat transfer section, TEMA Standards, Heat Exchanger Design Handbook (HEDH), Kemp Pinch Analysis and Process Integration, Smith Chemical Process Design and Integration"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Composite curves and pinch targets

**Goal:** the energy target (minimum hot and cold utility) and the pinch location before designing any network.

## Data extraction
For each process stream: supply temperature T_s, target temperature T_t, and heat capacity flowrate CP = m c_p (kW/K) (or enthalpy change, for phase-changing streams, with segmented linearisation). Hot streams need cooling, cold streams need heating.

## Composite curves
1. Shift temperatures: hot streams down by DT_min/2, cold streams up by DT_min/2 (or plot the curves with a DT_min gap).
2. Combine the heat loads of all hot streams in each temperature interval to make the hot composite curve (T versus cumulative H); do the same for cold streams.
3. Slide the cold curve horizontally until the closest approach equals DT_min: the **pinch** is at the closest approach. The overlap is the recoverable heat; the left over is the minimum cold utility, and the right over the minimum hot utility.

## Problem table algorithm (numerical equivalent)
1. List shifted temperature intervals; for each, net heat = (sum CP_hot - sum CP_cold) times interval width (a surplus if positive).
2. Cascade heat from the top assuming zero hot utility (cumulative sum of the net heats); the most negative cumulative value gives Q_H,min as its magnitude; reset the cascade by adding it at the top. (Sign convention checked by running the algorithm on a four-stream case: Q_H,min 7.5, Q_C,min 10, pinch at shifted 145, and Q_C,min - Q_H,min equals the net stream heat balance.)
3. The shifted temperature where the cascaded heat is zero is the pinch; the last value gives Q_C,min.

## Choosing DT_min
Typical process-to-process values are 10 to 20 K (gated: unconfirmed, source is paywalled or blocked); smaller for sub-ambient or high-value energy, larger for gases and fouling streams. Refine by cost trade-off (see the area-targeting skill).

## Gotchas
- Variable CP: split into linear segments.
- Streams with large heat-transfer coefficient differences need individual minimum approach contributions.

## Verify
- [ ] Energy balance: hot duty minus cold duty equals utility difference.
- [ ] The problem table pinch matches the composite curve pinch.

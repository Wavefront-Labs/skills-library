---
id: engineering-technology.chemical-engineering.heat-exchanger-design.pinch-design-method
name: pinch-design-method
category: engineering-technology
field: chemical-engineering
product: heat-exchanger-design
tags: [chemical-engineering, heat-exchanger-design, hx-pinch-and-integration, pinch-design-method, heat-exchanger-network, hen-synthesis, cp-inequality, stream-splitting, tick-off-rule, loops, minimum-units]
level: advanced
status: draft
description: "Design a heat exchanger network that achieves pinch targets: split at the pinch, CP rules for matches, stream splitting, tick-off heuristic and loop breaking."
sources:
  - "Kern Process Heat Transfer, Perry Handbook heat transfer section, TEMA Standards, Heat Exchanger Design Handbook (HEDH), Kemp Pinch Analysis and Process Integration, Smith Chemical Process Design and Integration"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pinch design method for networks

**Goal:** a network that meets the minimum-utility target with few units.

## Golden rules (from the pinch analysis)
1. Do not transfer heat across the pinch.
2. Do not use external cooling above the pinch.
3. Do not use external heating below the pinch.
Violating any of them increases utility use by the amount of violation.

## Design procedure
1. Divide the problem at the pinch: design **above** and **below** separately (start at the pinch and move away).
2. **Matches adjacent to the pinch**: above the pinch, each hot stream must be matched to a cold stream with CP_cold at least CP_hot at the pinch (cold stream has the larger or equal CP). Below the pinch, CP_hot at least CP_cold. Where the rule cannot be met, split a stream.
3. Number of streams at the pinch: above the pinch, the number of hot streams must be at most the number of cold streams (to be able to pair them), else split cold streams; the opposite below.
4. **Tick-off heuristic**: make each match as large as possible, to completely satisfy the smaller of the two stream duties (remove a stream from the problem).
5. After using up the pinch matches, complete the network away from the pinch with remaining matches and utilities.
6. Count units; the minimum number of units for each side is N_streams + N_utilities - 1 (no loops). Break **loops** (and utility paths) by shifting duty, accepting some utility violation if worthwhile.
7. Check DT_min for every match and adjust for area and cost.

## Practice
Use software (a pinch tool or HEN design in a simulator) to check; hand design is still essential for understanding.

## Gotchas
- A target-achieving network can have many small exchangers; trade energy versus capital.
- Practical constraints (distance, safety, operability, fouling) can forbid a match; the design must accept limits (forbidden matches).

## Verify
- [ ] Utility use equals the target (or the excess is explained).
- [ ] Every match meets the DT_min and the CP rules at the pinch.

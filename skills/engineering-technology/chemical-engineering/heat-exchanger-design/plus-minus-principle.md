---
id: engineering-technology.chemical-engineering.heat-exchanger-design.plus-minus-principle
name: plus-minus-principle
category: engineering-technology
field: chemical-engineering
product: heat-exchanger-design
tags: [chemical-engineering, heat-exchanger-design, hx-pinch-and-integration, plus-minus-principle, process-modification, pinch-analysis, energy-reduction, heat-integration, column-pressure-change, retrofit, targets]
level: advanced
status: verified
description: "Apply the plus-minus principle to find process changes that reduce energy: which stream or equipment changes above or below the pinch reduce utility targets."
sources:
  - "Kern Process Heat Transfer, Perry Handbook heat transfer section, TEMA Standards, Heat Exchanger Design Handbook (HEDH), Kemp Pinch Analysis and Process Integration, Smith Chemical Process Design and Integration"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Plus-minus principle for process changes

**Goal:** choose process modifications that reduce utility targets, using the composite curves.

## The rule
- Above the pinch, a change that **increases** hot-stream heat (net heat availability) or **decreases** cold-stream heat requirement reduces hot utility; decreasing hot-stream heat or increasing cold-stream heat increases hot utility. ("Plus" a hot stream or "minus" a cold stream above the pinch is beneficial.)
- Below the pinch, increasing cold-stream heat requirement or decreasing hot-stream heat available reduces cold utility. ("Minus" hot, "plus" cold, below.)
- Changes that straddle the pinch have partly opposite effects.

## Examples
- Lowering the temperature of a hot stream while it stays above the pinch does nothing, but shifting a hot stream from below to above the pinch (for example raising reflux temperature through pressure) adds heat above and reduces hot utility.
- Raising the operating pressure of a column so its condenser moves above the pinch can let it supply heat to cold streams.
- Reducing a reactor feed temperature to eliminate a hot duty above the pinch.

Direction check (computed with a problem table on a four-stream case, DT_min 10 K): raising the CP of a hot stream that has heat above the pinch cut Q_H,min from 7.5 to 2.5, and lowering the CP of a cold stream above the pinch cut it from 7.5 to 3.0, as the rule predicts. Original: Linnhoff and Hindmarsh, Chem. Eng. Sci. 38(5):745-763 (1983) (title Crossref-confirmed).

## Procedure
1. Establish the base targets and pinch.
2. List candidate changes: operating pressure, temperature, flow, reactor conversion, solvent loop temperatures.
3. For each, apply the principle to see if the target drops; quantify using the problem table with modified stream data.
4. Check feasibility with process constraints (azeotropes, catalyst limits, product specs); simulate.
5. Estimate savings versus modification cost.

## Gotchas
- Process changes alter flows and compositions elsewhere; always re-run the simulation.
- Retrofit costs (piping, structure) can reduce the benefit.

## Verify
- [ ] Revised targets from the modified data confirm the predicted trend.
- [ ] Economic comparison of the change versus the savings.

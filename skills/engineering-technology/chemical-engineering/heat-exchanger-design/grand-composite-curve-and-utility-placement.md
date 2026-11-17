---
id: engineering-technology.chemical-engineering.heat-exchanger-design.grand-composite-curve-and-utility-placement
name: grand-composite-curve-and-utility-placement
category: engineering-technology
field: chemical-engineering
product: heat-exchanger-design
tags: [chemical-engineering, heat-exchanger-design, hx-pinch-and-integration, grand-composite-curve-and-utility-placement, grand-composite-curve, gcc, utility-selection, multiple-utilities, steam-levels, heat-pump, cogeneration, appropriate-placement]
level: advanced
status: draft
description: "Use the grand composite curve to select utility levels, place steam and cooling water, find pockets for heat pumping and locate columns and cogeneration relative to the pinch."
sources:
  - "Kern Process Heat Transfer, Perry Handbook heat transfer section, TEMA Standards, Heat Exchanger Design Handbook (HEDH), Kemp Pinch Analysis and Process Integration, Smith Chemical Process Design and Integration"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Grand composite curve and utility placement

**Goal:** choose utility levels and loads that minimise cost, and see where equipment integrates well.

## Construct the GCC
Plot shifted temperature against the net heat flow from the cascaded problem table (the heat cascade). The curve touches the vertical axis at the pinch (zero net flow).

## Reading
- Above the pinch: net heat sink (needs hot utility); below: net heat source (needs cold utility).
- **Pockets**: regions where process-to-process exchange fills in; no utility is needed there.
- Utility levels appear as horizontal lines (shifted by DT_min/2): place a high-pressure steam level at the top end and a lower-pressure steam level lower, using the cheaper utility as much as possible without crossing the curve (the utility line must not cut the GCC).
- Similarly for cooling water, refrigeration and hot oil.

## Appropriate placement
- **Distillation columns**: a column fits when the overall column grand composite does not straddle the pinch: place it entirely above or below the pinch (reboiler above and condenser above, or both below) so the column does not violate the golden rules; if the condenser heat can be used as hot utility above the pinch, that is integration.
- **Heat engines (cogeneration)** run above the pinch; **heat pumps** across the pinch (pumping heat from below to above).
- **Evaporators** by similar rules.

## Procedure
1. Compute the GCC from the problem table.
2. Add candidate utility levels with their costs; choose the levels and loads for minimum cost, keeping each utility line within the curve.
3. Locate appropriate-placement candidates and test with a simulation.

## Gotchas
- Steam levels set by site headers, not by pure analysis; check availability and cost.
- Moving a column pressure changes its position relative to the pinch; this can be a useful process modification.

## Verify
- [ ] Utility loads sum to the problem table targets.
- [ ] No utility line crosses the GCC.

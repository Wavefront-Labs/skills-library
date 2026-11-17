---
id: engineering-technology.chemical-engineering.heat-exchanger-design.hen-area-targeting-and-cost-trade-off
name: hen-area-targeting-and-cost-trade-off
category: engineering-technology
field: chemical-engineering
product: heat-exchanger-design
tags: [chemical-engineering, heat-exchanger-design, hx-pinch-and-integration, hen-area-targeting-and-cost-trade-off, area-targeting, total-cost-targeting, delta-t-min-optimisation, bath-formula, network-cost, capital-energy-trade-off, supertargeting]
level: advanced
status: draft
description: "Target heat-exchanger-network area and total cost versus the minimum approach temperature, find the optimum DT_min and estimate network cost before design."
sources:
  - "Kern Process Heat Transfer, Perry Handbook heat transfer section, TEMA Standards, Heat Exchanger Design Handbook (HEDH), Kemp Pinch Analysis and Process Integration, Smith Chemical Process Design and Integration"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Area targeting and cost trade-off

**Goal:** choose DT_min from economics, before designing the network.

## Area target
For a network with vertical (counter-current) heat transfer between the composite curves in enthalpy intervals k, the minimum area is
A_min = sum over intervals k of [ (1/DT_LM,k) sum over streams i of (q_i,k / h_i) ]
(the Bath formula), with DT_LM,k the log mean difference between the hot and cold composite curves in interval k, q_i,k the duty of stream i in the interval and h_i its film coefficient (including fouling).

## Cost target
1. **Energy cost**: Q_H,min and Q_C,min at each DT_min times the utility costs.
2. **Area**: A_min from above; capital cost from a cost law, C = a + b A^c per exchanger (for example with exponent about 0.6 to 0.8), using the number of units N_min = N_streams + N_utilities - 1 (counting each side if needed).
3. **Total annual cost** = annualised capital + energy cost.

## Procedure
1. For DT_min from 5 to 40 K compute targets (energy, area, number of units).
2. Compute annualised capital with a capital charge factor (state it) and the total cost.
3. Plot total cost versus DT_min; find the minimum (typically broad and flat).
4. Choose DT_min at or slightly above the minimum (for robustness) and design the network (see `engineering-technology.chemical-engineering.heat-exchanger-design.pinch-design-method`).

## Gotchas
- Using a single film coefficient for all streams hides differences; use stream-specific values.
- Exotic materials or pressure raise the cost law parameters.
- Energy prices vary; test the optimum over a plausible range.

## Verify
- [ ] Cost curve plotted with the optimum DT_min and sensitivity to energy price.
- [ ] Targeted area compared with the designed network area (typically within 10 to 20%).

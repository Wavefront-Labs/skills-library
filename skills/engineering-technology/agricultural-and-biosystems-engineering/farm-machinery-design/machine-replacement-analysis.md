---
id: engineering-technology.agricultural-and-biosystems-engineering.farm-machinery-design.machine-replacement-analysis
name: machine-replacement-analysis
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: farm-machinery-design
tags: [agricultural-and-biosystems-engineering, farm-machinery-design, replacement-analysis, machinery-management, economic-life, marginal-cost, trade-in]
level: practitioner
status: draft
description: "Decide when to replace a tractor or implement by comparing average annual cost over its life with marginal cost, using ownership and repair-cost data."
sources:
  - "Hunt & Wilson, Farm Power and Machinery Management"
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Machine replacement analysis

**Goal:** find the economic life: the replacement age at which average annual total cost is lowest.

## Procedure
1. For each candidate age k, compute annual ownership cost (depreciation falls, interest falls) and annual repair cost (rises with hours) as in the ownership and repair-cost skills.
2. **Average annual cost** at age k = cumulative cost over k years (annualised at the farm's discount rate for rigour) / k.
3. **Marginal cost** at age k = cost of keeping the machine one more year (repair + interest on current value + depreciation of that year + any downtime cost).
4. Replace when marginal cost first exceeds the minimum average cost; the minimum is the economic life.
5. Add downtime cost: `lost timeliness + hired replacement` for critical machines like combines and planters. This usually shortens economic life.
6. Compare against trading in earlier versus keeping as a backup.

## Gotchas
- Using only repair cost against purchase price ignores reliability and technology gains (fuel efficiency, automation).
- Tax and finance terms can dominate; run the engineering view first, then add them.
- Low-use machines last far longer in years than in hours; set hours, not age, as the driver.

## Verify
- [ ] The cost curve shows an actual minimum within the horizon tested.
- [ ] Sensitivity to repair-cost coefficients and discount rate is shown.

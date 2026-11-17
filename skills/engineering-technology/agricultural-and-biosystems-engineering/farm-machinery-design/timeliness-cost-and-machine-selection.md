---
id: engineering-technology.agricultural-and-biosystems-engineering.farm-machinery-design.timeliness-cost-and-machine-selection
name: timeliness-cost-and-machine-selection
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: farm-machinery-design
tags: [agricultural-and-biosystems-engineering, farm-machinery-design, timeliness-cost, machinery-management, machine-selection, workable-days, planting-date-yield-loss, harvest-timeliness]
level: practitioner
status: draft
description: "Size a machine or fleet by balancing ownership and operating cost against the yield and quality loss from late operations; compute workable days and required capacity."
sources:
  - "Hunt & Wilson, Farm Power and Machinery Management"
  - "Srivastava, Goering, Rohrbach & Buckmaster, Engineering Principles of Agricultural Machines (ASABE)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Timeliness cost and machine selection

**Goal:** choose capacity so that the cost of lateness plus the cost of owning a bigger machine is minimised.

## Steps
1. **Required capacity**: `C_required (ha/h) = area (ha) / (workable days x hours per day)`. Workable days come from local weather and soil-trafficability records for the operation and window (use probability, e.g. days available in 8 of 10 years).
2. **Timeliness loss**: for each operation define a yield (or quality) loss per day of delay outside the optimum window, `K` in percent per day, from agronomic trials in your region. Cost per ha = `K/100 x yield x price x average delay (days)`.
3. **Total cost curve**: for candidate machine sizes (width or power) compute ownership cost + operating cost (fuel, labour, repairs) + timeliness cost per ha. The minimum is the economic size; the curve is usually flat near it, so favour the smaller or already-owned option inside 5 percent.
4. Check **field capacity** with a realistic field efficiency (see machinery-management skills) and **tractor power** for the implement (see tractor-implement matching).

## Gotchas
- Delay is not uniform: planting and harvest windows have asymmetric loss; do not use one K for the whole season.
- Crop mix spreads workload; model combined crops rather than one at a time.
- Custom hire or partnerships shift the cost curve; include them as options.

## Verify
- [ ] Capacity meets the area in the chosen probability of workable days.
- [ ] K values are sourced from local trial data and are named in the analysis.

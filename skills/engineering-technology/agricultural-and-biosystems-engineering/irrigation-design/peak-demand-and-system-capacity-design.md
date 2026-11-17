---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.peak-demand-and-system-capacity-design
name: peak-demand-and-system-capacity-design
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, peak-demand-design, crop-water-requirements, system-capacity, design-flow, peak-et, sets-per-day]
level: practitioner
status: gated
description: "Choose design peak ETc at a probability level, then convert to system flow, operating hours and area per set, with allowance for uniformity, leaching and downtime."
sources:
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
  - "Keller & Bliesner, Sprinkle and Trickle Irrigation"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Peak demand and system capacity design

**Goal:** a system that meets demand in a hot year, not an average one.

## Steps
1. **Design ETc**: use peak-period ETc (e.g. 10-day or monthly) at 75-90 percent probability from at least 20 years of weather (gated: unconfirmed, source is paywalled or blocked), with the crop's Kc at its peak stage (and partial canopy if applicable). Remember perennial or staggered plantings.
2. **Net requirement**: subtract any reliable water sources (shallow water table contribution, stored soil water).
3. **Gross**: `d_g = ETc / (E_a)` for sprinkler; for drip `d_g = ETc x Kr / (EU x (1 - LR))` (see drip skill).
4. **System capacity**: `Q (m3/h) = 10 x A (ha) x d_g (mm/day) / T (h/day)` (1 mm over 1 ha is 10 m3, computed). Choose T for operational realism: 18-22 h/day for automated systems (gated: unconfirmed, source is paywalled or blocked), less where labour or power restrictions apply.
5. **Downtime allowance**: add 5-10 percent (gated: unconfirmed, source is paywalled or blocked) for breakdowns, filter flushing, power cuts, or restrictions in the water right.
6. **Set arrangement**: divide area into zones/sets whose flow fits the pump or water supply, and time per set from application rate and depth.

## Gotchas
- A design based on average annual demand fails in heat waves.
- Water-right limits (flow rate, volume) may be the true constraint; check them first.
- Confirm the supply can deliver Q at pressure all season (well yield drops in drought).

## Verify
- [ ] Capacity versus peak ETc stated with the probability level and the downtime allowance.
- [ ] Check the water right and well yield cover Q for the season.

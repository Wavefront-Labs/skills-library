---
id: engineering-technology.agricultural-and-biosystems-engineering.farm-machinery-design.combine-throughput-and-capacity-matching
name: combine-throughput-and-capacity-matching
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: farm-machinery-design
tags: [agricultural-and-biosystems-engineering, farm-machinery-design, combine-throughput, combine-harvester, feed-rate, mog-ratio, harvest-capacity, grain-cart, loss-curve]
level: practitioner
status: draft
description: "Estimate combine capacity from feed rate and loss curve, convert to ha per hour, and match grain cart, trucks and drying capacity so the combine keeps running."
sources:
  - "Srivastava, Goering, Rohrbach & Buckmaster, Engineering Principles of Agricultural Machines (ASABE)"
  - "Hunt & Wilson, Farm Power and Machinery Management"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Combine throughput and capacity matching

**Goal:** operate the combine at its loss-limited capacity and avoid downstream bottlenecks.

## Capacity from the loss curve
Combine loss rises with material-other-than-grain (MOG) feed rate. Rated capacity is usually quoted at a defined loss level (often about 1 percent, per the maker's definition). Approximate:

- Feed rate (t/h) = `ground speed x header width x yield x (1 + MOG:grain ratio) / 10` in consistent units.
- Typical MOG to grain ratio near 1:1 for many crops; measure for your crop.
- Area capacity = `grain capacity (t/h) / yield (t/ha)`.

## Match logistics
1. Estimate grain flow = combine grain rate; cart and truck size and distance determine cycle time; add trucks until combine never waits.
2. Dryer and handling capacity must not be lower than harvest rate in wet seasons; plan staging space.
3. Unloading on the move versus stopped: unloading-on-the-go raises field efficiency by 5-15 percent.

## Gotchas
- Capacity falls in damp or lodged crops and on slopes.
- Headland and turning time reduce field efficiency (see field-efficiency skill).
- Machine ratings are not comparable between brands unless loss levels and crop definitions match.

## Verify
- [ ] Loss measured at planned speed in a trial strip.
- [ ] Combine idle time due to logistics is under about 10 percent in a day log.

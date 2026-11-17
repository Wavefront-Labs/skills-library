---
id: engineering-technology.agricultural-and-biosystems-engineering.farm-machinery-design.grain-drill-calibration
name: grain-drill-calibration
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: farm-machinery-design
tags: [agricultural-and-biosystems-engineering, farm-machinery-design, drill-calibration, seed-drill-calibration, planter-design, seed-rate, seeder-calibration, catch-test, grain-drill]
level: practitioner
status: verified
description: "Calibrate a grain drill or seeder for seed rate: stationary catch test, area from wheel revolutions, seed-size adjustments and a field check of seed use."
sources:
  - "Srivastava, Goering, Rohrbach & Buckmaster, Engineering Principles of Agricultural Machines (ASABE)"
  - "Hunt & Wilson, Farm Power and Machinery Management"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Grain drill calibration

**Goal:** apply the intended seed rate in kg/ha (or seeds/m2).

## Compute the target
`seeds/m2 = target plants/m2 / expected establishment %` (use local germination and field establishment). `kg/ha = seeds/m2 x thousand-seed-weight (g) / 100`.

## Stationary catch test
1. Fill hopper partway; set rate adjustment (gate or gearbox setting) to the manufacturer's chart value for the seed.
2. Jack up the ground drive wheel; collect seed from a known number of openers while turning the wheel a counted number of revolutions.
3. Area covered = `wheel circumference (m) x revolutions x working width of collected openers (m)`.
4. `rate = collected mass (kg) / area (ha)`; adjust setting and repeat until within the tolerance in the maker's manual (about 3 percent is common practice).
   Check (computed): 300 seeds/m2 at 40 g thousand-seed weight gives 300 x 40 / 100 = 120 kg/ha, since 10,000 m2 per ha x 0.04 g per seed / 1000 g per kg.

## Field check
Fill to a measured quantity, drill a measured area, weigh remaining seed. Compare with the target; slip of the drive wheel on soft ground reduces rate coverage.

## Gotchas
- Seed size and treatment change flow; recalibrate for each lot.
- Fluted feed and stepped gears have small flow differences by speed; check at working speed range.
- Distribution tubes blocked on one opener produce stripes.

## Verify
- [ ] All openers deliver within 5-10 percent of the average.
- [ ] Field seed use agrees with catch test.

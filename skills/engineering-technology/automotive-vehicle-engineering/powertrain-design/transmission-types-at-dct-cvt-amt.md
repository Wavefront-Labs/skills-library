---
id: engineering-technology.automotive-vehicle-engineering.powertrain-design.transmission-types-at-dct-cvt-amt
name: transmission-types-at-dct-cvt-amt
category: engineering-technology
field: automotive-vehicle-engineering
product: powertrain-design
tags: [transmission-types, automatic-transmission, dct, cvt, amt, torque-converter, planetary-gearset]
level: practitioner
status: draft
description: "Compare manual, torque-converter automatic, dual-clutch, CVT, AMT and EV single-speed transmissions on efficiency, shift quality, torque limits and cost."
sources:
  - "Naunheimer et al., Automotive Transmissions"
  - "Heisler, Advanced Vehicle Technology"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Compare AT, DCT, CVT, AMT

| Type | Strengths | Weaknesses |
|---|---|---|
| Manual (MT) | Efficient, cheap, direct feel | Driver effort, shift variability |
| Automatic (AT, planetary + torque converter) | Smooth launch, high torque capacity, many ratios available | More losses (hydraulic pump, converter), cost and mass; improved by lock-up and more gears |
| Dual-clutch (DCT, wet or dry) | Fast shifts, efficient | Low-speed launch/judder, heat in clutches, calibration effort |
| CVT (belt/chain) | Continuous ratio near best engine point, smooth | Torque capacity limit, belt friction losses, rubbery feel |
| AMT | Low cost | Torque interruption during shifts |
| EV single-speed | Simple, efficient | Limited ratio range; some designs use 2-speed for highway efficiency |

- Choose from application: torque level, vehicle class, cost, NVH, towing, packaging.
- Compare using a vehicle simulation on the same cycles (efficiency maps per gear, shift losses).
- Include hydraulic and clutch actuation power, and thermal limits.

**Gotchas:** quoted efficiency numbers depend strongly on test conditions; use consistent maps.

## Verify
- [ ] Simulation compares types on the same cycle and vehicle.
- [ ] Torque capacity margin to engine peak torque and rated life checked.

---
id: engineering-technology.agricultural-and-biosystems-engineering.farm-machinery-design.harvest-loss-measurement-and-monitors
name: harvest-loss-measurement-and-monitors
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: farm-machinery-design
tags: [agricultural-and-biosystems-engineering, farm-machinery-design, harvest-loss-measurement, combine-harvester, grain-loss, loss-monitor, catch-pan, header-loss, yield-loss]
level: practitioner
status: draft
description: "Measure combine losses with catch pans or frames, separate header, separator and shoe losses, convert counts to yield loss and calibrate loss monitors."
sources:
  - "Srivastava, Goering, Rohrbach & Buckmaster, Engineering Principles of Agricultural Machines (ASABE)"
  - "Hunt & Wilson, Farm Power and Machinery Management"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Harvest loss measurement and loss monitors

**Goal:** know where grain is lost and by how much, then fix the biggest source.

## Loss sources
- **Pre-harvest loss** (lodging, shatter, bird damage) is not machine loss; measure it ahead of the machine.
- **Header loss**: shatter and gathering loss at the cutterbar, reel or snapping rolls.
- **Separator loss**: grain in the straw/rotor discharge.
- **Cleaning shoe loss**: grain over the sieves.

## Procedure
1. Choose a representative area. Stop the machine with the header and threshing running; back up and measure.
2. Use a catch pan or frame of known area (for example 0.25 m2 or about 1 square foot) to collect kernels in the straw and chaff zones behind the machine. Count or weigh grain.
3. Header loss: count kernels on the ground in the cut width ahead of the machine's rear, minus pre-harvest losses.
4. Convert: `loss (kg/ha) = kernels per m2 x thousand-kernel weight (g) / 100`.
5. Compare with total yield: loss percent = loss / (yield + loss).

## Loss monitors
Piezo sensors on the shoe and separator detect kernel impacts and give relative readings; calibrate by comparing sensor reading with a measured catch-pan loss, then use it as a trend indicator, not an absolute.

## Gotchas
- Catch-pan counts are noisy; repeat at least three times.
- Scale check: for wheat at about 15,000 kernels per lb, one bushel per acre is roughly 20 kernels per square foot (about 200 per m2); compute the same way for your crop's kernel weight.
- Monitor calibration drifts with crop and moisture.

## Verify
- [ ] Source of losses identified (header, separator, shoe) and a change made, with a repeat measurement.

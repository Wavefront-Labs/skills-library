---
id: engineering-technology.agricultural-and-biosystems-engineering.farm-machinery-design.wheel-slip-measurement-and-traction-curve
name: wheel-slip-measurement-and-traction-curve
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: farm-machinery-design
tags: [agricultural-and-biosystems-engineering, farm-machinery-design, wheel-slip, tractor-performance, traction-slip-curve, slip-measurement, traction]
level: practitioner
status: draft
description: "Measure wheel slip with a marked-distance test, read the traction-slip curve, and select the operating slip range for efficient drawbar work."
sources:
  - "Srivastava, Goering, Rohrbach & Buckmaster, Engineering Principles of Agricultural Machines (ASABE)"
  - "Hunt & Wilson, Farm Power and Machinery Management"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Wheel slip and the traction-slip curve

**Goal:** operate where pull is high and slip losses are modest.

## Measure slip
1. Mark a tyre; with no load, drive a fixed number of wheel revolutions on the same surface and measure distance D0 (or use radar/GNSS speed).
2. Repeat under load: distance D1 for the same number of revolutions.
3. `slip (%) = (D0 - D1) / D0 x 100`.
With radar or GNSS speed: `slip = 1 - v_actual / v_theoretical`. Calibrate the tyre rolling radius first; a wrong radius gives wrong slip.

## Reading the curve
Net traction coefficient rises quickly with slip then flattens, while motion loss climbs; tractive efficiency peaks at modest slip. Extension and textbook guidance for tyred tractors puts the efficient range at roughly 8-15 percent depending on surface: lower on firm surfaces, higher on soft or tilled soil. Four-wheel-drive machines and tracks work at lower slip. Confirm with the manufacturer's recommendations and test data.

## Adjust
- Slip too high: add ballast, lower tyre pressure, reduce implement width or depth, change gear up, use duals or tracks.
- Slip too low: you are over-ballasted or under-loaded; reduce weight and save fuel.

## Gotchas
- Slip on one wheel of an axle with open differential is not the whole story; use diff lock only when needed.
- Slip is surface dependent: remeasure when moving between field conditions.

## Verify
- [ ] Slip measured by two methods agrees within 2 points.
- [ ] Fuel use per hectare drops or stays flat after the change.

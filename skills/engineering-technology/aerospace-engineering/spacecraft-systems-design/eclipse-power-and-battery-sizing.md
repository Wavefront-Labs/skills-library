---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.eclipse-power-and-battery-sizing
name: eclipse-power-and-battery-sizing
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [eclipse-power, battery-sizing, depth-of-discharge, eclipse-duration, power-subsystem, battery-cycle-life]
level: practitioner
status: verified
description: "Size a battery for eclipse load with depth-of-discharge limits for cycle life, and compute the array power needed to carry the load and recharge it."
sources:
  - "Wertz and Larson, Space Mission Analysis and Design"
  - "Fortescue et al., Spacecraft Systems Engineering"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Eclipse power budget

**Goal:** battery capacity and array power that carry the eclipse load and recharge in sunlight.

## Eclipse durations
- LEO: up to roughly 36 minutes out of a roughly 93-minute orbit at 400 km (computed: umbra half-angle 70.2 degrees, eclipse fraction 0.39) at low beta angle (see eclipse-duration-and-beta-angle); none at high beta for sun-synchronous dawn-dusk.
- GEO: eclipse seasons around the equinoxes, up to about 72 minutes per day at the equinox, with eclipses starting roughly 21-23 days before and ending as many days after it (about 40-46 days per season, depending on the source).

## Battery sizing
1. Eclipse energy `E_ecl = P_ecl * T_ecl` (average load times duration).
2. Battery capacity `C = E_ecl / (DoD * eta_discharge * N)` with `DoD` the depth of discharge and `N` the number of batteries or the transmission efficiency from battery to loads.
3. Choose `DoD` from cycle life. LEO has about 5700 cycles per year (computed, 400 km orbit); lithium-ion cells for LEO commonly run at shallow depth (roughly 20 to 40 percent for multi-year missions (gated: unconfirmed, source is paywalled or blocked)); GEO has few cycles (about 90 per year) and tolerates deeper discharge. Use cell cycle-life data at the planned temperature, not generic numbers.
4. Add margin for capacity fade at end of life, cell failure, and low temperature.

## Array sizing
`P_array = (P_ecl * T_ecl / X_e + P_day * T_day / X_d) / T_day` with `X_e`, `X_d` the efficiency of the path from array to loads via the battery (eclipse) or directly (day). SMAD-style values are in the range of roughly 0.6 to 0.65 for the battery path and 0.8 to 0.85 for the direct path (gated: unconfirmed, source is paywalled or blocked), depending on regulation architecture (see power-bus-architecture and solar-array-sizing).

## Gotchas
- Battery charge efficiency, not just discharge, affects recharge; allow for taper charge.
- Peak loads (transmitter, heaters) in eclipse can drive the sizing.
- Temperature controls capacity; the cold case reduces usable energy.

## Verify
- [ ] A time-domain orbit simulation holds the battery state of charge above the minimum at end of life in the worst eclipse.

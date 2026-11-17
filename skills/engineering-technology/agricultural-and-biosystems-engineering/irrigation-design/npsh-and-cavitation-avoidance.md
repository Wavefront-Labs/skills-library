---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.npsh-and-cavitation-avoidance
name: npsh-and-cavitation-avoidance
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, npsh, irrigation-pumping, pump-selection, cavitation, suction-lift, vapor-pressure, net-positive-suction-head]
level: practitioner
status: gated
description: "Calculate NPSH available for an irrigation pump (suction lift, vapour pressure, altitude, suction friction), compare with NPSH required, and fix cavitation risk."
sources:
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
  - "Keller & Bliesner, Sprinkle and Trickle Irrigation"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# NPSH and cavitation avoidance

**Goal:** no cavitation at any operating condition.

## Calculation
`NPSHa = (P_atm - P_vapour) / (rho g) - z_s - h_fs` in metres of water, with z_s the suction lift (negative if flooded suction) and h_fs friction and entrance losses in the suction line.
- Atmospheric head is about 10.3 m at sea level and drops roughly 1.2 m per 1000 m of elevation (computed from the standard atmosphere: 10.35 m at 101325 Pa and 998 kg/m3, 1.17 m lost by 1000 m).
- Vapour pressure head increases with temperature: about 0.24 m at 20 C and about 1.3 m at 50 C (computed with CoolProp: 2.34 kPa and 12.35 kPa saturation pressure).

## Rule
Require `NPSHa >= NPSHr + margin` where NPSHr comes from the pump curve at the highest flow expected, and the margin is commonly at least about 0.5-1 m or 10-20 percent (gated: unconfirmed, source is paywalled or blocked); follow the maker or Hydraulic Institute guidance.

## Fixes
- Lower the pump (reduce suction lift) or raise the water level.
- Larger suction pipe, fewer bends and valves, short line; use eccentric reducers with flat side up (gated: unconfirmed, source is paywalled or blocked).
- Cooler water; lower flow rate or lower speed.
- Choose a pump with lower NPSHr, or use a submersible/vertical turbine with the impeller below water.
- Foot valve and strainer sized to avoid choking.

## Signs of cavitation
Gravel-like noise, vibration, drop in head or flow, pitted impellers.

## Gotchas
- A clogged suction screen can cause cavitation unexpectedly.
- NPSHr increases with flow; calculate at the maximum.

## Verify
- [ ] NPSHa at the highest water temperature and lowest water level exceeds NPSHr plus margin.

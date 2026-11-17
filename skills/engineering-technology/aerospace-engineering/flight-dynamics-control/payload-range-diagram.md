---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.payload-range-diagram
name: payload-range-diagram
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [payload-range, range-diagram, ferry-range, mtow, mzfw, aircraft-performance]
level: practitioner
status: docs-checked
description: "Build a payload-range diagram from MZFW, MTOW, fuel capacity and Breguet range, and read the harmonic, economic and ferry range points."
sources:
  - "https://en.wikipedia.org/wiki/Range_(aeronautics)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Payload-range diagram

**Goal:** the trade between payload carried and distance flown, for a given aircraft.

## Weights
`MTOW` = maximum take-off weight; `MZFW` = maximum zero-fuel weight; `OEW` = operating empty weight; `MPL = MZFW - OEW`; tank capacity limits fuel.

## Corner points
1. **A, maximum payload**: take-off at `MTOW` with `MPL` and fuel `= MTOW - OEW - MPL` (this fuel mass must also fit in the tanks); range from Breguet with that fuel. Beyond A the horizontal line ends.
2. **B, maximum fuel**: tanks full, take-off still at `MTOW`, so payload is reduced to `MTOW - OEW - max fuel`. Between A and B, payload is traded for fuel at constant `MTOW`.
3. **C, ferry range**: tanks full, zero payload, take-off weight `OEW + max fuel`, below `MTOW`. Between B and C, payload falls and take-off weight falls with it.

## Range calculation
- Breguet (jet): `R = (V/c) * (L/D) * ln(W_start / W_end)`, with `c` the thrust-specific fuel consumption (see breguet-range-endurance).
- `W_start = take-off weight less climb fuel`, `W_end = W_start less cruise fuel`; hold reserves: add fixed-reserve fuel (diversion, hold) to the fuel needed so the stated range is design range with regulatory reserves. Reserve rules are set by the operating regulations of the region.

## Procedure
1. List weights and tank volume (use the density of the fuel in use).
2. Calculate range at A, B, C using a mission calculation with climb, cruise and descent.
3. Plot payload on the y axis versus range on the x axis.

## Gotchas
- Nominal and "typical" payload masses vary by operator seating.
- Range at B is limited by tank volume, not weight.
- Cruise `L/D` changes as weight falls; use step integration if the range is long.

## Verify
- [ ] Fuel plus payload plus `OEW` equals the weight limit at every corner.

## Checked
2026-11-01. The corner-point weight bookkeeping (A at MTOW with MPL, B at MTOW with full tanks, C at OEW plus full fuel) and the jet Breguet form were checked by derivation; no figures remain to look up. Removed: the fuel density figure. Regulatory reserve rules come from the operating regulations of the region.
Method: documentation only; no commands were run.

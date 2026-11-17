---
id: engineering-technology.aerospace-engineering.propulsion-engineering.compressor-map-and-surge-margin
name: compressor-map-and-surge-margin
category: engineering-technology
field: aerospace-engineering
product: propulsion-engineering
tags: [propulsion, turbomachinery, compressors, compressor-map, surge-margin, stall, corrected-flow, running-line]
level: practitioner
status: draft
description: "Read compressor maps (corrected flow, pressure ratio, efficiency islands), locate the surge line and running line, and calculate surge margin including stack-up."
sources:
  - "Cumpsty, Compressor Aerodynamics"
  - "Walsh and Fletcher, Gas Turbine Performance"
  - "Saravanamuttoo et al., Gas Turbine Theory"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Compressor map and surge margin

**Goal:** operating point and margin on a map.

## Reading the map
- Axes: corrected mass flow `W sqrt(theta)/delta` vs pressure ratio, with speed lines (corrected speed `N/sqrt(theta)`), efficiency islands, a surge/stall line on the left and choke on the right of each speed line.
- Running (operating) line: the locus of steady operating points set by the downstream turbine and nozzle (see off-design matching).

## Surge margin
`SM = (PR_surge/PR_operating - 1) x 100%`, evaluated at constant corrected flow (other definitions at constant speed exist; check the definition in use). Typical steady-state requirement is of the order 15-25% so that transient and degradation effects stay within the margin.

## Stack-up
Margin consumers: inlet distortion, engine deterioration, Reynolds number effect at altitude, tip-clearance, fuel acceleration transients (the acceleration line sits above the steady running line), bleed and power extraction, control tolerances. Use a root-sum-square or worst-case stack-up per company practice.

## Practice
1. Overlay the running line, acceleration line and surge line on the map.
2. Compute margins at critical points (idle acceleration, take-off power, altitude relight).
3. Place bleed valves and variable stators to hold margin at low speed.

## Gotchas
- Inlet distortion can cut surge margin by many points.
- Rotating stall may precede surge and degrade the engine without a violent surge.

## Verify
- [ ] Margin at each critical condition is computed with the same definition and shown on the map.

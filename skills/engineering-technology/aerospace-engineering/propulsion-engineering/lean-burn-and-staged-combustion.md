---
id: engineering-technology.aerospace-engineering.propulsion-engineering.lean-burn-and-staged-combustion
name: lean-burn-and-staged-combustion
category: engineering-technology
field: aerospace-engineering
product: propulsion-engineering
tags: [lean-burn, staged-combustion, low-nox, rql, taps, combustors-emissions]
level: practitioner
status: draft
description: "Compare staged, lean-premixed and rich-quench-lean combustion for low NOx, and know the instability, flashback and operability trade-offs for each."
sources:
  - "Lefebvre and Ballal, Gas Turbine Combustion"
  - "ICAO Annex 16 Volume II"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Staged and lean-burn concepts

**Goal:** lower NOx without raising CO, smoke or instability beyond limits.

## Why
NOx rises steeply with flame temperature. Burning leaner than stoichiometric lowers flame temperature, but too lean causes poor combustion efficiency, high CO and lean blowout.

## Concepts
- **Staged combustion**: a pilot stage for idle and low power and a main stage lit at high power (double-annular and twin-annular premixing swirler designs are examples). Fuel is split between stages by power setting.
- **Lean premixed pre-vaporised**: fuel and air mixed before the flame zone, avoiding hot stoichiometric pockets; risks include flashback, autoignition in the premixer and thermoacoustic instability.
- **Rich-quench-lean (RQL)**: a fuel-rich primary zone limits NOx and soot-sensitive formation conditions, rapid air quench, then lean burn-out; the critical design point is the quench mixing, which must be fast.

## Procedure for assessment
1. Collect ICAO landing and take-off cycle emissions data (NOx, CO, HC, smoke) for the candidate engines.
2. Map fuel staging versus power to see where NOx falls and where CO rises.
3. Check operability: ignition, relight, lean blowout margin, acoustic pressure fluctuations, pattern factor, altitude relight.
4. Include the effect on weight, cooling air and control complexity.

## Gotchas
- Combustion dynamics can force changes in the swirler design late in a programme.
- Low-power CO and HC often rise when NOx is cut at take-off.
- Regulatory limits for emissions are set by ICAO and national authorities; check the current limits (see icao-annex-16-engine-emissions).

## Verify
- [ ] Emissions at the four ICAO power points are within the applicable limit with stated margin.

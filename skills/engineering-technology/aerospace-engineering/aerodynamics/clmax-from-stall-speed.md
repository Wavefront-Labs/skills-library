---
id: engineering-technology.aerospace-engineering.aerodynamics.clmax-from-stall-speed
name: clmax-from-stall-speed
category: engineering-technology
field: aerospace-engineering
product: aerodynamics
tags: [aerodynamics, high-lift, clmax-sizing, stall-speed, wing-loading, approach-speed, vsr, certification-speeds]
level: practitioner
status: verified
description: "Work out the CLmax needed from stall and approach speed requirements and relate it to the certification speed definitions without misquoting them."
sources:
  - "14 CFR Part 25 sections 25.103 and 25.125"
  - "EASA CS-25 sections 25.103 and 25.125"
  - "Raymer, Aircraft Design"
  - "https://www.law.cornell.edu/cfr/text/14/25.103"
  - "https://www.law.cornell.edu/cfr/text/14/25.125"
  - "https://www.law.cornell.edu/cfr/text/14/25.107"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# CLmax sizing from stall speed

**Goal:** the high-lift capability a given wing loading and speed requirement demand.

## Basic relation
`V_s = sqrt( 2 W / (rho S CLmax) )`, so `CLmax = 2 (W/S) / (rho V_s^2)`. With sea-level density 1.225 kg/m3, 5000 N/m2 loading and a 55 m/s stall speed gives `CLmax` of about 2.7.

## Speed definitions (transport category)
- Stall speeds are defined in 25.103 (`V_SR`, reference stall speed, with the 1-g stall speed `V_S1g` as the related test quantity). In non-icing conditions `V_REF` may not be lower than 1.23 `V_SR0` (the reference stall speed in the landing configuration), nor than `V_MCL` or the speed giving the 25.143(h) manoeuvring capability (25.125(b)(2)(i)). `V_2MIN` may not be less than 1.13 `V_SR` for two- and three-engine propeller aircraft and for turbojets without a significant one-engine-inoperative stall-speed reduction, or 1.10 `V_MC` (25.107(b)); the other cases and `V_2` itself are in 25.107. Read the current regulation text for the exact conditions, because they change with amendments.

## Procedure
1. Choose landing weight and field requirement or approach speed.
2. Back out `CLmax_land` from `V_REF / 1.23 = V_SR0`.
3. Likewise for takeoff configuration from `V_2` requirement.
4. Compare with achievable `CLmax` for the flap system (see the flap skill) and iterate wing loading.

## Gotchas
- Stall speed is defined by regulation tests (1-g stall, specified deceleration rate), not by an arbitrary CLmax from a CFD run.
- Ice accretion and Reynolds effects reduce `CLmax`; certification stall speeds apply to the clean-wing tested conditions plus icing rules where applicable.
- This is conceptual-design guidance; the certification basis and the regulator's accepted means govern.

## Verify
- [ ] Margins quoted cite the regulation section and amendment used.
- [ ] Loading, density and speed units are consistent.

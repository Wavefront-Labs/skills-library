---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.water-hammer-and-surge-protection
name: water-hammer-and-surge-protection
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, water-hammer, surge-protection, joukowsky, wave-speed, pressure-surge, slow-closing-valve, surge-relief]
level: advanced
status: gated
description: "Estimate and control water hammer in irrigation pipelines: Joukowsky pressure rise, wave speed, closure time, surge sources and protective devices."
sources:
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Water hammer and surge protection

**Goal:** keep transient pressures within the pipe rating at pump trips, valve closure and fill.

## Basics
- Instantaneous velocity change dv causes a pressure rise dp = rho x a x dv (Joukowsky), where rho is density and a is the pressure wave speed, which depends on pipe material and wall thickness: it is highest for steel and lowest for plastics. Worked check (a = sqrt(K/rho / (1 + K D / (E e))), K = 2.2 GPa water, D = 100 mm): steel E = 200 GPa, e = 5 mm gives a about 1,340 m/s, so dp about 1.34 MPa (13 bar) per 1 m/s of velocity change; PVC E = 3 GPa, e = 5.5 mm gives about 390 m/s (modulus and wall values assumed for illustration; use supplier data). PVC and polyethylene have lower a, but pipes are also less strong.
- A valve closing slower than the critical time 2L/a (L is the length to the nearest reflection) produces a reduced rise; faster closure gives the full rise.
- Pump stop causes a drop, then column separation and a return surge, which can be worse than the initial drop.

## Sources on farms
Quick-closing hydrants and solenoid valves, pump start and stop, air trapped in lines, sudden check valve slam and filling a dry pipe quickly.

## Protection
- Slow-acting valves, valve actuators with set closing time, and soft-start or VFD ramps (`vfd-control-for-irrigation-pumps`).
- Surge relief and pressure relief valves, surge tanks, air chambers and air valves for vacuum (`air-release-and-pressure-regulating-valves`).
- Fill lines slowly (about 0.3 m/s is a commonly used filling velocity (gated: unconfirmed, source is paywalled or blocked)) with air release.
- For complex networks, run a transient model by a qualified engineer.

## Verify
- [ ] Surge pressure plus working pressure below pipe class.
- [ ] Field check with a pressure logger during a pump stop test.
- Unconfirmed: wave speed values; use the pipe supplier's modulus data.

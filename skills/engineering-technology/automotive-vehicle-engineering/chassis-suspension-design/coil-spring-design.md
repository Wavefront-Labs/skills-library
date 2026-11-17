---
id: engineering-technology.automotive-vehicle-engineering.chassis-suspension-design.coil-spring-design
name: coil-spring-design
category: engineering-technology
field: automotive-vehicle-engineering
product: chassis-suspension-design
tags: [coil-spring, helical-spring, spring-rate, wahl-factor, spring-stress, solid-height, shot-peening]
level: practitioner
status: verified
description: "Design a helical coil spring: rate and stress formulas with Wahl factor, geometry limits, progressive spring options, fatigue and corrosion protection."
sources:
  - "Shigley and Mischke, Mechanical Engineering Design (helical springs chapter)"
  - "Reimpell, Stoll and Betzler, The Automotive Chassis"
  - "https://www.engineeringtoolbox.com/modulus-rigidity-d_946.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Coil spring design

1. Rate: `k = G*d^4/(8*D^3*Na)` with G about 77-79 GPa for steel (engineeringtoolbox lists 77 for carbon steel, 79.3 for structural steel; use the supplier's value), wire diameter d, mean coil diameter D, active coils Na.
2. Stress: `tau = Kw*8*F*D/(pi*d^3)` with Wahl factor `Kw = (4C - 1)/(4C - 4) + 0.615/C`, spring index `C = D/d` (commonly 5-12; check the supplier's range).
3. Check at maximum load (full bump) against the permissible stress of the material/process (highly stressed suspension steel; ask the spring supplier for the design stress with shot-peening). Fatigue life from stress amplitude about static ride height over the road-load spectrum.
4. Geometry: free length, ride height length, solid height with clearance between coils at full jounce, seat design (ground ends, pigtail), buckling check for slender springs.
5. Progressive rate: variable pitch, variable wire diameter (tapered), or a bump stop engaged to avoid coil clash.
6. Side-load springs: bent axis or tilted springs to counter strut side loads.
7. Manufacturing: hot-wound, shot-peened, presetting (scragging), coated for corrosion; chip protection.
8. Test: load-deflection, fatigue to the specified cycles, corrosion fatigue.

**Gotchas:** weight saving by higher design stress raises sag and corrosion risk.

## Verify
- [ ] Calculated rate and rig measurement agree within the tolerance.
- [ ] Stress at full jounce below the supplier-approved limit.

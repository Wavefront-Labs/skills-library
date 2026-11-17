---
id: engineering-technology.automotive-vehicle-engineering.powertrain-design.bmep-torque-and-power-relations
name: bmep-torque-and-power-relations
category: engineering-technology
field: automotive-vehicle-engineering
product: powertrain-design
tags: [bmep, mean-effective-pressure, engine-torque, engine-power, displacement, specific-output, engine-fundamentals]
level: practitioner
status: gated
description: "Use BMEP to move between torque, power and displacement for 2- and 4-stroke engines, with typical ranges and what BMEP says about load."
sources:
  - "Heywood, Internal Combustion Engine Fundamentals"
  - "Pulkrabek, Engineering Fundamentals of the Internal Combustion Engine"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# BMEP, torque and power relations

- Definition: `bmep = 2*pi*nR*T/Vd` with T in N m, Vd in m^3, nR = 2 for four-stroke (rev per power stroke), 1 for two-stroke; result in Pa.
- Torque: `T = bmep*Vd/(4*pi)` (four-stroke). Example: 2.0 l (0.002 m^3) at 10 bar (1e6 Pa) gives `T = 1e6*0.002/12.566 = 159 N m`.
- Power: `P = T*omega = bmep*Vd*N/2` for four-stroke with N in rev/s (equivalently `P = bmep*Vd*n/120` with n in rpm; 2 l, 10 bar, 6000 rpm gives 100 kW both ways, computed).
- Typical maximum BMEP (Wikipedia mean-effective-pressure table, secondary source; check the engine at hand): passenger-car naturally aspirated petrol about 13 bar, turbocharged petrol about 22 bar, turbocharged diesel about 20 bar (truck turbodiesel about 24 bar).
- Specific output `kW/l` = `bmep*n/120`; raising either bmep or speed raises power; knock, boost and peak firing pressure limit the first, friction/valvetrain limits the second.
- BMEP also indicates relative load: with a friction mean effective pressure of 1 bar, a part-load BMEP of 3 bar means friction is 25% of the 4 bar of work before friction (1/(3+1)), and 2 bar means 33% (computed).

**Gotchas:** units; mixing indicated (imep) and brake (bmep) pressure.

## Verify
- [ ] Hand calc of torque from displacement and BMEP matches the dyno within a few percent.
- [ ] nR set correctly for the cycle.

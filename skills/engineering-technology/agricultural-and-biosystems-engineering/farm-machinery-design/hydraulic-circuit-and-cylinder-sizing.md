---
id: engineering-technology.agricultural-and-biosystems-engineering.farm-machinery-design.hydraulic-circuit-and-cylinder-sizing
name: hydraulic-circuit-and-cylinder-sizing
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: farm-machinery-design
tags: [agricultural-and-biosystems-engineering, farm-machinery-design, hydraulic-circuit-sizing, hydraulic-cylinder, pump-flow, tractor-hydraulics, pressure-drop, hose-sizing, machine-hydraulics]
level: advanced
status: verified
description: "Size an implement hydraulic circuit: cylinder bore and rod, flow for cycle time, hose velocity, pressure drop, relief setting and tractor remote compatibility."
sources:
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
  - "ISO standards catalogue (https://www.iso.org)"
  - "Srivastava, Goering, Rohrbach & Buckmaster, Engineering Principles of Agricultural Machines (ASABE)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hydraulic circuit and cylinder sizing

**Goal:** the required force and speed within the tractor's flow and pressure, without overheating.

## Steps
1. Force and stroke from the load case. F = p x A (bore area on push; bore minus rod area on pull). Add friction and a safety factor.
2. Choose working pressure within the tractor circuit rating; set relief below component ratings.
3. Flow for speed: Q = A x v. Check (computed): a 100 mm bore, 50 mm rod cylinder at 20 MPa pushes 157 kN and pulls 118 kN; at 0.2 m/s it needs 94 L/min to extend and 71 L/min to retract (the same flow retracts faster). Extend and retract speeds differ because of the rod.
4. Check the tractor's remote flow at working engine speed and the pump type (open-centre or closed-centre load-sensing); load-sensing needs a compatible implement circuit and load-sense line.
5. Hose sizing: use the hose maker's velocity guidance (lower in suction and return than in pressure lines). Long small-bore hoses cost pressure and make heat.
6. Thermal: lost pressure becomes heat; high-flow implements (fans, planters) may need a cooler and a case-drain connection.
7. Couplers: use the coupler standard the tractor uses (for example ISO flat-face), keep ratings consistent and bleed air.

## Safety
High-pressure fluid injection injuries are serious: never check leaks by hand. Mechanically lock rams before working under raised implements. Accumulators store energy.

## Verify
- [ ] Measured cycle time matches calculation at working engine speed.
- [ ] Oil temperature checked after a long run.
- [ ] Relief opens at the setting (gauge, approved procedure).
- Unconfirmed: specific velocities; use the hose maker's charts.

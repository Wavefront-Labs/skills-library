---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.irrigation-controller-programming-and-valve-sequencing
name: irrigation-controller-programming-and-valve-sequencing
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, controller-programming, valve-sequencing, irrigation-controller, solenoid-valve, station-run-time, stacking, irrigation-automation]
level: practitioner
status: gated
description: "Program an irrigation controller: station run times, start times, valve sequencing within pump capacity, stacking, rain delay, wiring limits and testing."
sources:
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
  - "Keller & Bliesner, Sprinkle and Trickle Irrigation"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Controller programming and valve sequencing

**Goal:** an automatic schedule that delivers the planned depth per zone without exceeding system capacity.

## Steps
1. Zone table: each valve with its flow (L/min), application rate (mm/h) and the required depth. Run time = required depth / application rate.
2. Concurrent valves: limit the sum of flows to pump and mainline capacity (`peak-demand-and-system-capacity-design`); sequence the valves, not run them together, if the flow exceeds capacity.
3. Start times and programs: group zones by crop or plant type; avoid overlapping programs that stack (queue) excess valves; some controllers allow stacking, which delays starts but can run past the intended window.
4. Seasonal adjust: percent scaling by ET or season; cycle and soak for slopes or low-intake soils.
5. Inputs: rain sensor, flow sensor (with high-flow shutdown for broken pipes), soil moisture override.
6. Valves and wiring: 24 VAC solenoids or DC latching (gated: unconfirmed, source is paywalled or blocked); check voltage drop on long runs against the valve's minimum; use proper wire size, splice connectors and surge protection. Pump start relay or master valve in the controller.
7. Fertigation or flushing sequences timed after the irrigation fill, with safe backflow protection.

## Test
Run every station manually, check pressure, leaks and coverage, then the program, and then record the programme.

## Verify
- [ ] Zone table and program printed and kept with the controller.
- [ ] Flow sensor alarm limit tested.
- Controller-specific menu terms and valve voltage limits: confirm in the controller and valve manuals (gated: unconfirmed, source is paywalled or blocked).

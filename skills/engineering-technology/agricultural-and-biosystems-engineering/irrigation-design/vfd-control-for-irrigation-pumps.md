---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.vfd-control-for-irrigation-pumps
name: vfd-control-for-irrigation-pumps
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, vfd-pumping, irrigation-pumping, pump-selection, variable-frequency-drive, constant-pressure-control, energy-saving]
level: practitioner
status: gated
description: "Apply variable frequency drives to irrigation pumping: when they save energy, constant-pressure control, minimum speed against static head, motor and cable limits and harmonics."
sources:
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
  - "Keller & Bliesner, Sprinkle and Trickle Irrigation"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# VFD control for irrigation pumps

**Goal:** hold pressure and cut energy where flow varies a lot.

## When it pays
VFDs save energy when the system curve is friction-dominated and flow varies (zones of different size, pivot start-up, variable demand). When static head is high, speed reduction cannot reduce flow below the speed at which the pump head equals static head, and savings are smaller.

## Design
1. Plot the pump curve at lower speeds using the affinity laws and the system curve; find the minimum speed that delivers the lowest zone at required pressure; keep above the cut-off speed.
2. Control: constant pressure at a transducer located at the far end or at the pump with friction compensation; PID tuning; set ramp times to avoid surges (see water hammer).
3. Motor: use inverter-duty motors or check the winding insulation; limit cable length or add filters; submersible pumps may need a sine or dV/dt filter and a minimum speed for cooling (gated: unconfirmed, source is paywalled or blocked); follow the motor and drive maker's data.
4. Harmonics and power quality: line reactors, compliance with the utility's rules.
5. Protect: dry-run, over-pressure, under-pressure, and minimum-flow protection.

## Gotchas
- Operating at very low speed overheats the motor in self-cooled designs.
- Energy savings must be verified; sizing the VFD to the pump's maximum power matters.
- Bypass contactor for failure operation.

## Verify
- [ ] Logged kWh per m3 before and after at comparable duty.

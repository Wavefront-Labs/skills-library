---
id: engineering-technology.chemical-engineering.process-control.compressor-and-pressure-control
name: compressor-and-pressure-control
category: engineering-technology
field: chemical-engineering
product: process-control
tags: [chemical-engineering, process-control, pc-unit-operation-control, compressor-and-pressure-control, pressure-control, compressor-control, capacity-control]
level: practitioner
status: draft
description: "Control gas pressure and compressors: suction or discharge pressure loops, capacity control, antisurge interaction and flare or letdown valves."
sources:
  - "Seborg Edgar Mellichamp and Doyle Process Dynamics and Control, Smith and Corripio, Luyben, Skogestad Multivariable Feedback Control, ISA-18.2"
  - "https://www.isa.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Compressor and pressure control

**Goal:** Control gas pressure and compressors: suction or discharge pressure loops, capacity control, antisurge interaction and flare or letdown valves.

## Steps
1. Select the controlled pressure (suction for upstream vessel pressure, discharge for the downstream demand).
2. Capacity control: speed variation for turbine and variable-speed drives, inlet guide vanes, suction throttling or recycle; compare the energy use.
3. Add antisurge control as a separate controller and ensure the capacity controller is aware of the antisurge action (decoupling or priority).
4. Use split-range to combine letdown and flare valves for the over-pressure control within the safe limits.
5. Tune pressure loops fast; they are normally gas capacitive processes with small time constants.

## Gotchas
- Interaction between antisurge and capacity control causes oscillation if not decoupled.
- Flare valve operation needs coordination with the relief design.

## Verify
- [ ] Control action avoids surge in all cases.
- [ ] Pressure variations stay within limits.

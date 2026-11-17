---
id: engineering-technology.chemical-engineering.process-control.reactor-temperature-control
name: reactor-temperature-control
category: engineering-technology
field: chemical-engineering
product: process-control
tags: [chemical-engineering, process-control, pc-unit-operation-control, reactor-temperature-control, reactor-temperature-control, cascade-jacket, runaway-protection]
level: practitioner
status: draft
description: "Design reactor temperature control: jacket cascade, feed temperature, coolant flow and runaway protection considerations."
sources:
  - "Seborg Edgar Mellichamp and Doyle Process Dynamics and Control, Smith and Corripio, Luyben, Skogestad Multivariable Feedback Control, ISA-18.2"
  - "https://www.isa.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reactor temperature control

**Goal:** Design reactor temperature control: jacket cascade, feed temperature, coolant flow and runaway protection considerations.

## Steps
1. For jacketed CSTRs use cascade: the reactor temperature controller sets the jacket temperature or coolant flow controller (fast inner loop).
2. Use split-range control for heating and cooling with a smooth switch.
3. For exothermic reactors check the open-loop stability (multiple steady states) and ensure the cooling capacity margin.
4. Control the feed rate and the temperature as additional handles; for semibatch, interlock the feed to the temperature.
5. Independent high-temperature alarms and safety trips are separate from the control loop.

## Gotchas
- Control tuning cannot rescue insufficient cooling.
- Test the cooling failure case.

## Verify
- [ ] Inner loop is faster than the outer by a good factor.
- [ ] Safety layers are independent of the control.

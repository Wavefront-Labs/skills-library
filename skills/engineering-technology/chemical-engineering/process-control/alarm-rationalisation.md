---
id: engineering-technology.chemical-engineering.process-control.alarm-rationalisation
name: alarm-rationalisation
category: engineering-technology
field: chemical-engineering
product: process-control
tags: [chemical-engineering, process-control, pc-alarms-and-interface, alarm-rationalisation, alarm-rationalisation, isa-18-2, alarm-management]
level: practitioner
status: gated
description: "Rationalise alarms following ISA-18.2 principles: purpose, consequence, response time, priority and documentation in the master alarm database."
sources:
  - "Seborg Edgar Mellichamp and Doyle Process Dynamics and Control, Smith and Corripio, Luyben, Skogestad Multivariable Feedback Control, ISA-18.2"
  - "https://www.isa.org"
  - "https://www.isa.org/products/ansi-isa-18-2-2016-management-of-alarm-systems-for"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alarm rationalisation

**Goal:** Rationalise alarms following ISA-18.2 principles: purpose, consequence, response time, priority and documentation in the master alarm database.

## Steps
1. Each alarm must require an operator action; if no action is needed, remove it or turn it into an event.
2. Document in the master alarm database: the cause, the consequence, the required response, the response time, the setpoint and the priority.
3. Assign priority from the consequence severity and the time available (a small number of priority levels, with the distribution target defined by the guideline in use).
4. Apply design: deadbands, delay timers, filtering and state-based suppression to avoid chattering.
5. Manage changes through a controlled process, and audit performance regularly. Confirm the current ISA-18.2 edition (ANSI/ISA-18.2-2016 at the time of review) and the company standards. The ISA-18.2 principles in steps 1 to 3 are quoted from memory (gated: unconfirmed, source is paywalled or blocked).

## Gotchas
- Do not duplicate trips as alarms without value.
- Priority tables vary between sites; use the site standard.

## Verify
- [ ] Every alarm has a documented response.
- [ ] Priority distribution has been checked.

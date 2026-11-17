---
id: engineering-technology.chemical-engineering.piping-instrumentation.control-loops-on-pid
name: control-loops-on-pid
category: engineering-technology
field: chemical-engineering
product: piping-instrumentation
tags: [chemical-engineering, piping-instrumentation, pi-pid-development, control-loops-on-pid, control-loops, interlocks, pid-instrumentation]
level: practitioner
status: draft
description: "Show control loops, interlocks and shutdown functions on a P&ID with the right symbols, tags and action descriptions."
sources:
  - "Crane Technical Paper 410, Perry Chemical Engineers Handbook, ASME B31.3, ISA-5.1, Darby Chemical Engineering Fluid Mechanics, Karassik Pump Handbook"
  - "https://www.isa.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Control loops on pid

**Goal:** Show control loops, interlocks and shutdown functions on a P&ID with the right symbols, tags and action descriptions.

## Steps
1. Draw the loop with the sensor, controller (function in DCS or field), and final element using the standard symbols and the shared display or field-mounted symbol.
2. Tag the loop with the same loop number, for example FT-101, FIC-101, FV-101.
3. Show the valve failure position (FC, FO, FL) and the action on air or power failure.
4. Show interlocks and trips with the interlock logic reference (cause-and-effect matrix), and keep the SIS devices clearly distinguished from the control.
5. Show alarm and trip setpoint tags where the company standard requires.

## Gotchas
- Do not share devices between the control and the safety function without review.
- Check consistency with the control narrative.

## Verify
- [ ] Every loop has a failure action.
- [ ] Cause and effect references match the P&ID.

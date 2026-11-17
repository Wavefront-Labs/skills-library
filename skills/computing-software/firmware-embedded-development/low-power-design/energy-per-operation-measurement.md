---
id: computing-software.firmware-embedded-development.low-power-design.energy-per-operation-measurement
name: energy-per-operation-measurement
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [energy-per-operation, microjoule, charge-per-event, joulescope, ppk2, race-to-sleep, energy-budget, low-power, firmware-embedded-development]
level: advanced
status: draft
description: "Measure energy per operation (sensor read, radio packet, flash write) with a current profiler and GPIO markers, and use it to compare designs and build energy budgets."
sources:
  - https://download.joulescope.com/docs/JoulescopeUsersGuide/index.html
  - https://docs.nordicsemi.com/bundle/ug_ppk2/page/UG/ppk/PPK_user_guide_Intro.html
  - https://www.silabs.com/documents/public/application-notes/an969-measuring-power-consumption.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Energy per operation

Average current depends on how often you do things; **energy per operation** is the property of
the firmware you can optimise and compare.

## Measure
1. Toggle a marker GPIO high at the start of the operation, low at the end. Connect it to the
   profiler's digital input (PPK2 D0-D7, Joulescope GPI, Otii digital in).
2. Capture at >= 100 kS/s; radio bursts have sub-ms structure.
3. Select the marker window and read charge (uC) or energy (uJ). Include tails: regulator
   settling, radio ramp-down, sensor conversion after the I2C write.
4. Subtract the sleep baseline x duration if you want the incremental cost.
5. Repeat 20+ times; report mean and max.

`E = V x Q`. With a regulator, measure at the battery so converter efficiency is included.

## Use the numbers
Battery life = capacity / (sleep current + sum over operations of `Q_op x rate_op`).
Example: BLE advertising event 15 uC every 1 s + sensor read 40 uC every 10 s + 2 uA sleep
-> 15 + 4 + 2 = 21 uA average -> CR2032 (~200 mAh usable) ~ 1 year.

## What usually wins
- **Race to sleep:** run faster to finish sooner if active current scales less than linearly with
  frequency (wait-state flash, static current dominate). Measure both; it is not universal.
- **Batching:** one radio connection sending 10 readings costs far less than 10 connections
  (connection setup dominates).
- **Sensor modes:** one-shot/forced mode with low oversampling; let the sensor's FIFO collect and
  read in bursts.
- **Flash writes:** buffer and write pages, not bytes; erase is the expensive part.
- **Peripheral clocks:** enable only during the operation.

## Gotchas
- Profiler burden voltage (shunt-based meters) can brown out a coin-cell setup; use auto-ranging
  low-burden tools.
- Range switching of the profiler adds glitches at transitions; check its documentation and fix the
  range if comparing small differences.
- GPIO marker itself costs a few uA while high; negligible but keep it consistent.

## Verify
- [ ] Energy per operation tabulated per firmware build and tracked over time.
- [ ] Predicted average current matches a long measurement within 10%.

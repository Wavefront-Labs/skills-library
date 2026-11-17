---
id: computing-software.firmware-embedded-development.hardware-debugging.first-power-on-checklist
name: first-power-on-checklist
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [board-bring-up, power-on-checklist, current-limited-supply, rail-verification, shorts-check, thermal-camera, reset-line, firmware-embedded-development]
level: practitioner
status: draft
description: "Power a new PCB for the first time without destroying it: pre-power resistance checks, current-limited bring-up, rail sequencing, reset and oscillator checks before firmware."
sources:
  - https://www.st.com/resource/en/application_note/an2586-getting-started-with-stm32f10xxx-hardware-development-stmicroelectronics.pdf
  - https://www.ti.com/lit/an/slva957/slva957.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# First power-on checklist

**Goal:** go from bare assembled board to "debugger can attach" safely, finding assembly and
design faults before they cost a board or hours of firmware debugging.

## Before power
1. Visual inspection under magnification: rotated ICs (pin 1 marks), solder bridges on fine-
   pitch parts, missing parts, polarised caps/diodes orientation.
2. **Resistance from each rail to GND** with a multimeter (both polarities): a few ohms or less
   on a rail means a short (bridged cap, reversed part). Compare to a known-good board if you
   have one; large-capacitance rails charge up slowly on the meter.
3. Check input protection orientation (reverse-polarity diode/FET).

## Power up current-limited
- Bench supply at nominal input voltage with the **current limit just above expected idle**
  (e.g. 50-100 mA for an MCU board with no radio). Ramp the voltage up if possible.
- Watch current: a jump to the limit = short or latch-up; switch off immediately.
- Feel/scan for hot parts (thermal camera or finger on suspect ICs for a second).

## Rails and sequencing
- Measure every rail at the load (not just regulator output): value within tolerance, low
  ripple (scope with ground spring).
- Multi-rail SoCs/FPGAs: verify the power-up sequence and ramp times against the datasheet
  with a multi-channel scope; wrong sequencing causes latch-up or failure to boot.
- Power-good / enable chains release in order.

## MCU alive checks (before firmware)
- **NRST**: high after power-up, pulses low on button press; no constant low (supervisor or
  debugger holding it).
- **BOOT pins**: at the level that boots from flash (BOOT0 low on STM32).
- **Oscillators**: HSE/LSE start once firmware enables them; before that, the internal RC is
  used, so a dead crystal doesn't stop debugger attach.
- **VCAP/VCORE** pins (STM32F4/F7/H7): internal regulator output present (~1.2 V); missing VCAP
  capacitors give random resets.
- **Debugger attach**: read the device ID (`st-info --probe`, `JLinkExe` connect, OpenOCD
  init). If it fails, check SWD wiring, target voltage sense pin, and try connect-under-reset.

## Record
Fill a bring-up log per board serial: idle current, rail voltages, observations. It becomes
the reference for production test limits.

## Verify
- [ ] Every rail measured and logged.
- [ ] Debugger reads the correct device ID and can halt the core.
- [ ] Idle current matches estimate within ~20 %.

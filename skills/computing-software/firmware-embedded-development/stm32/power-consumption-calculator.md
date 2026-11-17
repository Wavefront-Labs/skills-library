---
id: computing-software.firmware-embedded-development.stm32.power-consumption-calculator
name: power-consumption-calculator
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-low-power, power-consumption-calculator, cubemx-pcc, battery-life-estimate, low-power-sequence, stm32, firmware-embedded-development]
level: practitioner
status: gated
description: "Estimate STM32 battery life with the CubeMX Power Consumption Calculator: run/sleep/stop step sequences, battery models, and validating against measurements."
sources:
  - https://www.st.com/resource/en/user_manual/um1718-stm32cubemx-for-stm32-configuration-and-initialization-c-code-generation-stmicroelectronics.pdf
  - https://wiki.st.com/stm32mcu/wiki/STM32CubeMX_Power_Consumption_Calculator
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Power consumption calculator (PCC)

CubeMX's "Power Consumption Calculator" tab estimates average current and battery life from a
sequence of steps, using ST's characterisation data for the selected part.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Build a sequence
1. Select VDD and the battery (built-in models: CR2032, Li-ion, AA alkaline; or custom capacity,
   self-discharge, max continuous/pulse current).
2. Add steps. Each step has: mode (Run, Sleep, LPRun, LPSleep, Stop0/1/2, Standby, Shutdown),
   voltage range, clock source and frequency, RAM/flash settings, enabled peripherals, duration.
3. Typical sensor node: Run 5 ms at 16 MHz (measure, compute) -> Run 20 ms with SPI radio TX ->
   Stop 2 for 9.975 s with RTC + LPTIM.
4. Enable "Transition checker" to flag impossible sequences (e.g. Stop 2 from LPRun on L4) and
   account for wake-up transition time/energy.

## Reading results
- Average current, battery life, and per-step contribution: usually the sleep floor or the radio
  dominates. Optimise the dominant step first.
- "Peripherals" consumption is the MCU-internal peripheral current, not external parts.

## What PCC does not include
- External components: regulators' quiescent current, sensors, radio module, pull resistors,
  LEDs, leakage. Add them yourself (spreadsheet: sum over phases of I x t / period).
- Temperature effects: Stop/Standby leakage rises steeply above 50-85 C; PCC uses typical 25 C data.
- Firmware realities: extra awake time from debouncing, retries, log output.

## Validate
Measure the real board with a power analyser (Joulescope, PPK2, STLINK-V3PWR, X-NUCLEO-LPM01A
with STM32CubeMonitor-Power) over several full cycles. Compare per-phase durations and currents
with the PCC sequence and update the model. Expect real floors to be higher than the datasheet
typical; budget for max values at your temperature.

## Verify
- [ ] PCC sequence saved (`.pcs`) in the repo alongside the `.ioc`.
- [ ] Measured average within ~20% of the model, deviations explained.
- [ ] Battery life includes external components and temperature derating.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com, wiki.st.com); no readable alternative was found.

Method: documentation only; no commands were run.

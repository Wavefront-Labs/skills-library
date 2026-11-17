---
id: computing-software.firmware-embedded-development.stm32.gpio-output-speed-and-slew
name: gpio-output-speed-and-slew
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-gpio, gpio-speed, ospeedr, slew-rate, emi, ringing, compensation-cell, io-drive-strength, firmware-embedded-development]
level: practitioner
status: gated
description: "Choose STM32 GPIO OSPEEDR settings per signal: enough edge rate for the interface, no more, to limit EMI, ringing and ground bounce; plus the I/O compensation cell."
sources:
  - https://www.st.com/resource/en/application_note/an4899-stm32-microcontroller-gpio-hardware-settings-and-lowpower-consumption-stmicroelectronics.pdf
  - https://www.st.com/resource/en/datasheet/stm32f407vg.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GPIO output speed and slew

**Goal:** each output's slew rate matched to its job: fast enough for the signal's
frequency, slow enough not to radiate, ring or couple into neighbours.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## What OSPEEDR really sets
Not a frequency limit but the **output driver strength / edge rate**. Values (F4): 00 low,
01 medium, 10 high, 11 very high. The datasheet "I/O AC characteristics" table gives max
frequency and rise/fall time per setting, VDD and load capacitance, e.g. roughly 2-8 MHz for
low, 25-50 MHz medium, 50-100 MHz high, 100+ MHz very high on F4 at 3.3 V with 10-30 pF.

## Choosing
| Signal | Setting |
|---|---|
| LEDs, enables, chip selects, slow GPIO | low |
| UART, I2C (open drain), 1-10 MHz SPI | low or medium |
| 20-50 MHz SPI, SDIO, timers driving fast PWM edges | high |
| FMC/SDRAM, QSPI > 80 MHz, Ethernet RMII clock, trace port, MCO at high freq | very high |
Rule: pick the lowest setting whose rise time is < ~1/10 of the bit period (for 10 MHz SPI,
period 100 ns, rise < 10 ns is plenty).

## Why not "very high everywhere" (CubeMX templates often do)
- Edges in the 1-2 ns range radiate harmonics into hundreds of MHz: fails EMC emissions.
- Ringing/overshoot on unterminated traces: false clocking on SPI SCK, I2C glitches.
- Simultaneous switching of many fast pins causes ground bounce and VDD droop, upsetting
  ADC readings.
- Slightly higher dynamic current.

## Compensation cell (F4/F7/H7)
For pins above ~50 MHz with VDD > 2.4 V, enable the I/O compensation cell to reduce
slew-rate variation: `SYSCFG->CMPCR |= SYSCFG_CMPCR_CMP_PD;` then wait for `READY`
(`HAL_EnableCompensationCell()`). Needed for reliable FMC/QSPI at top speed.

## Verify
- [ ] Scope with a short ground spring on SCK: no overshoot beyond the absolute-max rating,
      no non-monotonic edges.
- [ ] Pins configured above "low" each have a documented reason.
- [ ] Pre-compliance EMC scan (or near-field probe) compared before/after reducing speeds.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.

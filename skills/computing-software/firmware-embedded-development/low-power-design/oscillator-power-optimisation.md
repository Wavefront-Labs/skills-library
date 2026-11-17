---
id: computing-software.firmware-embedded-development.low-power-design.oscillator-power-optimisation
name: oscillator-power-optimisation
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [oscillator-power, lse-drive, lsi-vs-lse, hfxo-on-demand, crystal-startup, msi-auto-calibration, low-power, firmware-embedded-development]
level: practitioner
status: draft
description: "Cut clock-source current: LSE drive strength, LSI vs 32 kHz crystal, starting the HF crystal only when the radio needs it, MSI PLL-mode calibration, and startup-time costs."
sources:
  - https://www.st.com/resource/en/application_note/an2867-guidelines-for-oscillator-design-on-stm8afals-and-stm32-mcusmpus-stmicroelectronics.pdf
  - https://docs.nordicsemi.com/bundle/ps_nrf52840/page/clock.html
  - https://www.st.com/resource/en/application_note/an4621-stm32l4-and-stm32l4-ultralowpower-features-overview-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Oscillator power

## Low-frequency (always-on) clock
- **32.768 kHz crystal (LSE/LFXO):** ~0.1-0.3 uA, +/-20 ppm. Needed for accurate RTC and BLE sleep
  clock (BLE requires <= 500 ppm; 50 ppm lets peers use smaller window widening, saving radio time).
- **Internal RC (LSI/LFRC):** ~0.1-0.6 uA, +/-1-5%. nRF LFRC can be calibrated against HFXO
  periodically (`CTIV`, ~250 ppm), costs HFXO time every few seconds.
- **LSE drive strength (STM32 `RCC_BDCR.LSEDRV`):** low drive uses least current but may not start
  with a high-ESR crystal or after layout contamination. Calculate gain margin
  (`gm_crit` per AN2867), start at medium-high, then lower after verifying margin >= 5 on worst
  units. Changing LSEDRV requires the backup domain write access.

## High-frequency clock
- **HF crystal (HSE/HFXO):** 100-500 uA running. Radios need it for TX/RX accuracy; the CPU often
  does not. nRF: request HFXO only around radio events (SoftDevice/MPSL does this automatically),
  run the CPU on HFINT (64 MHz RC) otherwise. Start-up 0.3-1 ms, budget it per radio event.
- **STM32 MSI with PLL mode (`MSIPLLEN`):** MSI auto-trims to LSE to ~+/-0.25%, good enough for
  UART and USB on some parts, avoiding the HSE entirely.
- Turn off HSE/PLL before Stop; restore after wake (Stop exits on MSI/HSI, so a clock restore
  function is part of every wake path).

## Startup time vs energy
Each wake that needs the HF crystal pays startup current x startup time. For frequent short
wakes, the internal RC with periodic calibration can beat a crystal. Use crystals with low ESR and
small load capacitance (6-7 pF) for fast startup and low drive.

## Gotchas
- 32 kHz crystal traces near noisy signals cause RTC jumps; guard ring and short traces.
- Probing crystal pins changes them; measure the clock via MCO or RTC calibration output.
- Clock security system (LSECSS) costs a little current but detects crystal failure in the field.

## Verify
- [ ] LSE starts on all units across temperature with the chosen drive level (gain margin test).
- [ ] HF crystal active time per hour measured (GPIO marker or profiler) and matches design.

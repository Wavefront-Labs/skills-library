---
id: computing-software.firmware-embedded-development.hardware-debugging.clock-drift-and-timebase-accuracy
name: clock-drift-and-timebase-accuracy
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [clock-drift, ppm, rtc-calibration, crystal-tolerance, lse, hsi-trimming, timebase, hardware-debugging, firmware-embedded-development]
level: advanced
status: draft
description: "Quantify and fix timebase drift: ppm maths, crystal tolerance vs temperature, RC trimming, RTC smooth calibration, measuring frequency, network time correction."
sources:
  - https://www.st.com/resource/en/application_note/an2867-guidelines-for-oscillator-design-on-stm8afals-and-stm32-mcusmpus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an4759-using-the-hardware-realtime-clock-rtc-and-the-tamper-management-unit-tamp-with-stm32-microcontrollers-stmicroelectronics.pdf
  - https://www.microchip.com/en-us/application-notes/an1200
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Clock drift and timebase accuracy

## The maths
1 ppm = 86.4 ms/day = 2.6 s/month. Typical sources:
| Source | Accuracy |
|---|---|
| 32.768 kHz tuning-fork crystal | +/-20 ppm at 25 C, plus parabolic loss -0.034 ppm/C^2 (at -20 C: about -70 ppm) |
| HSE MHz crystal | +/-10-30 ppm |
| TCXO | +/-0.5-2 ppm |
| Internal RC (HSI, LSI) | +/-1-5% (10 000-50 000 ppm), LSI worse |
UART tolerates ~2-3% total mismatch, so HSI is often fine for UART; it is never fine for a clock
that must keep time over days, or for USB (needs 0.25%; use HSE or HSI48 with CRS sync).

## Measure, don't assume
- Output the clock on MCO or an RTC calibration pin (STM32 RTC_OUT 512 Hz / 1 Hz) and measure with
  a frequency counter or scope with a GPS-disciplined reference; 1 Hz over 100 s gives 10 ppm
  resolution, use a gated count over longer windows or the 512 Hz output for faster readings.
- Firmware comparison: count LSE ticks against a timer clocked by a known-good HSE/TCXO, or against
  timestamps from NTP/GPS PPS over hours.

## Correcting
- **Crystal load capacitance:** wrong load caps shift frequency by tens of ppm; fix in hardware.
  LSE drive level too low = startup failures; too high = ageing/overdrive.
- **RTC smooth calibration (STM32):** `RTC_CALR` CALP/CALM adds/removes up to 511 pulses per 32 s
  window, ~0.954 ppm steps, range -487.1 to +488.5 ppm. Store the per-unit value from production
  test in flash.
- **RC trimming:** HSI trim bits (`HSITRIM`), AVR `OSCCAL`; calibrate against a reference (LSE,
  UART break timing, USB SOF via CRS).
- **Temperature compensation:** use the on-chip temperature sensor and the crystal's parabola to
  adjust calibration periodically.
- **Network discipline:** when connected, compute offset vs NTP/GNSS and slew (adjust calibration)
  rather than step, to keep timestamps monotonic.

## Firmware traps
- Tick-counting timers that reload after the ISR (`period - 1` mistakes, reload in software) add a
  cumulative error; use auto-reload hardware and absolute deadlines.
- Low-power modes that switch the RTOS tick from HSE to LSI change the tick accuracy.
- 32-bit millisecond counters wrap after 49.7 days; always compare with unsigned differences.

## Verify
- [ ] Measured drift per unit after calibration within spec across temperature range.
- [ ] 7-day soak against NTP shows expected seconds of error.

---
id: computing-software.firmware-embedded-development.stm32.lse-crystal-for-rtc
name: lse-crystal-for-rtc
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-clocks, lse-rtc-clock, lse-drive, backup-domain, rtc-smooth-calibration, lse-css, stm32, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Start and keep the STM32 32.768 kHz LSE running for the RTC: backup-domain access, drive strength, startup time, clock source locking, and smooth calibration for ppm accuracy."
sources:
  - https://www.st.com/resource/en/application_note/an2867-guidelines-for-oscillator-design-on-stm8afals-and-stm32-mcusmpus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an4759-using-the-hardware-realtime-clock-rtc-and-the-tamper-management-unit-tamp-with-stm32-microcontrollers-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LSE crystal for the RTC

## Bring-up order
LSE, RTC and backup registers live in the **backup domain**, which survives system resets
and runs from VBAT. Writing its registers needs backup access:
```c
HAL_PWR_EnableBkUpAccess();                          /* DBP bit */
__HAL_RCC_LSEDRIVE_CONFIG(RCC_LSEDRIVE_MEDIUMHIGH);  /* before enabling LSE */

RCC_OscInitTypeDef osc = { .OscillatorType = RCC_OSCILLATORTYPE_LSE, .LSEState = RCC_LSE_ON,
                           .PLL.PLLState = RCC_PLL_NONE };
if (HAL_RCC_OscConfig(&osc) != HAL_OK) { lse_fault(); }   /* LSE_STARTUP_TIMEOUT, default 5 s */

RCC_PeriphCLKInitTypeDef pc = { .PeriphClockSelection = RCC_PERIPHCLK_RTC,
                                .RTCClockSelection = RCC_RTCCLKSOURCE_LSE };
HAL_RCCEx_PeriphCLKConfig(&pc);
__HAL_RCC_RTC_ENABLE();
```
- LSE startup is slow: tuning-fork crystals can take **seconds** to stabilise (the HAL default
  `LSE_STARTUP_TIMEOUT` is 5 s). Don't block boot on it if you don't need the RTC
  immediately: start it early and check `LSERDY` later.
- Since the backup domain survives reset, on warm boots the LSE is already running and the RTC
  already set. Check `__HAL_RCC_GET_FLAG(RCC_FLAG_LSERDY)` and an "RTC initialised" marker in a
  backup register before reconfiguring; re-initialising the RTC every boot loses time.
- `RTCSEL` can only be changed after a **backup domain reset** (`__HAL_RCC_BACKUPRESET_FORCE/RELEASE`),
  which also clears RTC and backup registers.

## Drive strength
`RCC_LSEDRIVE_LOW` uses the least current but may not start crystals with high ESR or load
capacitance. Pick a crystal recommended for STM32 (AN2867 gives the LSE drive levels per series and
recommended crystals with CL/ESR; low-power designs pick the smallest CL, the ~6-7 pF class),
then check gain margin (AN2867: >3 for LSE, >5 for HSE). A board that starts LSE at
room temperature can fail cold; test at the low temperature limit. Increase drive if marginal,
but on some series the LSE gain is only modifiable with the oscillator off (AN2867:
statically modifiable LSE oscillators), not on the fly.

## Accuracy and calibration
A 20 ppm crystal drifts up to ~1.7 s/day, more at temperature extremes (tuning-fork crystals
follow a parabolic temperature curve, drifting more away from room temperature).
```c
/* measure with RTC calibration output (512 Hz or 1 Hz on RTC_OUT pin) and a frequency counter */
HAL_RTCEx_SetCalibrationOutPut(&hrtc, RTC_CALIBOUTPUT_1HZ);
/* correct: positive ppm error -> remove pulses */
HAL_RTCEx_SetSmoothCalib(&hrtc, RTC_SMOOTHCALIB_PERIOD_32SEC,
                         RTC_SMOOTHCALIB_PLUSPULSES_RESET, calm_value);
```
Smooth calibration resolution is about 0.954 ppm over 32 s. Store the per-unit value from
production test in flash/backup registers. Temperature compensation can update it periodically.

## Failure detection
`HAL_RCCEx_EnableLSECSS()` (series with LSE CSS) flags LSE failure, can wake from low power,
and the RTC can switch to LSI to keep running roughly. Handle `HAL_RCCEx_LSECSS_Callback`.

## Layout
Short traces, ground guard ring around crystal and caps, no signals routed underneath. LSE
pins are very high-impedance: flux residue or a scope probe can stop the oscillator. Measure
via the calibration output, not on the crystal pins.

## Verify
- [ ] LSE starts at minimum operating temperature on several boards.
- [ ] Warm reset doesn't reset the RTC time.
- [ ] Drift over 24 h within spec after calibration (compare with NTP or GPS PPS).

## Checked

2026-10-31: Confirmed the HAL macros (`__HAL_RCC_LSEDRIVE_CONFIG`, `HAL_RCCEx_PeriphCLKConfig`, `__HAL_RCC_BACKUPRESET_FORCE`, `HAL_RCCEx_EnableLSECSS`, `HAL_RTCEx_SetSmoothCalib`, `RTC_SMOOTHCALIB_*`, `HAL_RTCEx_SetCalibrationOutPut`, `RTC_CALIBOUTPUT_1HZ`), the LSE_STARTUP_TIMEOUT 5000 ms default and LSE_VALUE 32768 Hz against the L4 HAL sources; the smooth-calibration resolution of about 0.954 ppm over the 32 s window, its +/-487.1 ppm range, the 512 Hz / 1 Hz calibration output and CALP/CALM fields against AN4759; gain margin (>5 HSE, >3 LSE) and the statically- vs on-the-fly-modifiable LSE gain families, plus small-CL (about 6-7 pF) guidance, against AN2867. Rewrote: the LSE startup-time claim (anchored on the 5 s HAL timeout instead of an unverified range), the CL/drive guidance, and the drive-modification rule (now the AN2867 statically-modifiable-gain rule); removed the unverified -0.034 ppm/degC2 parabolic coefficient.

Method: documentation only; no commands were run.

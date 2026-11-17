---
id: computing-software.firmware-embedded-development.stm32.adc-self-calibration
name: adc-self-calibration
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-adc, stm32-adc-calibration, hal-adcex-calibration-start, calfact, offset-calibration, differential-calibration, recalibration-temperature, firmware-embedded-development]
level: practitioner
status: draft
description: "Run STM32 ADC self-calibration at the right moment (ADC disabled, after voltage regulator start-up), store/restore CALFACT across low-power modes, and add system-level gain calibration."
sources:
  - https://www.st.com/resource/en/application_note/an2834-how-to-get-the-best-adc-accuracy-in-stm32-microcontrollers-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ADC self-calibration (STM32)

**Goal:** remove the ADC's internal offset error (several LSB uncalibrated) and know which
errors calibration does not fix.

## When and how
Most newer families (F0/L0/L4/G0/G4/H7/U5) have a calibration routine that measures the offset
and stores a correction factor (`CALFACT`):
```c
/* ADC must be DISABLED, voltage regulator enabled and settled (HAL does this in Init) */
HAL_ADCEx_Calibration_Start(&hadc1, ADC_SINGLE_ENDED);
/* separate calibration for differential inputs on families that support them */
HAL_ADCEx_Calibration_Start(&hadc1, ADC_DIFFERENTIAL_ENDED);
HAL_ADC_Start(&hadc1);
```
H7 adds a linearity calibration (`ADC_CALIB_OFFSET_LINEARITY`) taking longer. F1 uses
`HAL_ADCEx_Calibration_Start(&hadc)` without mode; F4/F7 have no self-calibration.

## Rules
- Calibrate **after** power-up and once VDDA/VREF+ is stable, before the first conversion.
- **Recalibrate** when temperature changes significantly (> ~20 C), VDDA changes, or after
  long ADC power-down; offset drifts with both.
- **Low-power modes** that power the ADC down (Stop 2/Standby on L4) can lose `CALFACT`. Save
  it (`HAL_ADCEx_Calibration_GetValue`) after calibration and restore with
  `HAL_ADCEx_Calibration_SetValue` on wake, instead of re-running calibration each time (which
  costs ~100 us+).
- Calibration fixes **ADC offset only**: gain error from the reference, divider tolerances,
  source impedance and front-end op-amp offsets need system calibration.

## System (two-point) calibration
Measure two known inputs (e.g. 10 % and 90 % of range) during production test, compute gain and
offset, store in flash/OTP, apply in software:
`corrected = (raw - raw_lo) * (V_hi - V_lo) / (raw_hi - raw_lo) + V_lo`. Use VREFINT to
compensate VDDA variation when VDDA is the reference (see VREFINT skill).

## Verify
- [ ] Grounded input reads 0-2 LSB after calibration (vs several LSB before).
- [ ] Calibration value logged at boot is within the range seen on other units (outliers point
      to hardware issues).
- [ ] Readings stay consistent before and after a Stop-mode wake cycle.

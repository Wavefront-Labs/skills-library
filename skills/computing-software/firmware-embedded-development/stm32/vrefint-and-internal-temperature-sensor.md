---
id: computing-software.firmware-embedded-development.stm32.vrefint-and-internal-temperature-sensor
name: vrefint-and-internal-temperature-sensor
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-adc, vrefint, vrefint-cal, ts-cal1, ts-cal2, internal-temperature-sensor, vdda-compensation, factory-calibration-values, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Use STM32 VREFINT and the internal temperature sensor with factory calibration values (VREFINT_CAL, TS_CAL1/2) to compute VDDA and die temperature correctly."
sources:
  - https://www.st.com/resource/en/application_note/an2834-how-to-get-the-best-adc-accuracy-in-stm32-microcontrollers-stmicroelectronics.pdf
  - https://www.st.com/resource/en/datasheet/stm32l476rg.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VREFINT and the internal temperature sensor

**Goal:** accurate absolute voltages when VDDA isn't precisely known, and a usable die
temperature reading.

## Factory calibration values
Stored in system memory during production test; addresses and conditions are in the
datasheet ("Embedded internal voltage reference" and "Temperature sensor" sections), exposed
by CMSIS/LL as macros:
- `VREFINT_CAL_ADDR`: raw VREFINT reading at `VREFINT_CAL_VREF` (3000 mV on L4/G4, 3300 mV on
  F4-class parts; check your part).
- `TEMPSENSOR_CAL1_ADDR` at `TEMPSENSOR_CAL1_TEMP` (30 C), `TEMPSENSOR_CAL2_ADDR` at
  `TEMPSENSOR_CAL2_TEMP` (110 or 130 C depending on part), both at `TEMPSENSOR_CAL_VREFANALOG`.

## VDDA from VREFINT
```c
uint32_t vrefint_raw = adc_read(ADC_CHANNEL_VREFINT);
uint32_t vdda_mv = __LL_ADC_CALC_VREFANALOG_VOLTAGE(vrefint_raw, LL_ADC_RESOLUTION_12B);
/* any channel in mV, ratiometric-corrected: */
uint32_t ch_mv = __LL_ADC_CALC_DATA_TO_VOLTAGE(vdda_mv, raw, LL_ADC_RESOLUTION_12B);
```
This removes VDDA tolerance (e.g. a 3.3 V LDO at +/-2 %) from absolute measurements.

## Temperature
```c
int32_t t_c = __LL_ADC_CALC_TEMPERATURE(vdda_mv, ts_raw, LL_ADC_RESOLUTION_12B);
```
The macro scales the raw value to the calibration VDDA before interpolating between TS_CAL1
and TS_CAL2. Accuracy: about +/-1-2 C sensor linearity (L476 datasheet) with two-point calibration; parts
with only one cal point (or the "typical slope" formula on F4:
`(V_sense - V25)/Avg_Slope + 25` with datasheet `V25` and `Avg_Slope` parameters) are much
worse: use only for relative changes.
It measures **die** temperature, which runs above ambient under load.

## Enabling and sampling
- Enable the internal paths: `LL_ADC_SetCommonPathInternalCh(ADC12_COMMON,
  LL_ADC_PATH_INTERNAL_VREFINT | LL_ADC_PATH_INTERNAL_TEMPSENSOR)` (HAL does it when you
  configure those channels), then wait the start-up time (`LL_ADC_DELAY_TEMPSENSOR_STAB_US`; the L476
  datasheet gives tSTART up to 120 us).
- Use the **minimum sampling time from the datasheet** (`tS_vrefint` 4 us and `tS_temp` 5 us
  minimum on the L476); short sampling gives low, noisy readings.
- Disable the paths afterwards in low-power designs (they draw current).

## Verify
- [ ] Computed VDDA matches a multimeter on VDDA within ~1 %.
- [ ] Temperature tracks a reference at two temperatures (oven or freezer test).

## Checked

2026-10-31: Confirmed `VREFINT_CAL_ADDR`, `VREFINT_CAL_VREF` (3000 mV L4 / 3300 mV F4), `TEMPSENSOR_CAL1_ADDR`/`TEMPSENSOR_CAL2_ADDR`, `TEMPSENSOR_CAL1_TEMP` 30 C, `TEMPSENSOR_CAL2_TEMP` 110 or 130 C, `TEMPSENSOR_CAL_VREFANALOG` and the `__LL_ADC_CALC_VREFANALOG_VOLTAGE`/`DATA_TO_VOLTAGE`/`TEMPERATURE` macros from stm32l4xx_ll_adc.h and stm32f4xx_ll_adc.h; tS_vrefint 4 us, tS_temp 5 us, tSTART up to 120 us, VREFINT 1.212 V typ, V30 0.76 V at 3.0 V and the TS linearity/slope table from the STM32L476RG datasheet; the F4 `(V_sense - V25)/Avg_Slope + 25` formula from stm32f4xx_ll_adc.h. Fixed the macro names (`TS_CAL1_ADDR` -> `TEMPSENSOR_CAL1_ADDR`), replaced the tS/tSTART ranges with the datasheet figures, and removed the unverified accuracy error figures.

Method: documentation only; no commands were run.

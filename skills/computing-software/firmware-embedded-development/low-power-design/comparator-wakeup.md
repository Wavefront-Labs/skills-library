---
id: computing-software.firmware-embedded-development.low-power-design.comparator-wakeup
name: comparator-wakeup
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [comparator-wakeup, lpcomp, comp-exti, analog-threshold-wake, hysteresis, battery-threshold-wake, low-power, firmware-embedded-development]
level: practitioner
status: draft
description: "Wake an MCU on an analog threshold with a low-power comparator (nRF LPCOMP, STM32 COMP via EXTI): reference choice, hysteresis, ultra-low-power mode, and debouncing noise."
sources:
  - https://docs.nordicsemi.com/bundle/ps_nrf52840/page/lpcomp.html
  - https://www.st.com/resource/en/application_note/an4232-getting-started-with-analog-comparators-for-stm32f3-series-and-stm32g4-series-devices-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Comparator wake-up

**Use when:** the wake condition is analog (light level, battery voltage, piezo/vibration signal,
analog sensor output crossing a limit) and periodic ADC sampling would cost more.

## Nordic LPCOMP
- Works in System ON idle and System OFF (wake = reset with `RESETREAS.LPCOMP`). ~0.5 uA.
- Reference: fractions of VDD (1/8..7/8, 1/16 steps) or external AREF pin.
- Detect UP, DOWN or CROSS; hysteresis enable (`HYST` ~50 mV).
```c
NRF_LPCOMP->PSEL = LPCOMP_PSEL_PSEL_AnalogInput2;
NRF_LPCOMP->REFSEL = LPCOMP_REFSEL_REFSEL_Ref4_8Vdd;
NRF_LPCOMP->ANADETECT = LPCOMP_ANADETECT_ANADETECT_Up;   /* System OFF wake on up crossing */
NRF_LPCOMP->HYST = 1;
NRF_LPCOMP->ENABLE = 1; NRF_LPCOMP->TASKS_START = 1;
while (!NRF_LPCOMP->EVENTS_READY) {}
NRF_POWER->SYSTEMOFF = 1;
```
Zephyr/nrfx: `nrfx_lpcomp`. Note LPCOMP and SAADC/COMP share resources on some parts.

## STM32 COMP
- COMP output routed to EXTI lines (L4: COMP1 EXTI21, COMP2 EXTI22) wakes from Stop 0/1/2.
- Inputs: GPIO, DAC channel, VREFINT fractions (1/4, 1/2, 3/4, 1) via the internal ladder.
- `PWRMODE` ultra-low-power (~0.5 uA, slower ~us response) vs high-speed (~5-10 uA).
- `HYST` none/low/medium/high (~8/18/27 mV-ish, see datasheet).
```c
hcomp.Init.InputPlus = COMP_INPUT_PLUS_IO1; hcomp.Init.InputMinus = COMP_INPUT_MINUS_1_2VREFINT;
hcomp.Init.Hysteresis = COMP_HYSTERESIS_MEDIUM; hcomp.Init.Mode = COMP_POWERMODE_ULTRALOWPOWER;
hcomp.Init.TriggerMode = COMP_TRIGGERMODE_IT_RISING;
HAL_COMP_Init(&hcomp); HAL_COMP_Start(&hcomp);
```
VREFINT scaler costs a few uA (`SCALEN`/`BRGEN`); an external divider with high resistance can be
cheaper.

## Design notes
- Noise near the threshold causes wake storms: use hysteresis, an RC filter on the input, and in
  firmware disable the comparator interrupt for a hold-off period after each wake.
- Threshold in terms of VDD drifts as a battery discharges; use an absolute reference (VREFINT)
  if the sensor output is absolute.
- Comparator inputs need the pin in analog mode; GPIO digital input buffers on a mid-level analog
  signal draw crowbar current.

## Verify
- [ ] Sweeping the input with a lab supply wakes at the computed threshold +/- hysteresis.
- [ ] No spurious wakes over 12 h with the input held near the threshold.

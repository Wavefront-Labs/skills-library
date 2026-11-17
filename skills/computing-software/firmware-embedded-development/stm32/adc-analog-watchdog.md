---
id: computing-software.firmware-embedded-development.stm32.adc-analog-watchdog
name: adc-analog-watchdog
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-adc, analog-watchdog, awd-threshold, adc-window-interrupt, overvoltage-detection, stm32, firmware-embedded-development]
level: practitioner
status: gated
description: "Use the STM32 ADC analog watchdog to trigger an interrupt or timer break when a channel leaves a voltage window, without the CPU checking every sample."
sources:
  - https://www.st.com/resource/en/reference_manual/rm0440-stm32g4-series-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an4277-using-stm32-device-pwm-shutdown-features-for-motor-control-and-digital-power-conversion-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Analog watchdog

The ADC compares each conversion against high/low thresholds and sets the AWD flag (with
interrupt) when outside. AWD1 watches one or all channels; AWD2/AWD3 (L4, G4, H7) watch a channel
set with lower 8-bit resolution thresholds.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Configure
```c
ADC_AnalogWDGConfTypeDef w = {0};
w.WatchdogNumber = ADC_ANALOGWATCHDOG_1;
w.WatchdogMode = ADC_ANALOGWATCHDOG_SINGLE_REG;
w.Channel = ADC_CHANNEL_3;
w.ITMode = ENABLE;
w.HighThreshold = 3500;      /* raw codes at current resolution */
w.LowThreshold  = 500;
HAL_ADC_AnalogWDGConfig(&hadc1, &w);

void HAL_ADC_LevelOutOfWindowCallback(ADC_HandleTypeDef *h) {
    /* fires on every out-of-window conversion: disable or rate-limit */
    __HAL_ADC_DISABLE_IT(h, ADC_IT_AWD1);
    fault_flag = 1;
}
```

## Behaviour to know
- The flag re-sets on every out-of-window conversion. At 1 Msps continuous conversion, an
  unhandled condition is an interrupt storm. Disable the interrupt in the callback and re-enable
  after the condition clears (poll, or move thresholds for hysteresis).
- There is no built-in hysteresis: implement it by swapping thresholds after a trip.
- Thresholds are compared against the result after oversampling/shift on some series, raw on
  others; with oversampling, check the RM section "analog watchdog".
- G4/H7 offer filtering (`FilteringConfig`: trip only after N consecutive out-of-window samples).

## Hardware protection
On G4/F3, AWD outputs can feed timer break or ETR inputs (`ADCx_AWDy` in the timer's break source
list) to shut PWM down without software latency. On other series, combine with a comparator
(COMP) for hardware speed.

## Verify
- [ ] Voltage swept across thresholds: callback fires once per excursion with interrupt management.
- [ ] Trip latency measured (conversion time + ISR) meets protection requirement.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.

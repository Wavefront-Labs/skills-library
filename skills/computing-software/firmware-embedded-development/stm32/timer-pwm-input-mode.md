---
id: computing-software.firmware-embedded-development.stm32.timer-pwm-input-mode
name: timer-pwm-input-mode
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-timers, pwm-input, duty-cycle-measurement, slave-reset-mode, ti1fp1, stm32, firmware-embedded-development]
level: practitioner
status: gated
description: "Measure an external PWM signal's frequency and duty cycle in hardware with STM32 PWM input mode: two channels on one pin, slave reset mode and range limits."
sources:
  - https://www.st.com/resource/en/application_note/an4776-generalpurpose-timer-cookbook-for-stm32-microcontrollers-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PWM input mode

PWM input mode maps one input pin (TI1) to two capture channels: CH1 captures on the rising
edge (period), CH2 on the falling edge (high time). The slave controller resets the counter on
each rising edge, so CCR1 = period and CCR2 = pulse width directly.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Setup (HAL / CubeMX "PWM Input on CH1")
```c
TIM_SlaveConfigTypeDef s = { .SlaveMode = TIM_SLAVEMODE_RESET, .InputTrigger = TIM_TS_TI1FP1,
    .TriggerPolarity = TIM_INPUTCHANNELPOLARITY_RISING, .TriggerFilter = 0 };
HAL_TIM_SlaveConfigSynchro(&htim2, &s);
TIM_IC_InitTypeDef ic = { .ICPolarity = TIM_INPUTCHANNELPOLARITY_RISING,
    .ICSelection = TIM_ICSELECTION_DIRECTTI, .ICPrescaler = TIM_ICPSC_DIV1, .ICFilter = 4 };
HAL_TIM_IC_ConfigChannel(&htim2, &ic, TIM_CHANNEL_1);
ic.ICPolarity = TIM_INPUTCHANNELPOLARITY_FALLING; ic.ICSelection = TIM_ICSELECTION_INDIRECTTI;
HAL_TIM_IC_ConfigChannel(&htim2, &ic, TIM_CHANNEL_2);
HAL_TIM_IC_Start_IT(&htim2, TIM_CHANNEL_1);
HAL_TIM_IC_Start(&htim2, TIM_CHANNEL_2);

void HAL_TIM_IC_CaptureCallback(TIM_HandleTypeDef *h) {
    if (h->Channel == HAL_TIM_ACTIVE_CHANNEL_1) {
        uint32_t period = HAL_TIM_ReadCapturedValue(h, TIM_CHANNEL_1) + 1;
        uint32_t high   = HAL_TIM_ReadCapturedValue(h, TIM_CHANNEL_2) + 1;
        freq_hz = timclk / (psc + 1) / period;
        duty = (float)high / period;
    }
}
```
Only TI1 and TI2 can be used (channels 1/2 pair), not CH3/CH4.

## Range
- Max measurable period = (ARR+1) ticks: choose PSC so the slowest expected signal fits
  (counter overflow without capture means "below range"; detect with the update interrupt).
- Resolution at high frequency = 1 tick: at 1 MHz input with 80 MHz tick, 80 counts (1.25%).
- 32-bit TIM2/TIM5 give huge range at PSC = 0.

## No signal / 0% / 100% duty
A constant level produces no edges: captures stop. Use the update (overflow) interrupt as a
timeout and report 0% or 100% from the pin level.

## Filtering
`ICFilter` rejects glitches (N samples at fDTS/x). Set it for noisy RC receiver or fan tach lines.

## Verify
- [ ] Signal generator sweep: frequency and duty within 1 tick across the range.
- [ ] Signal removed: timeout reports loss within one period-limit.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.

---
id: computing-software.firmware-embedded-development.stm32.adc-timer-triggered-conversions
name: adc-timer-triggered-conversions
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-adc, adc-external-trigger, timer-trgo, adc-dma-sampling-rate, synchronous-sampling, stm32, firmware-embedded-development]
level: practitioner
status: gated
description: "Sample STM32 ADC channels at an exact rate using a timer TRGO external trigger and DMA, including edge selection, PWM-synchronised sampling and jitter-free audio or DSP capture."
sources:
  - https://www.st.com/resource/en/application_note/an3116-stm32s-adc-modes-and-their-applications-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timer-triggered ADC conversions

Software-started conversions in a loop have jittery sample timing. A timer trigger gives
crystal-accurate sampling, essential for FFT, filtering and audio.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Timer side
```c
/* TIM6 basic timer, 10 kHz update -> TRGO */
htim6.Init.Prescaler = 0;
htim6.Init.Period = (SystemCoreClock / 10000) - 1;       /* use actual timer clock */
HAL_TIM_Base_Init(&htim6);
TIM_MasterConfigTypeDef m = { .MasterOutputTrigger = TIM_TRGO_UPDATE, .MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE };
HAL_TIMEx_MasterConfigSynchronization(&htim6, &m);
```

## ADC side
```c
hadc1.Init.ContinuousConvMode = DISABLE;                     /* one sequence per trigger */
hadc1.Init.ExternalTrigConv = ADC_EXTERNALTRIG_T6_TRGO;
hadc1.Init.ExternalTrigConvEdge = ADC_EXTERNALTRIGCONVEDGE_RISING;
hadc1.Init.DMAContinuousRequests = ENABLE;                   /* keep DMA going in circular mode */
hadc1.Init.Overrun = ADC_OVR_DATA_OVERWRITTEN;
HAL_ADC_Init(&hadc1);
HAL_ADCEx_Calibration_Start(&hadc1, ADC_SINGLE_ENDED);
HAL_ADC_Start_DMA(&hadc1, (uint32_t *)buf, N);               /* DMA circular */
HAL_TIM_Base_Start(&htim6);
```
Process blocks in `HAL_ADC_ConvHalfCpltCallback` / `HAL_ADC_ConvCpltCallback`.

## Sampling at a PWM point (motor/power control)
Trigger from a PWM timer channel or TRGO2 at the centre of the PWM period (centre-aligned mode,
e.g. OC4REF as TRGO2 with CCR4 set near ARR) so current is sampled while
switches are quiet. Injected channels with `ExternalTrigInjecConv = TIM1_TRGO2` are typical.

## Checks
- Total conversion time per sequence (sampling + 12.5 cycles per channel) must be shorter than
  the trigger period, otherwise triggers are missed (or overrun).
- Trigger edge: rising only; "both" doubles the rate.
- `ContinuousConvMode = ENABLE` ignores the timer after the first trigger: classic mistake.

## Verify
- [ ] Toggle a GPIO in the DMA callback: callback rate equals sample rate / (N/2).
- [ ] FFT of a known sine shows the tone at the correct bin.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.

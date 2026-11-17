---
id: computing-software.firmware-embedded-development.stm32.adc-injected-channels
name: adc-injected-channels
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-adc, adc-injected, jsqr, injected-trigger, pwm-synchronised-sampling, motor-current-sense, jdr-registers, auto-injection, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Use STM32 ADC injected channels for high-priority, PWM-synchronised samples that interrupt the regular sequence (motor phase currents), read from the dedicated JDR registers."
sources:
  - https://www.st.com/resource/en/application_note/an3116-stm32s-adc-modes-and-their-applications-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0440-stm32g4-series-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ADC injected channels

**Goal:** sample a few critical channels at exactly the right instant (e.g. mid-PWM for motor
current) while slower housekeeping channels run as a regular sequence on the same ADC.

## How injected conversions differ
- Up to 4 injected channels in `JSQR`, each result in its own register `JDR1..4` (no DMA
  needed, no buffer ordering issues).
- An injected trigger **interrupts** an ongoing regular conversion; the regular sequence
  resumes afterwards.
- Separate trigger source (`JEXTSEL`), typically a timer compare/TRGO2 at the PWM centre.
- Per-channel offset registers can subtract a calibration offset in hardware (signed results).

## Setup (HAL)
```c
ADC_InjectionConfTypeDef inj = {0};
inj.InjectedChannel = ADC_CHANNEL_1;
inj.InjectedRank = ADC_INJECTED_RANK_1;
inj.InjectedSamplingTime = ADC_SAMPLETIME_6CYCLES_5;
inj.InjectedSingleDiff = ADC_SINGLE_ENDED;
inj.InjectedOffsetNumber = ADC_OFFSET_NONE;
inj.InjectedNbrOfConversion = 2;
inj.ExternalTrigInjecConv = ADC_EXTERNALTRIGINJEC_T1_TRGO2;
inj.ExternalTrigInjecConvEdge = ADC_EXTERNALTRIGINJECCONV_EDGE_RISING;
inj.AutoInjectedConv = DISABLE;
HAL_ADCEx_InjectedConfigChannel(&hadc1, &inj);
/* rank 2 similarly, then: */
HAL_ADCEx_InjectedStart_IT(&hadc1);
void HAL_ADCEx_InjectedConvCpltCallback(ADC_HandleTypeDef *h) {
    int32_t ia = HAL_ADCEx_InjectedGetValue(h, ADC_INJECTED_RANK_1);
    int32_t ib = HAL_ADCEx_InjectedGetValue(h, ADC_INJECTED_RANK_2);
    foc_current_loop(ia, ib);         /* runs every PWM period */
}
```
Timer: centre-aligned PWM on TIM1, `TRGO2` from OC4REF with CCR4 near ARR (counter peak) so
sampling happens when low-side switches are on and switching noise has settled.

## Dual-ADC simultaneous injected mode
For two phase currents sampled at the **same instant**, put one channel on ADC1 and one on ADC2
in dual simultaneous injected mode (`ADC_DUALMODE_INJECSIMULT`). Single-ADC sequential ranks are
offset by one conversion time.

## Gotchas
- STM32G4 JSQR is a queue (`JQM` context queue); writing JSQR while conversions are pending
  needs care; read the RM section on injected context queue.
- Injected interrupt latency + control loop must finish within one PWM period: measure with a GPIO.
- Auto-injected mode (injected after regular, no trigger) is a different use case; disable it for
  triggered sampling.

## Verify
- [ ] Scope: GPIO toggle in the callback aligned to PWM centre, constant phase.
- [ ] Regular channels still update while injected conversions run every PWM period.

## Checked

2026-10-31: Confirmed the injected data registers ADC_JDR1..JDR4 and the injected-channel HAL API from stm32l476xx.h and stm32l4xx_hal_adc.h/_ex.h.

Method: documentation only; no commands were run.

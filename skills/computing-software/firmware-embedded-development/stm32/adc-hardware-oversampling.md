---
id: computing-software.firmware-embedded-development.stm32.adc-hardware-oversampling
name: adc-hardware-oversampling
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-adc, adc-oversampling, oversampling-ratio, adc-resolution-boost, ovss-shift, stm32, firmware-embedded-development]
level: practitioner
status: gated
description: "Use the STM32 ADC hardware oversampler (L4, G0, G4, U5, H7) to average and extend resolution to 16 bits without CPU load: ratio, shift, triggered modes and noise limits."
sources:
  - https://www.st.com/resource/en/application_note/an2668-improving-stm32f1-series-stm32f3-series-and-stm32lx-series-adc-resolution-by-oversampling-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ADC hardware oversampling

The oversampler accumulates N conversions (ratio 2..256, up to 1024 on H7) and right-shifts the
sum (0..8 bits) before writing DR. One DR value, one DMA transfer, one interrupt.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Configure
```c
hadc1.Init.OversamplingMode = ENABLE;
hadc1.Init.Oversampling.Ratio = ADC_OVERSAMPLING_RATIO_256;
hadc1.Init.Oversampling.RightBitShift = ADC_RIGHTBITSHIFT_4;          /* 12 + 8 - 4 = 16-bit result */
hadc1.Init.Oversampling.TriggeredMode = ADC_TRIGGEREDMODE_SINGLE_TRIGGER;
hadc1.Init.Oversampling.OversamplingStopReset = ADC_REGOVERSAMPLING_CONTINUED_MODE;
HAL_ADC_Init(&hadc1);
```
Result width = 12 + log2(ratio) - shift. Sum of 256 12-bit samples is 20 bits; shift 4 gives 16
bits, shift 8 gives a plain 12-bit average.

## Does it really add resolution
Each 4x oversampling adds one effective bit **only if** there is at least ~1 LSB of random noise
(dither) on the input. A very clean, stable input averages to the same code: no gain. Real
boards usually have enough noise; check by looking at the raw spread.

Trade: conversion rate drops by the ratio. 256x at 1 Msps -> ~3.9 ksps effective.

## Modes
- **Single trigger** (default): one trigger runs all N conversions back to back.
- **Triggered mode** (`ADC_TRIGGEREDMODE_MULTI_TRIGGER`): each conversion needs a trigger,
  so a timer spreads samples over time (filters low-frequency interference such as 50/60 Hz when
  spread over a whole mains period).
- Injected channels have their own oversampling enable (`InjectedOversamplingMode`).
- With scan mode, each channel is oversampled before moving to the next.

## Pitfalls
- Change oversampling settings only with ADC disabled (`HAL_ADC_DeInit`/`Init`).
- Data alignment: left alignment with 16-bit results is not available in all combinations.
- Analog watchdog compares the oversampled (shifted) result on some series, raw on others: check RM.

## Verify
- [ ] Noise (standard deviation) of results drops by sqrt(ratio) on a DC input.
- [ ] Conversion rate measured matches the expected reduced rate.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.

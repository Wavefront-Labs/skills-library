---
id: computing-software.firmware-embedded-development.stm32.adc-scan-mode-with-dma
name: adc-scan-mode-with-dma
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-adc, adc-scan-dma, regular-sequence, continuous-conversion, circular-dma, timer-triggered-adc, overrun, sampling-time-per-channel, firmware-embedded-development]
level: practitioner
status: gated
description: "Sample several STM32 ADC channels continuously or on a timer trigger with scan mode and circular DMA, without overruns, channel misalignment or stale data."
sources:
  - https://www.st.com/resource/en/application_note/an3116-stm32s-adc-modes-and-their-applications-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an2834-how-to-get-the-best-adc-accuracy-in-stm32-microcontrollers-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ADC scan mode with DMA

**Goal:** a buffer that always holds fresh samples of N channels at a defined rate, filled by
hardware.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Configuration (HAL, G4/L4/F4 style)
```c
hadc.Init.ScanConvMode = ADC_SCAN_ENABLE;
hadc.Init.ContinuousConvMode = DISABLE;               /* one sequence per trigger */
hadc.Init.ExternalTrigConv = ADC_EXTERNALTRIG_T6_TRGO; /* timer sets the sample rate */
hadc.Init.ExternalTrigConvEdge = ADC_EXTERNALTRIGCONVEDGE_RISING;
hadc.Init.NbrOfConversion = 3;
hadc.Init.DMAContinuousRequests = ENABLE;             /* keep DMA requests after first buffer */
hadc.Init.Overrun = ADC_OVR_DATA_OVERWRITTEN;
/* ranks 1..3 with HAL_ADC_ConfigChannel(&hadc, &ch) each, sampling time per channel */
HAL_ADCEx_Calibration_Start(&hadc, ADC_SINGLE_ENDED);  /* families with calibration */
HAL_ADC_Start_DMA(&hadc, (uint32_t *)buf, 3 * N_SAMPLES);   /* DMA circular, halfword */
HAL_TIM_Base_Start(&htim6);                              /* TRGO = update */
```
Process in `HAL_ADC_ConvHalfCpltCallback` (first half) and `HAL_ADC_ConvCpltCallback` (second
half) while DMA fills the other half.

## Rules
- **DMA in circular mode** with `DMAContinuousRequests = ENABLE`; otherwise conversion stops
  after one buffer.
- **Buffer length a multiple of the sequence length**, so `buf[i*3 + k]` is always channel k.
  If DMA ever misses a sample (overrun), channels rotate permanently: detect via the OVR flag
  and restart ADC+DMA.
- Data width: DMA halfword for 12-bit results into a `uint16_t` array.
- Sample rate is set by the timer, not by ADC continuous mode: continuous mode runs as fast as
  possible and floods DMA/CPU.
- Total conversion time (sum of sampling + 12.5 cycles per channel) must be shorter than the
  trigger period.
- Cortex-M7 (F7/H7) with D-cache: buffer in non-cacheable memory, or invalidate the half before
  reading it.

## Choosing sampling time
Per channel, from source impedance: longer sampling for high-impedance sources (dividers,
sensors) and internal channels (VREFINT/temperature need long minimum sampling times, often
> 5-10 us, see datasheet).

## Verify
- [ ] Known voltages on each channel appear in the right buffer slots over hours (no rotation).
- [ ] Toggle a GPIO in the callbacks: callback rate = trigger rate x samples per half / sequence length.
- [ ] OVR flag never set in normal operation.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.

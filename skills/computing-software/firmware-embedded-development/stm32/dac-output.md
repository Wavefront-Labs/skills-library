---
id: computing-software.firmware-embedded-development.stm32.dac-output
name: dac-output
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-adc, stm32-dac, dac-dma-waveform, dac-output-buffer, triangle-noise-generation, stm32, firmware-embedded-development]
level: practitioner
status: gated
description: "Generate analog voltages and waveforms with the STM32 DAC: output buffer choice, timer-triggered DMA waveforms, built-in noise/triangle, and settling and load limits."
sources:
  - https://www.st.com/resource/en/application_note/an3126-audio-and-waveform-generation-using-the-dac-in-stm32-products-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an4566-extending-the-dac-performance-of-stm32-microcontrollers-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DAC output

## Static voltage
```c
DAC_ChannelConfTypeDef c = { .DAC_Trigger = DAC_TRIGGER_NONE, .DAC_OutputBuffer = DAC_OUTPUTBUFFER_ENABLE };
HAL_DAC_ConfigChannel(&hdac1, &c, DAC_CHANNEL_1);
HAL_DAC_Start(&hdac1, DAC_CHANNEL_1);
HAL_DAC_SetValue(&hdac1, DAC_CHANNEL_1, DAC_ALIGN_12B_R, 2048);    /* ~VREF/2 */
```
Vout = VREF+ x code / 4096. VREF+ on small packages is VDDA: accuracy follows your supply.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Output buffer
- Buffer on: drives loads down to ~5 kohm, but output can't reach the rails (~0.2 V from each,
  see datasheet). Good default for external loads.
- Buffer off: rail to rail, but high output impedance (~10-15 kohm): only for high-impedance
  loads or internal connections (comparator, OPAMP input).
- Newer DACs (L4/G4/H7) have "sample and hold" mode for low-power holding of a voltage.

## Waveforms with DMA
```c
c.DAC_Trigger = DAC_TRIGGER_T6_TRGO;
HAL_DAC_ConfigChannel(&hdac1, &c, DAC_CHANNEL_1);
/* TIM6 TRGO at sample rate, e.g. 32 samples per period x 1 kHz = 32 kHz */
HAL_DAC_Start_DMA(&hdac1, DAC_CHANNEL_1, (uint32_t *)sine_tbl, 32, DAC_ALIGN_12B_R);
HAL_TIM_Base_Start(&htim6);
```
DMA circular, half-word. Output frequency = trigger rate / table length. Follow with an RC or
active low-pass (reconstruction filter) to remove the staircase.

## Built-in generators
`HAL_DACEx_TriangleWaveGenerate` and `HAL_DACEx_NoiseWaveGenerate` (LFSR) add to the DHR value on
each trigger: cheap test signals, dither injection.

## Limits
- Settling time a few us for full-scale steps: max useful update rate ~1 Msps (buffered) on
  most parts; G4 has fast 15 Msps DACs (internal-only on some channels).
- DAC pin must be analog mode; the pin's ADC/comparator functions share it.

## Verify
- [ ] DC accuracy at several codes against a DMM (offset/gain errors noted).
- [ ] Sine output frequency and distortion checked on a scope/FFT.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.

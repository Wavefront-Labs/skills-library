---
id: computing-software.firmware-embedded-development.stm32.dual-adc-modes
name: dual-adc-modes
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-adc, dual-adc, simultaneous-sampling, interleaved-mode, adc-common-ccr, stm32, firmware-embedded-development]
level: advanced
status: gated
description: "Use STM32 dual ADC modes for simultaneous sampling of two signals (voltage and current) or interleaved mode to double sample rate, with common DMA and data packing."
sources:
  - https://www.st.com/resource/en/application_note/an3116-stm32s-adc-modes-and-their-applications-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0440-stm32g4-series-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dual ADC modes

Parts with ADC1+ADC2 sharing a common block (F4, F7, G4, L4 with ADC12, H7) can run them as
master/slave.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Modes
| Mode | Use |
|---|---|
| Regular simultaneous | sample V and I at the same instant (power metering, motor phase currents) |
| Injected simultaneous | same for injected groups (FOC current sampling) |
| Interleaved | ADC2 starts a fixed delay after ADC1 on the same channel: 2x sample rate |
| Alternate trigger | triggers alternate between ADCs |
| Combined modes | regular simultaneous + injected simultaneous etc. |

## Simultaneous with packed DMA
```c
ADC_MultiModeTypeDef mm = { .Mode = ADC_DUALMODE_REGSIMULT,
                            .DMAAccessMode = ADC_DMAACCESSMODE_12_10_BITS,   /* both results in one 32-bit word */
                            .TwoSamplingDelay = ADC_TWOSAMPLINGDELAY_1CYCLE };
HAL_ADCEx_MultiModeConfigChannel(&hadc1, &mm);
/* configure ADC2 channels (same count, same sampling times), then: */
HAL_ADC_Start(&hadc2);                                       /* slave first */
HAL_ADCEx_MultiModeStart_DMA(&hadc1, (uint32_t *)buf32, N);  /* master owns DMA */
/* buf32[i] low half = ADC1, high half = ADC2 */
```
Both ADCs need identical sequence length and matching sampling times in simultaneous mode,
or one waits for the other and timing skews.

## Interleaved
`ADC_DUALMODE_INTERL` with `TwoSamplingDelay` >= sampling time of a conversion; both on the same
channel. Effective rate doubles (e.g. 2 x 4 Msps on G4 = ~8 Msps). Gain/offset mismatch between
ADCs causes spurs at fs/2: calibrate both and correct offsets in software.

## Pitfalls
- Only the master's trigger is used; slave external triggers are ignored.
- HAL handles for both ADCs must be initialised; the slave's DMA setting must be off.
- F4 uses `ADC_CCR` MULTI bits (triple mode with ADC3 too); naming differs per series.

## Verify
- [ ] Same signal on both channels: ADC1 and ADC2 values agree within calibration error.
- [ ] Phase between V and I measured on a known load matches theory.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.

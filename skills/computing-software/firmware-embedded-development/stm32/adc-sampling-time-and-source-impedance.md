---
id: computing-software.firmware-embedded-development.stm32.adc-sampling-time-and-source-impedance
name: adc-sampling-time-and-source-impedance
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-adc, adc-sampling-time, source-impedance, adc-input-capacitor, sar-adc, stm32, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Choose STM32 ADC sampling time from source impedance and sample capacitor, add buffering or RC filters, and diagnose readings that depend on channel order."
sources:
  - https://www.st.com/resource/en/application_note/an2834-how-to-get-the-best-adc-accuracy-in-stm32-microcontrollers-stmicroelectronics.pdf
  - https://www.st.com/resource/en/datasheet/stm32f407vg.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sampling time and source impedance

A SAR ADC charges its internal sample capacitor (C_ADC, a few pF) through the source impedance
(R_AIN) plus the switch resistance (R_ADC). If sampling ends before the cap settles
within 1/2 LSB, readings are low and depend on what the previous channel was.

## Datasheet formula
R_AIN max = T_S / (f_ADC x C_ADC x ln(2^(N+2))) - R_ADC

The reference manual gives a table of the maximum R_AIN per sampling time and ADC clock; the
allowed impedance scales roughly with the sampling time (check the table for your part).

## Configure
```c
ADC_ChannelConfTypeDef c = { .Channel = ADC_CHANNEL_5, .Rank = ADC_REGULAR_RANK_1,
                             .SamplingTime = ADC_SAMPLETIME_247CYCLES_5 };   /* L4 naming */
HAL_ADC_ConfigChannel(&hadc1, &c);
```
Internal channels (VREFINT, temperature sensor) need long minimum sampling times
(several us, see datasheet `tS_vrefint`, `tS_temp`).

## High-impedance sources (dividers, sensors)
Options, in order:
1. Longer sampling time (cheapest, lowers max rate).
2. Capacitor at the pin (e.g. 10-100 nF): acts as a charge reservoir. C_ext >> C_ADC so each
   sample barely disturbs it, but the RC low-passes the signal: fine for slow signals like
   battery voltage (1 Mohm divider + 100 nF -> 0.1 s time constant).
3. Op-amp buffer (or the internal OPAMP on G4/L4 in follower mode).

## Symptom check
Convert the channel twice in a row after a channel at a very different voltage. If the first
reading differs from the second, sampling time is too short (crosstalk via residual charge).

## Verify
- [ ] Ghosting test (alternating 0 V / 3.3 V neighbour) shows < 1 LSB effect.
- [ ] Reading at the pin matches a DMM within the error budget.

## Checked

2026-10-31: Confirmed the RAIN/RADC/CADC source-impedance model and the tc = (RADC + RAIN) x CADC settling relation, including the 1/2 LSB criterion, from AN2834; `ADC_SAMPLETIME_247CYCLES_5` and the channel-config API from stm32l4xx_hal_adc.h; the on-chip OPAMP availability from stm32l476xx.h; the internal-channel minimum sampling times (tS_vrefint 4 us, tS_temp 5 us) from the STM32L476RG datasheet. Removed the C_ADC/R_ADC typical values and the F4 R_AIN table example figures (RM0090 and the table exceed the fetch size limit).

Method: documentation only; no commands were run.

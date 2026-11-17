---
id: computing-software.firmware-embedded-development.stm32.timer-encoder-interface
name: timer-encoder-interface
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-timer, encoder-mode, quadrature-encoder, x4-counting, index-pulse, position-overflow, velocity-estimation, rotary-encoder, firmware-embedded-development]
level: practitioner
status: gated
description: "Read quadrature encoders with STM32 timer encoder mode: x2/x4 counting, 16-bit overflow extension to 32/64-bit position, index pulses, filtering and velocity."
sources:
  - https://www.st.com/resource/en/application_note/an4776-generalpurpose-timer-cookbook-for-stm32-microcontrollers-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an4013-introduction-to-timers-for-stm32-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timer encoder interface

**Goal:** zero-CPU quadrature decoding of motor encoders and rotary knobs, with position
that never wraps unexpectedly and a clean speed estimate.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Setup
Encoder A and B to TIx_CH1 and CH2 of one timer. Encoder mode 3 counts on both edges of both
signals (x4 resolution):
```c
TIM_Encoder_InitTypeDef e = {
    .EncoderMode = TIM_ENCODERMODE_TI12,           /* x4 */
    .IC1Polarity = TIM_ICPOLARITY_RISING, .IC1Selection = TIM_ICSELECTION_DIRECTTI,
    .IC1Filter = 6,
    .IC2Polarity = TIM_ICPOLARITY_RISING, .IC2Selection = TIM_ICSELECTION_DIRECTTI,
    .IC2Filter = 6 };
htim3.Init.Period = 0xFFFF;
HAL_TIM_Encoder_Init(&htim3, &e);
HAL_TIM_Encoder_Start(&htim3, TIM_CHANNEL_ALL);
int16_t delta = (int16_t)(TIM3->CNT - last); last = TIM3->CNT;   /* signed 16-bit delta */
```
`TI1` or `TI2` alone gives x2. Swap polarity of one input (or A/B wires) to invert direction.
Counter direction is in `CR1.DIR`.

## Extending position beyond 16 bits
Read the counter periodically (faster than half a wrap at maximum speed) and accumulate the
**signed 16-bit difference** into a 32/64-bit position:
`max_speed_counts_per_s * read_period < 32768`. E.g. 10,000 rpm x 4096 counts/rev = 683k
counts/s needs reads at least every ~48 ms; use 1-10 ms. Or use a 32-bit timer (TIM2/TIM5),
or the update interrupt with direction to count wraps.

## Index pulse
Route the Z (index) signal to a capture channel or EXTI and capture/reset the count once per
revolution to correct for missed counts. Newer timers (G4, H7 TIM with `ECR.IE`) can reset the
counter on index in hardware.

## Filtering and noise
- Input filter (`ICxF`) rejects short glitches; motor encoders on long cables need it, plus
  differential line receivers (RS-422) for industrial encoders.
- Mechanical knobs bounce: filter 10-15 and a divide-by-4 in software for one count per detent.

## Velocity
- High speed: delta counts per fixed sample period.
- Low speed (few counts per period): measure time between edges with input capture on another
  timer, or use the encoder timer's capture on CH3/CH4 with a time base. Combine both methods
  by speed range.

## Verify
- [ ] One full revolution reads exactly CPR x 4 counts, both directions.
- [ ] Running at max speed for minutes: accumulated position matches index count.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.

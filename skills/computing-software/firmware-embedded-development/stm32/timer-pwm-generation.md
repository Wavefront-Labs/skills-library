---
id: computing-software.firmware-embedded-development.stm32.timer-pwm-generation
name: timer-pwm-generation
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-timer, pwm-generation, psc-arr-ccr, pwm-mode-1, center-aligned, preload-arpe, complementary-outputs, dead-time, moe-bit, firmware-embedded-development]
level: practitioner
status: gated
description: "Generate PWM on STM32 timers: PSC/ARR/CCR maths, edge vs centre-aligned, preload for glitch-free updates, advanced-timer MOE and dead-time for half bridges."
sources:
  - https://www.st.com/resource/en/application_note/an4776-generalpurpose-timer-cookbook-for-stm32-microcontrollers-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an4013-introduction-to-timers-for-stm32-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timer PWM generation (STM32)

**Goal:** PWM with the exact frequency and resolution needed, duty-cycle updates without
glitches, and safe complementary outputs for motor/power stages.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Frequency and resolution
```
f_pwm = f_timer_clk / ((PSC + 1) * (ARR + 1))      (edge-aligned)
duty   = CCRx / (ARR + 1)
```
Timer clock: on many STM32s, if the APB prescaler is not 1 the timer clock is **2x PCLK**;
check the clock tree. Maximise ARR for resolution: 20 kHz from 170 MHz with PSC = 0 gives
ARR = 8499 (13 bits). Centre-aligned mode halves the frequency for the same ARR
(`f = f_clk / (2 * (PSC+1) * ARR)`).

## Setup (HAL)
```c
htim1.Init.Prescaler = 0;
htim1.Init.Period = 8499;
htim1.Init.CounterMode = TIM_COUNTERMODE_UP;
htim1.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_ENABLE;   /* ARPE */
HAL_TIM_PWM_Init(&htim1);
TIM_OC_InitTypeDef oc = { .OCMode = TIM_OCMODE_PWM1, .Pulse = 4250,
                          .OCPolarity = TIM_OCPOLARITY_HIGH, .OCFastMode = TIM_OCFAST_DISABLE };
HAL_TIM_PWM_ConfigChannel(&htim1, &oc, TIM_CHANNEL_1);          /* sets OC1PE preload */
HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_1);
/* update duty: */ __HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_1, new_ccr);
```
With preload enabled (OCxPE, ARPE) new CCR/ARR values take effect at the next update event:
no runt pulses. Without it, writing a CCR below the current counter skips a pulse.

## Advanced timers (TIM1/TIM8/TIM20)
- Outputs stay off until **MOE** in `BDTR` is set (`HAL_TIM_PWM_Start` does it; register-level
  code forgets it, giving "PWM configured but no output").
- Complementary outputs CHxN with **dead time** (`BDTR.DTG`): for a half bridge, set dead time
  longer than the MOSFET driver's turn-off delay + fall time, e.g. 200-500 ns.
- **Break input** (BKIN) connected to an overcurrent comparator disables outputs in hardware
  within nanoseconds; configure off-state levels (OSSI/OSSR) so the bridge is safe.

## Gotchas
- PWM pin needs the right alternate function and speed; check AF table.
- 0 % and 100 % duty: CCR = 0 gives constant low, CCR > ARR gives constant high in PWM1 mode.
- Changing PSC on the fly applies only at the next update event; force with `EGR.UG` (which
  also resets the counter).
- Many duty updates per period (e.g. from an ISR racing the counter) need DMA burst
  (`TIMx->DCR/DMAR`) or careful update-interrupt timing.

## Verify
- [ ] Scope shows the computed frequency and duty at 0 %, 50 %, 100 %.
- [ ] Rapid duty changes produce no runt pulses (preload on).
- [ ] Dead time measured between high- and low-side gate signals.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.

---
id: computing-software.firmware-embedded-development.stm32.timer-one-pulse-mode
name: timer-one-pulse-mode
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-timer, one-pulse-mode, opm-bit, triggered-pulse, pulse-delay, repetition-counter, retriggerable-opm, firmware-embedded-development]
level: practitioner
status: gated
description: "Produce precisely timed single pulses or bursts with STM32 timer one-pulse mode: delay and width from CCR/ARR, external trigger start, repetition counter bursts."
sources:
  - https://www.st.com/resource/en/application_note/an4776-generalpurpose-timer-cookbook-for-stm32-microcontrollers-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timer one-pulse mode

**Goal:** a single pulse (or N pulses) of exact delay and width after a trigger, generated
entirely in hardware: triggering a camera, firing an ultrasonic burst, strobing an LED,
generating a sensor's reset pulse.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## How it works
With `CR1.OPM = 1` the counter stops at the next update event (counter clears `CEN`).
In PWM mode 2 on a channel:
```
delay  = CCRx / f_cnt
width  = (ARR - CCRx + 1) / f_cnt
```
Started by software (set `CEN`) or by a trigger input in slave **trigger mode** (external edge
on TI1/TI2 or another timer's TRGO), so latency from trigger edge to pulse is fixed and short.

## HAL setup (external trigger on TI2, pulse on CH1)
```c
htim.Init.Prescaler = 169;                 /* 1 MHz at 170 MHz */
htim.Init.Period = 1099;                   /* ARR */
HAL_TIM_OnePulse_Init(&htim, TIM_OPMODE_SINGLE);
TIM_OnePulse_InitTypeDef op = {
    .OCMode = TIM_OCMODE_PWM2, .Pulse = 100,           /* 100 us delay */
    .OCPolarity = TIM_OCPOLARITY_HIGH,
    .ICPolarity = TIM_ICPOLARITY_RISING, .ICSelection = TIM_ICSELECTION_DIRECTTI,
    .ICFilter = 0 };
HAL_TIM_OnePulse_ConfigChannel(&htim, &op, TIM_CHANNEL_1, TIM_CHANNEL_2);
HAL_TIM_OnePulse_Start(&htim, TIM_CHANNEL_1);         /* armed; waits for TI2 edge */
```
Result: 100 us after each rising edge on CH2 input, a 1000 us high pulse on CH1.

## Bursts
Advanced timers (TIM1/8) and some general-purpose ones have a **repetition counter** (`RCR`):
in one-pulse mode the timer runs RCR+1 periods before stopping, giving a burst of N pulses.

## Variants and gotchas
- Minimum delay is one count (CCR = 0 is not "no delay" in PWM2; use PWM1 with CCR = ARR+1
  tricks or check the cookbook for zero-delay configs).
- Re-triggering during a pulse is ignored in normal OPM; newer timers (G4, H7, L4+) have a
  **retriggerable OPM** mode (combined slave mode) that restarts the pulse on each trigger.
- Software start: `__HAL_TIM_ENABLE(&htim)` each time; the counter must have stopped (CEN=0).
- The output stays at the idle level between pulses: set polarity so idle is the safe state.

## Verify
- [ ] Scope with trigger signal and output: delay and width match within 1 count.
- [ ] Trigger jitter: output edge jitter vs input edge is within the timer clock resolution.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.

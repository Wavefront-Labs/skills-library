---
id: computing-software.firmware-embedded-development.stm32.timer-input-capture
name: timer-input-capture
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-timer, input-capture, pwm-input-mode, frequency-measurement, period-measurement, capture-overflow, icf-filter, dma-capture, firmware-embedded-development]
level: practitioner
status: gated
description: "Measure frequency, period and pulse width with STM32 timer input capture: PWM-input mode, overflow handling, input filters and DMA capture for high-rate signals."
sources:
  - https://www.st.com/resource/en/application_note/an4776-generalpurpose-timer-cookbook-for-stm32-microcontrollers-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timer input capture

**Goal:** timestamps of external edges with timer-clock resolution, for frequency, period,
duty cycle, or protocol decoding (IR, PPM, ultrasonic echo).

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Period / frequency with one channel
Capture on rising edges; period = difference between consecutive captures:
```c
void HAL_TIM_IC_CaptureCallback(TIM_HandleTypeDef *htim) {
    if (htim->Channel == HAL_TIM_ACTIVE_CHANNEL_1) {
        uint32_t now = HAL_TIM_ReadCapturedValue(htim, TIM_CHANNEL_1);
        uint32_t period = (now - last) & 0xFFFF;   /* 16-bit timer: mask the wrap */
        last = now;
        freq_hz = timer_clk_hz / period;
    }
}
```
Unsigned subtraction handles one counter wrap. Periods longer than one full counter range
need an overflow count from the update interrupt (and careful ordering when a capture and
update happen close together), or a 32-bit timer (TIM2/TIM5 on most STM32s), or a larger
prescaler.

## PWM input mode (period + duty in hardware)
Map TI1 to both CH1 (rising, direct) and CH2 (falling, indirect), and set the slave mode
controller to **reset mode** triggered by TI1FP1. Each rising edge resets the counter, so
`CCR1` = period and `CCR2` = high time, with no software subtraction:
```c
TIM_SlaveConfigTypeDef s = { .SlaveMode = TIM_SLAVEMODE_RESET, .InputTrigger = TIM_TS_TI1FP1 };
```
Works only on channels 1/2 (TI1/TI2).

## Input filter and prescaler
- `ICFilter` (0-15) requires N consecutive samples at f_DTS: rejects glitches and contact
  bounce; costs latency. Use 0 for clean digital signals, higher for noisy cables.
- `ICPrescaler` captures every 2/4/8 edges: measure high frequencies with fewer interrupts.

## High rates: DMA
At tens of kHz, an interrupt per edge burns CPU. Use `HAL_TIM_IC_Start_DMA` into a circular
buffer of timestamps and process in blocks (half/full transfer callbacks).

## Resolution and range
Resolution = 1/f_timer (e.g. 5.9 ns at 170 MHz). Choose PSC so the longest expected period
fits the counter (or use overflow counting) while keeping enough resolution for the shortest.
For very low frequencies, gate-count instead (count edges in a fixed time window).

## Verify
- [ ] Signal generator sweep: measured frequency error < 1 count across range.
- [ ] Glitch injection rejected with the chosen filter.
- [ ] Periods longer than one counter wrap measured correctly.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.

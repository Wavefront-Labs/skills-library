---
id: computing-software.firmware-embedded-development.stm32.timer-prescaler-and-arr-calculation
name: timer-prescaler-and-arr-calculation
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-timers, timer-prescaler, auto-reload, arr-psc-calculation, update-frequency, stm32, firmware-embedded-development]
level: practitioner
status: gated
description: "Compute STM32 timer PSC and ARR for exact update or PWM frequencies, handle 16 vs 32-bit counters, rounding and preload (ARPE) so changes don't glitch."
sources:
  - https://www.st.com/resource/en/application_note/an4013-introduction-to-timers-for-stm32-mcus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prescaler and ARR calculation

Update frequency:  f_upd = f_timclk / ((PSC + 1) x (ARR + 1))

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

`f_timclk` is the timer kernel clock (APB timer clock, x2 rule when APB prescaler > 1).

## Pick values
Maximise ARR for best resolution (PWM duty steps = ARR + 1), keep PSC as small as possible:
```c
/* returns 0 on success; 16-bit timer limits */
int timer_calc(uint32_t fclk, uint32_t fout, uint16_t *psc, uint16_t *arr) {
    uint64_t ticks = (fclk + fout / 2) / fout;          /* total counts per period, rounded */
    uint32_t p = (uint32_t)((ticks + 65535) / 65536);   /* smallest prescaler giving ARR <= 65535 */
    if (p == 0) p = 1;
    if (p > 65536) return -1;
    uint32_t a = (uint32_t)((ticks + p / 2) / p);
    if (a < 2) return -1;
    *psc = p - 1; *arr = a - 1;
    return 0;
}
```
Achieved frequency = fclk / (p x a); report the error. For exact results pick a timer clock that
divides cleanly (e.g. 1 MHz tick with PSC = fclk/1e6 - 1).

## 32-bit timers
TIM2 and TIM5 (on most series) have 32-bit ARR/CNT: PSC = 0 and ARR up to 2^32-1, great for long
periods with full resolution.

## Example
84 MHz timer clock, 20 kHz PWM: ticks = 4200, PSC = 0, ARR = 4199 -> duty resolution 4200 steps
(~12 bits). 50 Hz servo: ticks = 1,680,000 -> PSC = 25 (p=26), ARR = 64614; better use a 1 MHz
tick: PSC = 83, ARR = 19999, pulse in microseconds directly.

## Changing on the fly
- `ARPE = 1` (`TIM_AUTORELOAD_PRELOAD_ENABLE`): new ARR takes effect at the next update event,
  no glitch. Without preload, writing an ARR lower than the current CNT makes the counter run
  to 0xFFFF and wrap: one very long period.
- PSC is always preloaded: it applies at the next update. Force with `TIMx->EGR = TIM_EGR_UG`
  (also resets CNT and fires an update interrupt unless `URS` is set).
- `__HAL_TIM_SET_AUTORELOAD(&htim, arr)`, `__HAL_TIM_SET_PRESCALER(&htim, psc)`.

## Verify
- [ ] Frequency measured on scope within computed error.
- [ ] Period changes under load show no long or short glitch period.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.

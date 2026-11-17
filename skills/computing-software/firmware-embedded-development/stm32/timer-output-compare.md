---
id: computing-software.firmware-embedded-development.stm32.timer-output-compare
name: timer-output-compare
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-timers, output-compare, oc-toggle, ccr-interrupt, timed-events, stm32, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Generate precisely timed pulses and events with STM32 timer output compare: toggle/active/inactive modes, CCR updates in the ISR for multiple frequencies, and forced outputs."
sources:
  - https://www.st.com/resource/en/application_note/an4013-introduction-to-timers-for-stm32-mcus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0090-stm32f405415-stm32f407417-stm32f427437-and-stm32f429439-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Output compare

When CNT equals CCRx, the channel does something: set, clear, toggle the pin, or just raise an
interrupt/DMA request. Unlike PWM, each channel can generate a different timing on the same
free-running counter.

## Modes (`OCxM` in CCMRx)
| HAL mode | Behaviour |
|---|---|
| `TIM_OCMODE_TIMING` | no pin change, interrupt only (software timeouts) |
| `TIM_OCMODE_ACTIVE` / `INACTIVE` | set / clear on match |
| `TIM_OCMODE_TOGGLE` | toggle on match |
| `TIM_OCMODE_FORCED_ACTIVE` / `INACTIVE` | force pin now (manual override) |
| `TIM_OCMODE_PWM1/2` | PWM (see PWM skill) |

## Several frequencies on one timer
Free-running counter (ARR = 0xFFFF or 0xFFFFFFFF), each channel toggles and advances its CCR by
its half period in the interrupt:
```c
#define HALF1 500   /* ticks */
#define HALF2 730
void HAL_TIM_OC_DelayElapsedCallback(TIM_HandleTypeDef *h) {
    if (h->Channel == HAL_TIM_ACTIVE_CHANNEL_1)
        __HAL_TIM_SET_COMPARE(h, TIM_CHANNEL_1, __HAL_TIM_GET_COMPARE(h, TIM_CHANNEL_1) + HALF1);
    else if (h->Channel == HAL_TIM_ACTIVE_CHANNEL_2)
        __HAL_TIM_SET_COMPARE(h, TIM_CHANNEL_2, __HAL_TIM_GET_COMPARE(h, TIM_CHANNEL_2) + HALF2);
}
HAL_TIM_OC_Start_IT(&htim3, TIM_CHANNEL_1);
HAL_TIM_OC_Start_IT(&htim3, TIM_CHANNEL_2);
```
Unsigned wraparound of CCR + half is correct with ARR at the counter max. The ISR must run
before the next match, which bounds the shortest half period by interrupt latency (use DMA to
CCR for faster sequences).

## Preload
For this pattern, keep CCR preload **off** (`OCxPE = 0`, HAL `OCFastMode`/preload settings) so a
new CCR takes effect immediately. For PWM keep it on.

## Precise single delay
Start: read CNT, set CCR = CNT + delay, enable CCx interrupt or use ACTIVE mode on the pin.
Jitter is one timer tick plus nothing else: much better than software delays.

## Polarity and idle
`OCPolarity` inverts the output; on advanced timers (TIM1/8) set `MOE` (`__HAL_TIM_MOE_ENABLE`)
or the pins stay inactive. HAL_TIM_OC_Start does it for TIM1.

## Verify
- [ ] Scope: each channel's frequency and phase correct, no missed toggles at min period.
- [ ] Worst-case ISR latency measured below the shortest half period.

## Checked

2026-10-31: Confirmed `TIM_OCMODE_TIMING`/`ACTIVE`/`INACTIVE`/`TOGGLE`/`PWM1`/`PWM2` and the output-compare HAL API from stm32l4xx_hal_tim.h, with the LL equivalents in stm32l4xx_ll_tim.h.

Method: documentation only; no commands were run.

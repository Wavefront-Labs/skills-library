---
id: computing-software.firmware-embedded-development.stm32.timer-break-input
name: timer-break-input
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-timers, timer-break-input, bkin, moe-shutdown, motor-protection, bdtr, stm32, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Protect power stages with STM32 advanced-timer break inputs: BKIN/BKIN2 pins, comparator break sources, polarity and filtering, automatic output enable, and safe idle states."
sources:
  - https://www.st.com/resource/en/application_note/an4277-using-stm32-device-pwm-shutdown-features-for-motor-control-and-digital-power-conversion-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0440-stm32g4-series-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timer break input

Advanced timers (TIM1, TIM8, TIM20, plus TIM15-17 partly) have break inputs that force PWM
outputs to a safe state in hardware within tens of ns, independent of software. Essential for
overcurrent protection on inverters and SMPS.

## Configuration (BDTR)
```c
TIM_BreakDeadTimeConfigTypeDef b = {0};
b.OffStateRunMode = TIM_OSSR_ENABLE;          /* outputs driven to inactive level, not floating */
b.OffStateIDLEMode = TIM_OSSI_ENABLE;
b.DeadTime = 50;
b.BreakState = TIM_BREAK_ENABLE;
b.BreakPolarity = TIM_BREAKPOLARITY_LOW;      /* fault pin active low */
b.BreakFilter = 4;                            /* reject spikes; adds delay */
b.AutomaticOutput = TIM_AUTOMATICOUTPUT_DISABLE;   /* latch: software must re-enable */
b.Break2State = TIM_BREAK2_ENABLE;            /* G4/F3/L4/H7: second input */
b.Break2Polarity = TIM_BREAK2POLARITY_LOW;
HAL_TIMEx_ConfigBreakDeadTime(&htim1, &b);
```
On break: `MOE` clears, outputs go to idle states set by `OISx`/`OISxN` (`OCIdleState`,
`OCNIdleState` in the channel config). Choose idle levels so both high and low switches are off
(considering gate-driver polarity).

## Break sources
- BKIN pin (external comparator or gate-driver fault output).
- Internal comparators (G4/F3: COMPx output to break, `HAL_TIMEx_ConfigBreakInput`) for
  cycle-by-cycle current limiting without an external comparator.
- Clock security system failure and core lockup (system break, `SBIF`) always tied to break
  on many series.
- BKIN2 (where available) acts like BKIN but forces outputs to inactive regardless of OSSR,
  typically used for severe faults while BKIN handles cycle-by-cycle limits.

## Recovery
With `AutomaticOutput` disabled, `MOE` stays cleared until software sets it
(`__HAL_TIM_MOE_ENABLE`) after checking the fault is gone. Automatic output re-enables at the next
update event: use only for cycle-by-cycle limiting. The break interrupt (`HAL_TIMEx_BreakCallback`)
logs the event; clear `BIF` and check the input level before re-arming.

## Lock
`LockLevel` (`TIM_LOCKLEVEL_1..3`) freezes BDTR and polarity settings until reset, protecting
against runaway firmware. Set after configuration in production.

## Verify
- [ ] Inject a fault pulse: scope shows outputs off within datasheet delay plus filter.
- [ ] Debug halt does not leave switches on (combine with DBGMCU timer freeze settings).
- [ ] Re-arm only possible after fault cleared.

## Checked

2026-10-31: Confirmed the break-related fields and constants: `TIM_BDTR_MOE` and the BDTR lock levels `TIM_LOCKLEVEL_1..3` (stm32l4xx_hal_tim.h), the `TIM_CR2_OIS1..OIS4`/`OIS1N..` output-idle bits (CMSIS device headers) and the break filter/enable fields of `TIM_BreakDeadTimeConfigTypeDef` (stm32l4xx_hal_tim_ex.h).

Method: documentation only; no commands were run.

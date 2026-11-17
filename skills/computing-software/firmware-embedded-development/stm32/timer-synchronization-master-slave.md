---
id: computing-software.firmware-embedded-development.stm32.timer-synchronization-master-slave
name: timer-synchronization-master-slave
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-timer, timer-synchronization, trgo, itr, slave-mode, gated-mode, trigger-mode, adc-trigger, phase-shifted-pwm, firmware-embedded-development]
level: advanced
status: gated
description: "Chain STM32 timers and peripherals in hardware: master TRGO, slave reset/gated/trigger modes, ITR mapping, synchronous start and timer-triggered ADC sampling."
sources:
  - https://www.st.com/resource/en/application_note/an4776-generalpurpose-timer-cookbook-for-stm32-microcontrollers-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0440-stm32g4-series-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timer synchronisation (master/slave)

**Goal:** timers and ADCs that start, stop and sample in lockstep with zero software jitter:
synchronous multi-phase PWM, ADC sampling at a PWM centre, 32-bit timers from two 16-bit ones.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Master side
`TIMx_CR2.MMS` selects what goes out on **TRGO**: reset, enable, update event, compare pulse,
OCxREF. HAL:
```c
TIM_MasterConfigTypeDef m = { .MasterOutputTrigger = TIM_TRGO_UPDATE,
                              .MasterSlaveMode = TIM_MASTERSLAVEMODE_ENABLE };
HAL_TIMEx_MasterConfigSynchronization(&htim1, &m);
```
`MSM` (master/slave mode bit) delays the master slightly so slaves started by it are perfectly
aligned.

## Slave side
`SMCR.TS` picks the trigger input: **ITR0..ITRn** are internal connections from other timers'
TRGO. The mapping (e.g. "TIM3 ITR0 = TIM1 TRGO") is a table per family in the reference
manual: always look it up.
`SMCR.SMS` modes:
| Mode | Behaviour |
|---|---|
| Reset | trigger resets the counter (phase lock) |
| Gated | counter runs only while trigger is high |
| Trigger | trigger starts the counter (synchronous start) |
| External clock mode 1 | trigger edges clock the counter (prescaler/cascade) |
```c
TIM_SlaveConfigTypeDef s = { .SlaveMode = TIM_SLAVEMODE_TRIGGER, .InputTrigger = TIM_TS_ITR0 };
HAL_TIM_SlaveConfigSynchro(&htim3, &s);
```

## Recipes
- **Phase-shifted PWM:** master TIM1, slaves TIM8/TIM3 in reset mode on master update, with
  their CNT preloaded to different values, or use one advanced timer's channels with different
  compare values in combined/asymmetric PWM modes (G4/F3).
- **ADC sampled mid-PWM:** set ADC external trigger to `TIMx_TRGO` or `TIMx_CC4`, centre-aligned
  PWM with CC4 at the counter peak: current sampled when switching noise is lowest.
- **32-bit cascade:** master update event as TRGO, slave in external clock mode 1 on that ITR:
  slave counts master overflows.
- **Synchronous start of several timers:** slaves in trigger mode; enabling the master starts
  all with identical phase.

## Gotchas
- Slave timers must be configured and enabled (CEN for gated/reset modes; not for trigger mode)
  before the master starts.
- Changing MMS/SMS while running causes spurious triggers: configure everything, then start.
- ITR mapping differs between families and even between timers: copying code across families
  silently links the wrong timer.

## Verify
- [ ] Logic analyser shows slave edges aligned to master within one timer clock.
- [ ] ADC samples align with PWM centre (toggle a GPIO in the ADC EOC handler to check).

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.

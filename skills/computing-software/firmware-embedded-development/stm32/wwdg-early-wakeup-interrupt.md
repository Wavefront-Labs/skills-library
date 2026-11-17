---
id: computing-software.firmware-embedded-development.stm32.wwdg-early-wakeup-interrupt
name: wwdg-early-wakeup-interrupt
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-watchdog, wwdg-early-wakeup, ewi, wwdg-last-chance, fault-logging, stm32, firmware-embedded-development]
level: practitioner
status: gated
description: "Use the STM32 window watchdog early wakeup interrupt (EWI) to log state or reach a safe state just before a WWDG reset, without abusing it as a refresh."
sources:
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/user_manual/um1884-description-of-stm32l4l4-hal-and-lowlayer-drivers-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WWDG early wakeup interrupt

The WWDG counter counts down from up to 0x7F; reset happens when it passes 0x40 -> 0x3F (T6
clears). The early wakeup interrupt (EWI) fires when the counter reaches 0x40, one WWDG tick
before reset.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Time available
One tick = 4096 x 2^WDGTB / PCLK. At PCLK = 80 MHz, WDGTB = 3 (/8): 4096 x 8 / 80e6 = 410 us.
That is all the time the ISR has. Pick WDGTB for the time you need, then set the counter and
window for your refresh scheme.

## Setup
```c
hwwdg.Instance = WWDG;
hwwdg.Init.Prescaler = WWDG_PRESCALER_8;
hwwdg.Init.Window = 0x50;
hwwdg.Init.Counter = 0x7F;
hwwdg.Init.EWIMode = WWDG_EWI_ENABLE;
HAL_WWDG_Init(&hwwdg);
HAL_NVIC_SetPriority(WWDG_IRQn, 0, 0);          /* highest: must run before reset */
HAL_NVIC_EnableIRQ(WWDG_IRQn);

void HAL_WWDG_EarlyWakeupCallback(WWDG_HandleTypeDef *h) {
    backup_log(BKP_PC, last_task_id);            /* backup register or noinit RAM */
    safe_outputs();                               /* motor off, valves closed */
    /* do NOT refresh here */
}
```
The EWI flag is cleared by HAL in `HAL_WWDG_IRQHandler`. Note EWI can be enabled only once:
it can't be disabled by software until reset.

## Do not refresh from the EWI
Refreshing in the ISR defeats the watchdog: a main loop stuck forever would be "rescued" by the
interrupt every period. The EWI's job is diagnostics and safe state.

## Logging that survives the reset
- Backup registers (RTC/TAMP BKPxR) or a `.noinit` RAM section (linker section not zeroed by
  startup) with a magic word.
- Store PC of the interrupted context from the exception stack frame:
  `uint32_t *sp = (uint32_t *)__get_PSP() /* or MSP */; pc = sp[6];`
- On boot, check `RCC_FLAG_WWDGRST` and report the logged data.

## Interaction
If interrupts are globally disabled when the hang happens, the EWI never runs: the reset still
occurs, only diagnostics are lost. The highest NVIC priority helps only for normal masking.

## Verify
- [ ] Deliberate hang: EWI log present after reset, with the expected task/PC.
- [ ] Safe outputs reached within the EWI window (scope).

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.

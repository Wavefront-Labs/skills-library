---
id: computing-software.firmware-embedded-development.stm32.window-watchdog-wwdg
name: window-watchdog-wwdg
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [iwdg, wwdg, window-watchdog, early-wakeup-interrupt, watchdog-timeout-calculation, stm32, firmware-embedded-development]
level: practitioner
status: gated
description: "Configure the STM32 window watchdog (WWDG) to catch code that runs too slow or too fast, compute its timing from PCLK, use the early-wakeup interrupt, and pair it with the IWDG."
sources:
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an4435-guidelines-for-obtaining-ulcsaiec-607301-and-603351-class-b-certification-in-any-stm32-application-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Window watchdog (WWDG)

## IWDG vs WWDG
| | IWDG | WWDG |
|---|---|---|
| Clock | LSI (independent, ~32 kHz, +-several %) | PCLK (APB) |
| Detects | code stopped refreshing (hang) | refresh too late **or too early** |
| Survives main clock failure | yes | no |
| Early warning interrupt | no (some series: yes, IWDG EWI on newer parts) | yes (EWI) |
| Runs in Stop/Standby | yes (unless frozen by option bytes) | no (clock stops) |
Safety standards (IEC 60730 Class B) commonly use both: IWDG for clock-independent hang
detection, WWDG for program-flow timing.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## How WWDG works
A 7-bit down-counter (T[6:0]) clocked by `PCLK / 4096 / 2^WDGTB`.
- Reset when the counter goes from 0x40 to 0x3F (bit T6 clears): too late.
- Reset when you refresh while the counter is **above the window value W**: too early.
- Valid refresh window: counter between W and 0x40.

Timing:
```
t_tick   = 4096 * 2^WDGTB / f_PCLK
timeout  = t_tick * (T[5:0] + 1)          /* from refresh to reset */
too_early_until = t_tick * (T - W)         /* refresh before this -> reset */
```
Example: PCLK = 80 MHz, WDGTB = 3 (prescaler 8): t_tick = 409.6 us. T = 0x7F gives a timeout of
64 x 409.6 us = 26.2 ms. W = 0x5F means refreshes in the first (0x7F-0x5F) x 409.6 us = 13.1 ms
cause a reset. So the valid window is 13.1-26.2 ms after each refresh.

## HAL setup
```c
WWDG_HandleTypeDef hwwdg = {
    .Instance = WWDG,
    .Init = { .Prescaler = WWDG_PRESCALER_8, .Window = 0x5F,
              .Counter = 0x7F, .EWIMode = WWDG_EWI_ENABLE },
};
HAL_WWDG_Init(&hwwdg);                  /* starts it: can't be stopped except by reset */
/* periodic task / loop with a period inside the window: */
HAL_WWDG_Refresh(&hwwdg);
```
Early wakeup interrupt fires at counter 0x40, one tick before reset:
```c
void HAL_WWDG_EarlyWakeupCallback(WWDG_HandleTypeDef *h) {
    save_fault_context_to_noinit(FAULT_WWDG);   /* ~one tick of time: keep it tiny */
}
```
Don't refresh from the EWI to "save" the system; that defeats the purpose.

## Where to refresh
In a place whose timing proves the main loop or control task is running at the right rate,
typically the end of the periodic control cycle. With an RTOS, combine with per-task
supervision (see multi-task-watchdog-supervision).

## Gotchas
- PCLK changes (low-power run, clock fallback via CSS) change the window. Recompute or
  reconfigure after clock switches.
- Debug: halting the core lets WWDG reset the board unless frozen (see freezing-watchdogs-in-debug).
- Stop mode: WWDG stops with the clock and continues after wake, so a refresh window can be
  violated right after wake. Refresh immediately after wake if your timing allows.
- Hardware WWDG option byte (`WWDG_SW` = 0) starts it automatically at reset on some series.

## Verify
- [ ] Deliberately refresh too early and too late in a test build: both cause a WWDG reset (`WWDGRSTF`).
- [ ] EWI handler records the fault and it is reported after reboot.
- [ ] Window numbers recomputed for every PCLK configuration the product uses.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.

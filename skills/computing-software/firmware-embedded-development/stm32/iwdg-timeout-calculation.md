---
id: computing-software.firmware-embedded-development.stm32.iwdg-timeout-calculation
name: iwdg-timeout-calculation
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-watchdog, iwdg-timeout, iwdg-prescaler, lsi-tolerance, watchdog-refresh, stm32, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Compute STM32 IWDG prescaler and reload for a target timeout, account for LSI tolerance across temperature, and place refreshes so the timeout catches real hangs."
sources:
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/datasheet/stm32l476rg.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IWDG timeout calculation

timeout = (4 x 2^PR) x (RLR + 1) / f_LSI

PR = 0..6 (prescaler /4 .. /256), RLR = 0..4095 (12 bits).

## LSI tolerance dominates
LSI is a low-accuracy RC: nominal 32 kHz on most series (40 kHz on F0/F1/F3), with datasheet
min/max such as 29.5-34 kHz (L4) or 17-47 kHz (F4). Design both ends:
- Fastest LSI gives the **shortest** timeout: refresh interval must be shorter than that.
- Slowest LSI gives the **longest** timeout: detection latency of a hang.

## Example (L4, 1 s target)
PR = 3 (/32): tick = 32 / 32000 = 1 ms nominal. RLR = 999 -> 1.000 s nominal.
At LSI max 34 kHz: 32 x 1000 / 34000 = 0.94 s. Refresh at least every 0.5 s for margin.
At LSI min 29.5 kHz: 1.08 s worst-case detection.

```c
hiwdg.Instance = IWDG;
hiwdg.Init.Prescaler = IWDG_PRESCALER_32;
hiwdg.Init.Reload = 999;
hiwdg.Init.Window = IWDG_WINDOW_DISABLE;     /* window option on newer series */
HAL_IWDG_Init(&hiwdg);                        /* starts the watchdog */
/* main loop */
HAL_IWDG_Refresh(&hiwdg);
```

## Measure the actual LSI
On many parts, LSI can be routed to a timer input-capture channel to measure it against the
HSE (see the timer input-selection options in your reference manual), then compute RLR for the
real frequency. Useful when the timeout needs to be tight.

## Where to refresh
Refresh from one place that only runs when the system is healthy (main loop after all checks, or
a supervisor task that verifies other tasks' heartbeats), never from a timer ISR: ISRs keep
running when the main loop deadlocks.

## Long operations
Flash mass erase (seconds), long blocking init: refresh inside the loop or select a longer
timeout during init and shorten it after (RLR can be rewritten; PR/RLR updates take effect after
the `PVU`/`RVU` flags clear).

## Verify
- [ ] Deliberate hang resets within the computed max timeout.
- [ ] No spurious resets across the temperature range (LSI fast corner).

## Checked

2026-10-31: Confirmed the LSI ranges 29.5-34 kHz (STM32L476RG datasheet), 17-47 kHz with 32 kHz typical (STM32F407VG datasheet) and 40 kHz typical on F1 (STM32F103C8 datasheet); `IWDG_SR_PVU`/`RVU` and the IWDG register structure from stm32l476xx.h; `HAL_IWDG_Init`/`Refresh`, `IWDG_PRESCALER_32`, `IWDG_WINDOW_DISABLE` from stm32l4xx_hal_iwdg.h. Rewrote the LSI-measurement note to drop unverified timer remap channel names (now points at the RM's timer input-selection section); the worked example numbers follow from the confirmed formula and ranges.

Method: documentation only; no commands were run.

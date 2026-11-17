---
id: computing-software.firmware-embedded-development.low-power-design.low-power-timer-lptim
name: low-power-timer-lptim
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [wake-source, lptim, low-power-timer, tickless-timebase, pulse-counting-in-stop, lse, arr-cmp-update, firmware-embedded-development]
level: advanced
status: draft
description: "Use the STM32 LPTIM (or similar low-power timer) as a Stop-mode wake timer, a tickless RTOS timebase and a pulse counter that runs while the CPU sleeps."
sources:
  - https://www.st.com/resource/en/application_note/an4865-lowpower-timer-lptim-applicative-use-cases-on-stm32-mcus-and-mpus-stmicroelectronics.pdf
  - https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/12-Low-power-support/01-Tickless-idle-mode
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Low-power timer (LPTIM)

**Goal:** sub-second wake timing and event counting in Stop mode, where normal TIMx timers
are unclocked.

## What LPTIM gives you
- 16-bit counter clocked from LSE/LSI/HSI or an **external pin** (counts pulses with no clock
  at all in asynchronous mode: flow meters, anemometers, reed switches while asleep).
- Runs in Stop 0/1/2 (check per instance: on L4, LPTIM1 runs in Stop 2, LPTIM2 only to
  Stop 1).
- Wakes on compare match (`CMPM`), auto-reload match (`ARRM`) or external trigger.

## Wake timer at 1 ms resolution
LSE 32768 Hz / prescaler 32 = 1024 Hz: ~0.98 ms ticks, 64 s max interval at 16 bits.
```c
HAL_LPTIM_TimeOut_Start_IT(&hlptim1, 0xFFFF, ticks);   /* period, timeout compare */
/* or one-shot: HAL_LPTIM_SetOnce_Start_IT(&hlptim1, period, pulse) */
HAL_PWREx_EnterSTOP2Mode(PWR_STOPENTRY_WFI);
```

## As a tickless RTOS timebase
SysTick stops in Stop mode, so FreeRTOS tickless idle with deep sleep needs a timer that runs
there. Pattern for `portSUPPRESS_TICKS_AND_SLEEP` (FreeRTOS) or a Zephyr timer driver:
1. Compute the expected idle time in ticks, clamp to the 16-bit range.
2. Program LPTIM compare, enter Stop.
3. On wake, read `LPTIM->CNT` (read twice until equal: asynchronous clock domain) to get
   elapsed time, call `vTaskStepTick(elapsed)`.
Zephyr ships this as `CONFIG_STM32_LPTIM_TIMER=y` with LSE.

## Gotchas
- **Register writes are asynchronous:** after writing `CMP` or `ARR`, wait for `CMPOK` /
  `ARROK` before the next write or before sleeping; writing twice too fast is silently lost.
- **ARR and CMP can only be written while the timer is enabled** (`ENABLE` bit set) on most
  STM32 LPTIMs, which is the opposite of TIMx.
- **Counter read** needs the double-read because of the clock crossing.
- **LSI drift** (+/-5 %) makes a tickless kernel's time drift; use LSE.
- External pulse counting with glitch filter needs a clock; with no clock enable only the
  asynchronous counter mode (no filter) works: add hardware RC filtering.

## Verify
- [ ] 1000 x 100 ms sleeps measured on a GPIO: total within LSE tolerance.
- [ ] RTOS tick count after a 60 s idle matches wall time within a tick.
- [ ] Pulse counter matches a signal generator count while the CPU stays in Stop.

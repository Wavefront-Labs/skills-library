---
id: computing-software.firmware-embedded-development.freertos.software-timers-and-tickless-idle
name: software-timers-and-tickless-idle
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [freertos, software-timer, xtimercreate, timer-service-task, tickless-idle, configuse-tickless-idle, portsuppressticksandsleep, low-power-rtos, idle-hook, timer-command-queue, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Use FreeRTOS software timers without stalling the timer service task, and enable tickless idle so the RTOS sleeps between events instead of waking every tick for nothing."
sources:
  - https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/06-Software-timers/01-RTOS-software-timer
  - https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Low-power-tickless/01-RTOS-low-power-support
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FreeRTOS software timers and tickless idle

**Goal:** use software timers without silently starving other timers, and
enable tickless idle so a sleeping system doesn't burn power waking up every
tick for nothing — connects directly to
`computing-software.firmware-embedded-development.low-power-design.current-profiling-and-duty-cycle-budget`'s
measured-current approach, from the RTOS-configuration side.

## Software timers run on one shared task
`xTimerCreate`/`xTimerStart` don't run the callback in an ISR or a dedicated
task per timer — every software timer's callback executes on a single,
shared **Timer Service Task**. This means:
- A slow or blocking timer callback delays every *other* timer due to fire
  after it, because they all funnel through one task. A timer callback must be
  short and non-blocking, same discipline as an ISR's top half.
- The timer command queue (`configTIMER_QUEUE_LENGTH`) can fill up if timers
  are started/stopped/reset faster than the service task drains commands;
  `xTimerStart` etc. then either block (if called with a wait) or fail —
  check return values, don't assume timer commands always succeed.
- Timer Service Task priority (`configTIMER_TASK_PRIORITY`) determines whether
  timers fire promptly under load from higher-priority application tasks —
  set it appropriately for how time-sensitive the timers actually need to be,
  not left at a default that may starve them under a busy system.

## Tickless idle: sleeping between events instead of every tick
By default, FreeRTOS wakes every tick (commonly 1ms) even when nothing is
scheduled to happen, because the tick interrupt itself is what the scheduler
uses to track time — this alone can prevent deep sleep modes that need long
uninterrupted periods. `configUSE_TICKLESS_IDLE = 1` lets the idle task, when
nothing is due to run, compute how long until the next scheduled event
(timer expiry, task delay) and suppress the tick interrupt for that duration
via a port-specific `portSUPPRESS_TICKS_AND_SLEEP()`, entering a low-power
sleep mode for the gap instead of waking every tick to do nothing.

## Pitfalls specific to tickless idle
- **Time drift during sleep**: the port's tickless implementation must
  reconcile the RTOS tick count with however long the MCU actually slept
  (often measured by a separate low-power timer/RTC that keeps running during
  sleep) — a port implementation that doesn't correct for this makes
  `vTaskDelay`-based timing drift relative to wall-clock time the longer/more
  often the system sleeps.
- **Minimum sleep threshold** (`configEXPECTED_IDLE_TIME_BEFORE_SLEEP`): very
  short idle gaps aren't worth the sleep-entry/exit overhead; tune this rather
  than accepting the default blindly for a specific MCU's wake latency.
- **A peripheral needing periodic servicing faster than the tick** (e.g. a
  watchdog that must be kicked more often than the longest tickless sleep
  period) can be defeated by tickless idle unless it's accounted for in the
  "how long can I sleep" calculation — check the port's implementation covers
  this, or cap the maximum tickless sleep duration.
- Tickless idle changes the power-measurement picture entirely: re-profile
  current draw after enabling it, don't assume the gain matches a datasheet
  number without measuring on the actual board (per
  `computing-software.firmware-embedded-development.low-power-design.current-profiling-and-duty-cycle-budget`).

## Verify
- [ ] No software timer callback blocks or runs long; timer service task priority matches real timing requirements.
- [ ] Timer command queue depth is sized for the actual start/stop/reset rate, and `xTimerStart`/`xTimerStop` return values are checked under load.
- [ ] Tickless idle is enabled and measured current draw during idle periods actually drops versus non-tickless, confirmed on a scope/profiler, not assumed.
- [ ] Long-run soak test confirms `vTaskDelay`-based timing doesn't drift against a wall clock after extended tickless sleep periods.

## Checked
2026-11-01. Confirmed in FreeRTOS-Kernel include/FreeRTOS.h: `configTIMER_TASK_PRIORITY` is required when timers are on,
`portSUPPRESS_TICKS_AND_SLEEP`, `configEXPECTED_IDLE_TIME_BEFORE_SLEEP` and `configUSE_TICKLESS_IDLE` exist. The
timer-service-task and command-queue behaviour is the documented design; the rest is engineering guidance.
Method: documentation only; no commands were run.

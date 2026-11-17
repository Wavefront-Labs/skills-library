---
id: computing-software.firmware-embedded-development.freertos.periodic-tasks-with-vtaskdelayuntil
name: periodic-tasks-with-vtaskdelayuntil
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [xtaskcreate, vtaskdelayuntil, xtaskdelayuntil, periodic-task, drift-free-timing, deadline-overrun, freertos, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Run a FreeRTOS task at a fixed, drift-free rate with vTaskDelayUntil/xTaskDelayUntil, and detect and handle overruns instead of bursting to catch up."
sources:
  - https://www.freertos.org/Documentation/02-Kernel/04-API-references/02-Task-control/02-vTaskDelayUntil
  - https://www.freertos.org/Documentation/02-Kernel/04-API-references/02-Task-control/01-vTaskDelay
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Periodic tasks with vTaskDelayUntil

**Goal:** a control loop or sampler that runs every N ms with no cumulative drift.

## Why not vTaskDelay
`vTaskDelay(10)` blocks 10 ticks **from now**, so the period is 10 ticks + execution time +
preemption. Over hours this drifts. `vTaskDelayUntil` blocks until an **absolute** tick:
the previous wake time plus the period.

## Pattern
```c
/* INCLUDE_xTaskDelayUntil 1 (older configs used INCLUDE_vTaskDelayUntil; defining both is an #error) */
static void vControlTask(void *arg)
{
    const TickType_t period = pdMS_TO_TICKS(10);
    TickType_t last = xTaskGetTickCount();      /* initialise ONCE, before the loop */
    for (;;) {
        BaseType_t on_time = xTaskDelayUntil(&last, period);
        if (on_time == pdFALSE) {
            overruns++;                          /* we were already late: no block happened */
            last = xTaskGetTickCount();          /* re-phase instead of bursting */
        }
        run_control_step();
    }
}
```
`last` is updated in place by the call. Re-initialising it inside the loop turns it back into
a relative delay.

## Overrun behaviour (the important part)
If the work overran so that `last + period` is already in the past, the call returns
immediately and still advances `last` by **one** period. After a 50 ms stall a 10 ms loop then
runs about five iterations back to back to catch up. For a PID loop that burst is usually
worse than skipping. Decide per task:
- **Catch up** (keep the call as it is): right for counters and integrators that must see every
  sample.
- **Re-phase** (reset `last` as above): right for control and sensing, where stale samples
  are useless.

`vTaskDelayUntil` (void) can't tell you it was late; use `xTaskDelayUntil` where available,
or compare `xTaskGetTickCount()` against `last` yourself.

## Resolution limits
- Period resolution is one tick. 1 kHz tick allows 1 ms steps; a 2.5 ms period is not possible.
  For sub-tick periods use a hardware timer interrupt plus a task notification.
- Jitter = time spent waiting for higher-priority tasks/ISRs after the wake tick. Give
  hard-periodic tasks high priority (rate-monotonic-priority-assignment).
- `pdMS_TO_TICKS` truncates. With a 100 Hz tick, `pdMS_TO_TICKS(15)` is 1 tick.

## Verify
- [ ] Toggle a GPIO at the top of the loop and confirm period and jitter on a scope or logic analyser.
- [ ] Inject a deliberate 5x-period stall and confirm the chosen overrun policy (burst vs re-phase).
- [ ] Overrun counter is exported to logs/telemetry.

## Checked

2026-11-01. Confirmed against FreeRTOS-Kernel tasks.c and include/FreeRTOS.h: `xTaskDelayUntil` is guarded by `INCLUDE_xTaskDelayUntil`, `INCLUDE_vTaskDelayUntil` is the older name and defining both is a #error. Clarified that line.
Method: documentation only; no commands were run.

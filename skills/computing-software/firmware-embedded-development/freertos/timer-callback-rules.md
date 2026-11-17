---
id: computing-software.firmware-embedded-development.freertos.timer-callback-rules
name: timer-callback-rules
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [timer-callback, timer-service-task, configtimer-task-priority, configtimer-queue-length, freertos, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Write FreeRTOS software timer callbacks that never block, size the timer task priority, stack and command queue, and diagnose late or missing timer expiries."
sources:
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/timers.c
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/timers.h
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/FreeRTOS.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timer callback rules

All software-timer callbacks run **in the timer service (daemon) task**, one after another.
Any delay in one callback delays every other timer and every `xTimerPendFunctionCall`.

```c
static void vLedTimerCb(TimerHandle_t t)
{
    (void)t;
    HAL_GPIO_TogglePin(LED_GPIO_Port, LED_Pin);   /* short, non-blocking */
}
```

## Callback rules
- Never call anything that blocks with a non-zero timeout: no `vTaskDelay`, no
  `xQueueReceive(.., portMAX_DELAY)`, no `xSemaphoreTake` that can wait. Use timeout 0.
- Keep work short; hand longer work to a task with a notification or queue send (timeout 0).
- Timer API calls from inside a callback (e.g. `xTimerChangePeriod`) must use block time 0:
  the callback runs in the task that services the command queue, so it would wait on itself.
- Callbacks are task context, not ISR context: use the normal (non-FromISR) APIs.

## Daemon task configuration
```c
#define configUSE_TIMERS              1
#define configTIMER_TASK_PRIORITY     (configMAX_PRIORITIES - 1)   /* or just above app tasks */
#define configTIMER_QUEUE_LENGTH      10
#define configTIMER_TASK_STACK_DEPTH  (configMINIMAL_STACK_SIZE * 2)
```
- **Priority:** if lower than busy application tasks, expiries are late by however long those
  tasks run. High priority gives accurate timers but callbacks then preempt the application.
- **Queue length:** commands (`xTimerStart`, `Stop`, `Reset`, `PendFunctionCall`) from tasks and
  ISRs go through this queue. If ISRs restart timers in bursts, size it for the burst; a full
  queue makes `xTimerStartFromISR` return `pdFAIL`.
- **Stack:** the deepest callback sets it. Check with
  `uxTaskGetStackHighWaterMark(xTimerGetTimerDaemonTaskHandle())`.

## Diagnosing late or missing expiries
- Late: timer task priority too low, or one callback runs long. Toggle a GPIO in each callback
  and look at it on a scope or logic analyser.
- Missing: start command failed (queue full, return value ignored), or the timer was started
  before the scheduler and the queue overflowed. Check every `xTimer*` return.
- Drift on auto-reload: none by design (next expiry is computed from the previous one), unless
  callbacks take longer than the period.

## Verify
- [ ] No blocking calls in any callback (grep callbacks for `portMAX_DELAY`, `vTaskDelay`).
- [ ] Timer daemon stack high-water mark checked under load.
- [ ] All `xTimer*` return values handled.

## Checked

2026-10-28: confirmed against the FreeRTOS-Kernel sources and headers read this batch: timer daemon task and command queue (`configTIMER_QUEUE_LENGTH`, statically created queue), `configTIMER_TASK_PRIORITY` and `configTIMER_TASK_STACK_DEPTH` must be defined with `configUSE_TIMERS`, `xTimerGetTimerDaemonTaskHandle`, `INCLUDE_xTimerPendFunctionCall`, ISR start can fail when the command queue is full, auto-reload next-expiry calculation (timers.c, timers.h, FreeRTOS.h). Removed or rewritten: nothing removed; only the dead freertos.org sources were replaced.
Method: documentation only; no commands were run.

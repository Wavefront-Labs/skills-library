---
id: computing-software.firmware-embedded-development.freertos.deadlock-avoidance
name: deadlock-avoidance
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [deadlock-avoidance, lock-ordering, mutex-timeout, xsemaphoregetmutexholder, deadly-embrace, freertos, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Prevent and diagnose deadlocks in FreeRTOS firmware: global lock ordering, bounded timeouts, no blocking while holding locks, and finding the cycle on a live target."
sources:
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/semphr.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/FreeRTOS.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/task.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/queue.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel-Book/blob/main/ch08.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deadlock avoidance

A deadlock needs all four Coffman conditions: mutual exclusion, hold-and-wait, no preemption
of locks, and a circular wait. Remove any one and it can't happen. In firmware the practical
levers are hold-and-wait and circular wait.

## 1. Global lock order (breaks circular wait)
Number every mutex and always take them in ascending order:
```c
/* lock_order.h: the single source of truth */
enum { LOCK_I2C = 10, LOCK_SPI_FLASH = 20, LOCK_FS = 30, LOCK_NET = 40 };
```
Task A taking `FS` then `I2C` while task B takes `I2C` then `FS` is the classic deadly
embrace. In debug builds, wrap take/give to record held levels per task (thread-local via
`vTaskSetThreadLocalStoragePointer`, which needs `configNUM_THREAD_LOCAL_STORAGE_POINTERS`
above 0) and `configASSERT(new_level > max_held)`.

## 2. Don't block while holding a lock (breaks hold-and-wait)
- No `xQueueReceive(..., portMAX_DELAY)`, `vTaskDelay`, or waits on another task while a mutex
  is held.
- Don't call unknown callbacks while holding a lock: they may lock something else.
- Copy the data out, release, then do slow work.

## 3. Bounded timeouts instead of portMAX_DELAY
```c
if (xSemaphoreTake(fs_lock, pdMS_TO_TICKS(500)) != pdTRUE) {
    TaskHandle_t h = xSemaphoreGetMutexHolder(fs_lock);   /* needs INCLUDE_xSemaphoreGetMutexHolder 1 */
    LOG_ERR("fs_lock timeout, held by %s", h ? pcTaskGetName(h) : "?");
    return -EBUSY;
}
```
Timeouts turn a silent hang into a logged, recoverable error and point at the holder. Size
them well above worst-case hold time so they only fire on real faults.

## 4. One owner instead of shared locks
A gatekeeper task (see gatekeeper-tasks) owns the resource and serialises requests through a
queue, so there is no mutex to deadlock on.

## FreeRTOS-specific traps
- **Timer daemon**: timer callbacks run in the daemon task and must not block; a callback
  that waits on a lock held by a task that is itself waiting on the timer command queue
  stalls every timer.
- **Scheduler suspended**: blocking with a non-zero timeout while the scheduler is suspended
  trips an assert in queue.c.
- **Self-deadlock**: re-taking a non-recursive mutex in a nested call (see recursive-mutexes).
- Priority inheritance does **not** resolve deadlocks; the Kernel Book says it only lessens the
  effect of priority inversion.

## Diagnosing on a live target
1. Halt and open a kernel-aware debugger view, or run a `vTaskListTasks` dump (needs
   `configUSE_TRACE_FACILITY` and `configUSE_STATS_FORMATTING_FUNCTIONS`): look for two or more
   tasks Blocked that should be running.
2. Register the mutexes with `vQueueAddToRegistry` so a debugger can name them, and map holders
   with `xSemaphoreGetMutexHolder`. The cycle is the bug.
3. A trace recording shows the take order leading up to the hang.

## Verify
- [ ] Lock order table exists and the debug-build assertion is on in CI.
- [ ] grep: no `portMAX_DELAY` takes on mutexes in application code (or each one justified).
- [ ] Soak test with randomised task timing (vary priorities and delays) runs 24 h without a timeout log.

## Checked

Checked 2026-10-25 against FreeRTOS-Kernel V11.3.2 (History.txt, released 16 October 2026, current main) and the FreeRTOS Kernel Book source. Confirmed: xSemaphoreGetMutexHolder is gated by INCLUDE_xSemaphoreGetMutexHolder (derived from INCLUDE_xQueueGetMutexHolder, default 0) and configNUM_THREAD_LOCAL_STORAGE_POINTERS defaults to 0 (FreeRTOS.h); vTaskListTasks needs configUSE_TRACE_FACILITY and configUSE_STATS_FORMATTING_FUNCTIONS (task.h); vQueueAddToRegistry covers queues, semaphores and mutexes (queue.h); queue.c asserts against blocking while the scheduler is suspended; Kernel Book 8.3.3/8.3.4 on inheritance and deadlock. Removed named trace tools and the claim that a timer callback deadlock drains no queue. 
Method: documentation only; no commands were run.

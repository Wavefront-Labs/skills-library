---
id: computing-software.firmware-embedded-development.freertos.task-starvation-and-idle-task
name: task-starvation-and-idle-task
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [freertos-scheduler, task-starvation, idle-task, vapplicationidlehook, idle-starvation, event-driven-design, freertos, firmware-embedded-development]
level: practitioner
status: draft
description: "Detect and fix task starvation in FreeRTOS, including a starved idle task, using run-time stats, idle-fed watchdogs and event-driven task design."
sources:
  - https://www.freertos.org/Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book
  - https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/15-Idle-task
  - https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Task starvation and the idle task

FreeRTOS has no priority aging. A ready task runs only when no higher-priority task is ready.
If a higher-priority task never blocks, everything below it, including the idle task, starves
**forever**.

## Why a starved idle task matters
The idle task (priority `tskIDLE_PRIORITY` = 0) does real work:
- frees TCBs and stacks of tasks that deleted themselves (memory leak if starved);
- runs `vApplicationIdleHook` (often your low-power entry or background checks);
- is where tickless idle enters sleep (no idle means no sleep and battery drain).

## Symptoms
- Heap slowly shrinks while tasks are created/deleted.
- Low-priority tasks (logging, UI) freeze while high ones look fine.
- Power consumption high; tickless idle never triggers.
- Run-time stats show `IDLE` at 0%.

## Detect
```c
/* configGENERATE_RUN_TIME_STATS 1 */
vTaskGetRunTimeStatistics(buf, sizeof buf);   /* look for IDLE ~0%, one task ~100% */
```
- **Idle-fed watchdog:** set a flag in the idle hook; a monitor (or the hardware watchdog
  feeder) checks it. If idle hasn't run in N ms, something is spinning. ESP-IDF does exactly
  this with its idle-task watchdog.
- Per-task check-in counters for watchdog supervision of every task.

## Causes and fixes
| Cause | Fix |
|---|---|
| Polling loop: `while (!flag) {}` | block on a notification/semaphore set by the ISR |
| `vTaskDelay(0)` or `taskYIELD()` "to be nice" | only yields to **equal** priority; block with a real delay or event |
| High-priority task does long processing | split: high-priority task captures, lower one processes |
| Retry loops without delay on errors | add backoff (`vTaskDelay`) in error paths |
| Busy-wait for hardware (`while(!(SR & TXE))`) | interrupt or DMA completion plus notification |
| Priority-0 app task in a tight loop with `configIDLE_SHOULD_YIELD 0` | block, or give it priority 1 with real blocking |

## Idle hook rules
```c
/* configUSE_IDLE_HOOK 1 */
void vApplicationIdleHook(void) {
    idle_alive = 1;          /* for the monitor */
    /* never block here; no vTaskDelay, no queue waits */
}
```
If an idle hook blocks, the system can end up with no ready task, which the kernel doesn't allow.

## Design rule
Every task's main loop must contain a **blocking call with a real wait** on its normal path.
Review: for each task, name the call where it blocks and what wakes it.

## Verify
- [ ] Run-time stats under peak load show IDLE above 0% (target 20%+ headroom).
- [ ] Idle-alive monitor trips in a test build with an injected busy loop.
- [ ] Create/delete soak test shows stable free heap.

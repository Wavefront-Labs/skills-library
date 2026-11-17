---
id: computing-software.firmware-embedded-development.freertos.task-state-dumps
name: task-state-dumps
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [freertos-debugging, vtasklist, vtasklisttasks, etaskgetstate, task-state, blocked-task-diagnosis, cli-ps-command, freertos, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Dump all FreeRTOS task states, priorities and stack margins on demand (vTaskListTasks / uxTaskGetSystemState) to diagnose hangs, deadlocks and starvation."
sources:
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/tasks.c
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/task.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Task state dumps

**Goal:** a `ps`-like snapshot of every task when the system misbehaves, from a console
command, a watchdog pre-reset hook or the debugger.

## The quick text dump
```c
/* configUSE_TRACE_FACILITY 1, configUSE_STATS_FORMATTING_FUNCTIONS 1 */
static char buf[512];                 /* size for your task count */
vTaskListTasks(buf, sizeof buf);      /* second argument is the buffer length */
printf("Name          State Prio Stack Num\n%s", buf);
```
States: `X` running, `B` blocked, `R` ready, `S` suspended (or blocked forever), `D` deleted
(awaiting cleanup). Stack column = high-water mark in **words**, not bytes.

## Reading the dump
| Pattern | Meaning |
|---|---|
| Task `R` for a long time while a higher one is `X` | starvation: higher-priority task never blocks |
| Two tasks `B` on each other's mutexes | deadlock (confirm with `xSemaphoreGetMutexHolder`) |
| Task `B` that should have been woken | missing give/notify, or event cleared by another waiter |
| Stack column near 0 | imminent overflow |
| Many `D` tasks | idle task starved, so deleted tasks' memory isn't freed |

## Richer dumps
`uxTaskGetSystemState` gives `eCurrentState`, `uxCurrentPriority` vs `uxBasePriority` (shows
priority inheritance in action), `usStackHighWaterMark`, run time. For blocked tasks, the object they wait on is not in `TaskStatus_t`.

## Where to trigger it
- Console/shell command (`ps`).
- **Watchdog early-warning**: if the hardware watchdog has a pre-timeout interrupt, dump task states to no-init RAM or flash before reset: the
  most useful post-mortem for field hangs.
- Debugger: an RTOS-aware debugger view shows similar information without code.

## Gotchas
- `vTaskListTasks` suspends the scheduler while building the string; don't call it from a
  high-rate loop.
- Names truncated to `configMAX_TASK_NAME_LEN`; choose distinctive short names.

## Verify
- [ ] Console `ps` works under load.
- [ ] A forced deadlock in a test build is visible in the dump with both tasks blocked.

## Checked

2026-10-28: confirmed against the FreeRTOS-Kernel sources and headers read this batch: `vTaskListTasks(buf, length)` needs `configUSE_TRACE_FACILITY == 1` and `configUSE_STATS_FORMATTING_FUNCTIONS > 0`, state letters (`X`, `B`, `R`, `S`, `D`), stack column is words, `TaskStatus_t` fields, `configMAX_TASK_NAME_LEN`, `xSemaphoreGetMutexHolder` (tasks.c, task.h, FreeRTOS.h, semphr.h). Removed or rewritten: the undefined `MAX_TASKS` sizing, vendor/debugger names (Ozone, CubeIDE, OpenOCD flag), STM32/ESP32 watchdog names, and the old `vTaskList` overflow note.
Method: documentation only; no commands were run.

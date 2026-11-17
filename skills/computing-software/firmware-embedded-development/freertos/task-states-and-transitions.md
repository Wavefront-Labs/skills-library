---
id: computing-software.firmware-embedded-development.freertos.task-states-and-transitions
name: task-states-and-transitions
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [task-states, blocked-state, suspended-state, etaskgetstate, freertos, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Reason about FreeRTOS task states (Running, Ready, Blocked, Suspended, Deleted): which API moves a task where, and how to diagnose a task stuck in the wrong state."
sources:
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/tasks.c
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/task.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Task states

## The four states (plus Deleted)
| State | Meaning | Entered by |
|---|---|---|
| Running | Executing on a core (one per core) | Scheduler picks highest-priority Ready task |
| Ready | Able to run, waiting for the CPU | Unblock, resume, creation, preemption |
| Blocked | Waiting for an event **or** a timeout | `vTaskDelay`, `xQueueReceive(.., ticks)`, `xSemaphoreTake`, `ulTaskNotifyTake`, `xEventGroupWaitBits` |
| Suspended | Not schedulable until explicitly resumed | `vTaskSuspend`; also an indefinite `portMAX_DELAY` wait when `INCLUDE_vTaskSuspend == 1` |
| Deleted | TCB awaiting idle-task cleanup | `vTaskDelete` |

Key subtlety: a task blocking with `portMAX_DELAY` and `INCLUDE_vTaskSuspend 1` is placed on
the suspended list (no timeout), so `eTaskGetState()` reports it as **Suspended**. Don't
misread that as someone calling `vTaskSuspend`.

## Querying
```c
eTaskState s = eTaskGetState(h);  /* INCLUDE_eTaskGetState 1 */
/* eRunning, eReady, eBlocked, eSuspended, eDeleted, eInvalid */
```
`vTaskListTasks()` letters: `X` running, `R` ready, `B` blocked, `S` suspended, `D` deleted.

## Diagnosing a stuck task
- **Always Ready, never Running:** a higher-priority task never blocks (busy loop, polling
  without delay). Find the CPU hog in run-time stats.
- **Blocked forever:** the event never arrives. Check the producer exists, the queue/semaphore
  handle is the same object, and the give actually executes (breakpoint on the give).
- **Suspended unexpectedly:** either a `portMAX_DELAY` wait (normal) or a stray
  `vTaskSuspend`; grep for suspend calls.
- **Deleted but memory not returned:** the idle task is starved so it never frees the TCB and
  stack. Make sure higher-priority tasks block.

## Design rules
- Every task should spend most time Blocked; a task that is always Ready starves all lower
  priorities.
- Prefer blocking calls with a finite timeout in production so a lost event is detectable.
- `vTaskSuspend`/`vTaskResume` from another task is wrong for synchronisation: a resume that
  arrives before the suspend is lost. Use a notification or semaphore instead.

## Verify
- [ ] `vTaskList` shows worker tasks mostly `B`/`S` and the idle task getting CPU.
- [ ] Each blocking call in long-running tasks has a reviewed timeout value.

## Checked

2026-10-28: confirmed against the FreeRTOS-Kernel sources and headers read this batch: `eTaskState` values (`eRunning`, `eReady`, `eBlocked`, `eSuspended`, `eDeleted`, `eInvalid`), `INCLUDE_eTaskGetState` default 0, deleted tasks wait on a termination list for idle cleanup, state letters, suspended-list handling with `INCLUDE_vTaskSuspend` (task.h, tasks.c, FreeRTOS.h). Removed or rewritten: the 'self-delete' qualifier and the old `vTaskList` name.
Method: documentation only; no commands were run.

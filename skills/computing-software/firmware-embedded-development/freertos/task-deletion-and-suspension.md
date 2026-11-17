---
id: computing-software.firmware-embedded-development.freertos.task-deletion-and-suspension
name: task-deletion-and-suspension
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [xtaskcreate, vtaskdelete, vtasksuspend, vtaskresume, idle-task-cleanup, task-lifecycle, freertos, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Delete, suspend and resume FreeRTOS tasks safely: who frees the memory, why suspend/resume is not a sync primitive, and the leaks and races to avoid."
sources:
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/task.h
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/tasks.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Task deletion and suspension

**Goal:** end or park a task without leaking memory, orphaning a mutex or losing a wake-up.

## Config
```c
#define INCLUDE_vTaskDelete   1
#define INCLUDE_vTaskSuspend  1   /* also makes portMAX_DELAY block forever */
```

## Deleting
```c
vTaskDelete(NULL);          /* self-delete: last line of a one-shot task */
vTaskDelete(hWorker);       /* delete another task */
```
- The kernel-allocated memory of a deleted task is freed by the **idle task** (task.h note). If idle is
  starved (see task-starvation-and-idle-task) the memory never comes back.
- Only memory the **kernel** allocated is freed. Buffers the task got from `pvPortMalloc`,
  mutexes it holds, sockets and peripherals stay as they were. Release them first.
- Statically created tasks (`xTaskCreateStatic`) free nothing; the buffers are yours to reuse.
- Do not return from a task function. End with `vTaskDelete(NULL)` or an infinite loop.

### Clean shutdown pattern
Never kill a task from outside while it holds a resource. Ask it to stop:
```c
xTaskNotify(hWorker, STOP_BIT, eSetBits);   /* worker sees bit, releases mutex, closes */
/* worker: cleanup(); vTaskDelete(NULL); */
```

## Suspending
```c
vTaskSuspend(hTask);   /* NULL = self */
vTaskResume(hTask);
```
- Suspension is not counted: three suspends are undone by one resume.
- A suspended task doesn't run whatever its priority.
- `xTaskResumeFromISR` must **not** be used to sync a task with an interrupt: if the interrupt
  fires before the task has suspended itself, the resume is lost and the task sleeps forever.
  Use a task notification or semaphore, which latch the event.
- Suspending a task that holds a mutex blocks everyone waiting for it. Priority inheritance
  can't help, because the holder can't run.
- `vTaskSuspendAll()` is different: it stops the scheduler (see critical-sections-and-scheduler-suspension).

## Legitimate uses of suspend
Parking a task during a mode change (e.g. firmware update), or debug/test harnesses. For
"wait until there is work" use blocking on a queue or notification instead.

## Verify
- [ ] The free-heap figure of your heap implementation returns to its baseline after create/delete cycles.
- [ ] Idle task gets CPU time (run-time stats) so self-deleted tasks are reaped.
- [ ] No task is deleted or suspended from outside while it can hold a mutex.
- [ ] No ISR-to-task signalling uses `xTaskResumeFromISR`.

## Checked

2026-10-28: confirmed against the FreeRTOS-Kernel sources and headers read this batch: calls to `vTaskSuspend` are not accumulative, the idle task frees the kernel-allocated memory of deleted tasks, `INCLUDE_vTaskSuspend` makes `portMAX_DELAY` waits indefinite, `xTaskResumeFromISR` and `INCLUDE_xTaskResumeFromISR` exist (task.h, FreeRTOS.h). Removed or rewritten: the split between self-delete and other-delete freeing, the 'asserts/hangs on most ports' claim, the block-timeout-while-suspended claim, `xPortGetFreeHeapSize` and the 1000x figure.
Method: documentation only; no commands were run.

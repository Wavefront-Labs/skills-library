---
id: computing-software.firmware-embedded-development.freertos.changing-task-priority-at-runtime
name: changing-task-priority-at-runtime
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [vtaskpriorityset, uxtaskpriorityget, dynamic-priority, priority-boost, freertos, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Change FreeRTOS task priorities at runtime with vTaskPrioritySet: immediate preemption effects, interaction with mutex inheritance, and safer alternatives."
sources:
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/task.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/tasks.c
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/History.txt
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/FreeRTOS.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Changing priority at runtime

```c
/* FreeRTOSConfig.h */
#define INCLUDE_vTaskPrioritySet   1
#define INCLUDE_uxTaskPriorityGet  1

UBaseType_t old = uxTaskPriorityGet(NULL);
vTaskPrioritySet(NULL, old + 2);     /* boost self */
do_time_critical_section();
vTaskPrioritySet(NULL, old);         /* restore */
```

## Semantics
- Takes effect immediately. Raising another task above the caller, or lowering the caller
  below a Ready task, causes a context switch **inside** the call.
- Values `>= configMAX_PRIORITIES` are clamped to `configMAX_PRIORITIES - 1` (and assert in
  debug builds).
- Mutex holders: the kernel tracks the base priority separately. `vTaskPrioritySet` changes
  the base; an inherited higher priority still applies until the mutex is given back.
  `uxTaskPriorityGet` returns the current priority, which may be inherited; `uxTaskBasePriorityGet`
  (added in V11.0.0) returns the base priority.
- There is no FromISR variant of `vTaskPrioritySet`; defer the change to a task.

## When it's reasonable
- Startup sequencing: an init task runs high, then drops itself to normal.
- Mode changes (e.g. a logging task raised while flushing before power-off).
- A supervisor demoting a task found hogging CPU.

## When it's a smell
- Using priority swaps to protect shared data: a task preempted mid-access still holds the
  data half-updated. Use a mutex or critical section.
- Boosting tasks in turn to make them alternate: use notifications.
- Hand-rolled priority inheritance: `xSemaphoreCreateMutex` already does it.

## Gotchas
- Raising a task above the timer service task changes when timer callbacks run relative to it.
- Save the old value from `uxTaskPriorityGet` instead of hardcoding the restore.

## Verify
- [ ] A trace (SystemView or GPIO toggles) shows the expected preemption at the set call.
- [ ] The original priority is restored on every path, including error returns.

## Checked

Checked 2026-10-25 against FreeRTOS-Kernel V11.3.2 (History.txt, released 16 October 2026, current main) and the FreeRTOS Kernel Book source. Confirmed: vTaskPrioritySet clamps a value of configMAX_PRIORITIES or more to configMAX_PRIORITIES - 1 and asserts (tasks.c); INCLUDE_vTaskPrioritySet and INCLUDE_uxTaskPriorityGet default to 0 (FreeRTOS.h); uxTaskBasePriorityGet added in V11.0.0 (History.txt); task.h declares no FromISR setter. Removed the SMP migration claim. 
Method: documentation only; no commands were run.

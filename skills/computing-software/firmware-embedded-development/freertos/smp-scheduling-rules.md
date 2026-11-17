---
id: computing-software.firmware-embedded-development.freertos.smp-scheduling-rules
name: smp-scheduling-rules
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [freertos-smp, smp-scheduling, confignumber-of-cores, configrun-multiple-priorities, vtaskcoreaffinityset, smp-race-conditions, rp2040-smp, freertos, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Understand FreeRTOS SMP scheduling (one kernel across cores): how priorities map to cores, configRUN_MULTIPLE_PRIORITIES, affinity, and single-core assumptions that break."
sources:
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/FreeRTOS.h
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/task.h
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/tasks.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FreeRTOS SMP scheduling rules

**Goal:** move single-core FreeRTOS designs to the SMP kernel without introducing races that single-core priority rules
used to prevent.

## Model
One kernel instance schedules tasks across `configNUMBER_OF_CORES` identical cores. At any time
the N highest-priority ready tasks run, one per core (subject to affinity).

## Key config
```c
#define configNUMBER_OF_CORES          2
#define configRUN_MULTIPLE_PRIORITIES  1   /* default 0 */
#define configUSE_CORE_AFFINITY        1
#define configUSE_TASK_PREEMPTION_DISABLE 1
#define configUSE_PASSIVE_IDLE_HOOK    0
```
- `configRUN_MULTIPLE_PRIORITIES` defaults to 0 (FreeRTOS.h); tasks.c refers to yielding cores "if multiple priorities are not allowed to run", so 0 restricts parallelism across priorities.
- With 1, tasks of different priorities may run at the same time on different cores.

## Assumptions that break
| Single-core habit | Why it breaks on SMP |
|---|---|
| "Highest priority task runs alone, so no lock needed for data only it and lower tasks touch" | lower tasks run in parallel now |
| `vTaskSuspendAll()` to protect data | check what the SMP kernel guarantees for it; prefer mutexes or the kernel's critical sections |
| ISR and task never run simultaneously | the ISR may run on the other core |
| Disabling interrupts as a lock | only the local core |
| Busy-wait for a flag set by a lower-priority task | fine now (it can run), but wastes a core |
Audit every shared variable and use the kernel's synchronisation primitives or atomics.

## Affinity
`vTaskCoreAffinitySet(task, 1 << 0)` pins to core 0 (e.g. tasks using a peripheral whose
interrupt is routed to core 0, or legacy code that isn't thread-safe). Pinning everything
recreates two single-core systems; pin only what needs it.

## Preemption control
`vTaskPreemptionDisable(task)` (with `configUSE_TASK_PREEMPTION_DISABLE`) prevents a task being
preempted on its core: short sections that must complete without interleaving on that core.

## Verify
- [ ] Stress test with all tasks unpinned and `configRUN_MULTIPLE_PRIORITIES=1` under ThreadSanitizer-like
      review of shared data (or long soak with assertions on invariants).
- [ ] Trace shows the expected task-to-core distribution.

## Checked

2026-10-28: confirmed against the FreeRTOS-Kernel sources and headers read this batch: `configNUMBER_OF_CORES`, `configRUN_MULTIPLE_PRIORITIES` (default 0), `configUSE_CORE_AFFINITY` (default 0), `configUSE_TASK_PREEMPTION_DISABLE` (default 0), `vTaskCoreAffinitySet`, `vTaskPreemptionDisable`, `tskNO_AFFINITY` (FreeRTOS.h, task.h, tasks.c). Removed or rewritten: the platform list, the ESP-IDF section, the spinlock claim for critical sections, the `vTaskSuspendAll` behaviour claim and the 'same (highest) priority' definition of the 0 setting.
Method: documentation only; no commands were run.

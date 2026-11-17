---
id: computing-software.firmware-embedded-development.freertos.time-slicing-equal-priority-tasks
name: time-slicing-equal-priority-tasks
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [freertos-scheduler, time-slicing, configuse-time-slicing, round-robin, configidle-should-yield, taskyield, freertos, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Understand and configure FreeRTOS round-robin time slicing between equal-priority tasks: tick-based slices, partial slices, idle yielding and when to turn it off."
sources:
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/FreeRTOS.h
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/tasks.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time slicing between equal-priority tasks

With `configUSE_PREEMPTION` and `configUSE_TIME_SLICING` both 1, the highest
priority ready task runs, and **ready tasks of equal priority share the CPU round-robin on tick interrupts**.

## Config
```c
#define configUSE_PREEMPTION      1
#define configUSE_TIME_SLICING    1   /* default 1 if not defined */
#define configIDLE_SHOULD_YIELD   1   /* idle yields to priority-0 app tasks */
#define configTICK_RATE_HZ        1000
```

## How a slice behaves
- A slice ends at the **next tick interrupt**, not after a full tick period. A task that was
  switched in partway through a tick period only gets the rest of that period.
  Don't expect fair CPU shares from time slicing.
- A task that blocks or yields early gives up the rest of its slice.
- Time slicing only matters when two or more equal-priority tasks are **ready at the same
  time**. In well-designed event-driven firmware tasks mostly block, and slicing rarely happens.
- `taskYIELD()` hands over to the next equal-priority ready task immediately.

## Turning it off
`configUSE_TIME_SLICING 0`: equal-priority tasks don't rotate on ticks. The running task keeps
the CPU until it blocks, yields or a higher-priority task becomes ready. Use it when:
- you want fewer context switches (less overhead, better cache behaviour) and tasks are
  event-driven anyway;
- equal-priority tasks touch the same data and you'd rather not have tick-driven preemption
  between them (it doesn't replace locking against higher priorities or ISRs).

Risk: a CPU-bound task starves its equal-priority peers indefinitely.

## Idle task and priority 0
With `configIDLE_SHOULD_YIELD 1`, idle yields at once if an application task at priority 0 is
ready, so priority-0 app tasks get nearly all idle time. With 0, idle takes a full slice like
any other priority-0 task. Idle hook work and deleted-task cleanup run inside idle, so if you
have priority-0 busy loops, check idle still gets time.

## SMP note
On SMP FreeRTOS (`configNUMBER_OF_CORES > 1`) the kernel has a separate time-slicing branch, so ordering assumptions
from single-core builds may not hold (see smp-scheduling-rules).

## Verify
- [ ] Two CPU-bound equal-priority test tasks both make progress with slicing on, and one starves with it off.
- [ ] A trace tool shows tick-driven switches only where you expect them.
- [ ] Design doc says which tasks share a priority and why.

## Checked

2026-10-28: confirmed against the FreeRTOS-Kernel sources and headers read this batch: `configUSE_TIME_SLICING` and `configIDLE_SHOULD_YIELD` default to 1 (FreeRTOS.h); the time-slicing branch is guarded by `configUSE_PREEMPTION == 1 && configUSE_TIME_SLICING == 1` and the single-core/SMP split (tasks.c); idle yield and idle-task housekeeping (tasks.c). Removed or rewritten: the 0.9 ms/0.1 ms example, the quoted policy name, and the claim that SMP time slicing rotates tasks across cores.
Method: documentation only; no commands were run.

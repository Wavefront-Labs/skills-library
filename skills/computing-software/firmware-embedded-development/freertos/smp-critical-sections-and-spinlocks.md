---
id: computing-software.firmware-embedded-development.freertos.smp-critical-sections-and-spinlocks
name: smp-critical-sections-and-spinlocks
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [smp-critical-section, portget-task-lock, portget-isr-lock, spinlock, cross-core-race, freertos, firmware-embedded-development]
level: sme
status: draft
description: "Protect shared data on FreeRTOS SMP: why disabling interrupts is no longer enough, how taskENTER_CRITICAL takes cross-core locks, and port spinlocks like ESP-IDF's."
sources:
  - https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/13-Symmetric-multiprocessing-introduction
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/freertos_idf.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SMP critical sections and spinlocks

On a single core, "disable interrupts" or "suspend the scheduler" makes a code region exclusive.
On SMP both only affect the **calling core**; the other core keeps running and can touch the same
data.

## Mainline FreeRTOS SMP (kernel 11)
`taskENTER_CRITICAL()` on SMP ports:
1. disables interrupts on this core,
2. takes the port's **ISR lock** and **task lock** (`portGET_ISR_LOCK`, `portGET_TASK_LOCK`,
   hardware spinlocks or atomic flags supplied by the port),
3. nests per core.

So it is exclusive across cores, but every core contending spins. Keep sections to a handful of
instructions.

```c
taskENTER_CRITICAL();
shared_counter++;
ring_head = next;
taskEXIT_CRITICAL();

/* ISR side */
UBaseType_t s = taskENTER_CRITICAL_FROM_ISR();
...
taskEXIT_CRITICAL_FROM_ISR(s);
```
`vTaskSuspendAll()` on SMP stops scheduling on all cores, but tasks already running on other
cores continue; it does **not** protect data from them. Use a mutex or critical section.

## ESP-IDF FreeRTOS (dual-core Xtensa/RISC-V)
IDF's variant makes the lock explicit:
```c
static portMUX_TYPE s_lock = portMUX_INITIALIZER_UNLOCKED;

portENTER_CRITICAL(&s_lock);        /* task context */
...
portEXIT_CRITICAL(&s_lock);

portENTER_CRITICAL_ISR(&s_lock);    /* ISR context */
```
Use one `portMUX_TYPE` per protected resource, not one global, to reduce contention.

## Choosing
| Section length | Tool |
|---|---|
| A few instructions, ISR involved | critical section / spinlock |
| Single word update | C11 atomics (`atomic_fetch_add`) or FreeRTOS `Atomic_Increment_u32` (atomic.h) |
| Longer, task-only | mutex (blocks instead of spinning, priority inheritance) |
| Data owned by one task | queue to a gatekeeper task; no lock needed |

## Pitfalls
- Code ported from single-core relying on "my task is highest priority, so nobody else runs":
  with `configRUN_MULTIPLE_PRIORITIES 1` lower-priority tasks run concurrently on other cores.
  Setting it to 0 restores the guarantee at the cost of parallelism.
- Calling blocking APIs inside a critical section deadlocks faster on SMP.
- Spinning across cores with interrupts disabled raises worst-case interrupt latency on both.
- Volatile is not synchronisation; use atomics or locks for cross-core flags, plus memory barriers
  where the port does not include them.

## Verify
- [ ] Every shared structure lists its protecting lock; reviewers check each access.
- [ ] Stress test with tasks pinned to different cores hammering shared data passes.
- [ ] Critical sections measured (cycle counter) under a few microseconds.

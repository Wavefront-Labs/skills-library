---
id: computing-software.firmware-embedded-development.zephyr.deadline-edf-scheduling
name: deadline-edf-scheduling
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [edf-scheduling, config-sched-deadline, k-thread-deadline-set, earliest-deadline-first, zephyr, firmware-embedded-development]
level: sme
status: docs-checked
description: "Use Zephyr's earliest-deadline-first tie-breaking (CONFIG_SCHED_DEADLINE, k_thread_deadline_set) among equal-priority threads, and understand what it does not guarantee."
sources:
  - https://docs.zephyrproject.org/latest/kernel/services/scheduling/index.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/kernel.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deadline (EDF) scheduling

```
CONFIG_SCHED_DEADLINE=y
```
Zephyr's EDF is a **tie-breaker within a priority level**: static priority still decides first.
Among ready threads with the same priority, the one with the earliest deadline runs.

```c
void sensor_fn(void *a, void *b, void *c)
{
    for (;;) {
        k_sem_take(&data_ready, K_FOREVER);
        k_thread_deadline_set(k_current_get(), k_ms_to_cyc_ceil32(2));   /* due in 2 ms */
        process_frame();
    }
}
```
- `k_thread_deadline_set(tid, deadline_cycles)`: deadline is a time delta **from now**, in the
  units of `k_cycle_get_32()` (`k_ms_to_cyc_ceil32` and the other time-unit helpers convert).
  Set it each time a job is released. The relative deadline is silently clamped to the range
  [0, 2^30] cycles.
- `k_thread_absolute_deadline_set(tid, deadline)` takes an absolute timestamp, so several threads
  can share one "now".
- Deadlines are stored as 32-bit unsigned values: the span between the first and last deadline
  in the ready queue must be less than 2^31 cycles, or threads may run in the wrong deadline order.
- With EDF enabled, two threads only count as equal priority when both static priority and
  deadline are equal.

## What it is not
- Not a full EDF scheduler: the kernel makes no guarantee the thread will be scheduled within
  its deadline and takes no runtime/period metadata to validate achievability. Even a deadline
  already in the past just orders threads from earliest to latest; nothing is killed or flagged.
- Doesn't preempt across priorities: a higher-priority thread with a far deadline still beats a
  lower-priority thread with an urgent one.
- The multi-queue ready queue (`CONFIG_SCHED_MULTIQ`) is documented as incompatible with deadline
  scheduling, which needs to sort threads more finely; use the simple or scalable ready queue.

## When useful
A group of similar jobs at one priority (several sensor pipelines, media frames) where release
times vary and you want the most urgent first without juggling priorities.

## Verify
- [ ] EDF threads share a priority level with no non-EDF threads.
- [ ] Deadlines set at each job release, converted with the kernel cycle helpers.
- [ ] Tracing shows the earliest-deadline thread runs first when several are ready.

## Checked

Checked 2026-10-25 against the Zephyr source (main, post-4.4; latest release v4.4.2): doc/kernel/services/scheduling/index.rst and include/zephyr/kernel.h.
Confirmed: `CONFIG_SCHED_DEADLINE` as a tie-breaker among equal static priorities; `k_thread_deadline_set` (relative, in `k_cycle_get_32()` units, clamped to [0, 2^30]); `k_thread_absolute_deadline_set`; the 2^31 span rule; no achievability checking; no cross-priority preemption; MULTIQ incompatibility.

Method: documentation only; no commands were run.

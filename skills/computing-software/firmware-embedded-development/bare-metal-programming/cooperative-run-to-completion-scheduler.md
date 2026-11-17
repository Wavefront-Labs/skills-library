---
id: computing-software.firmware-embedded-development.bare-metal-programming.cooperative-run-to-completion-scheduler
name: cooperative-run-to-completion-scheduler
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [cooperative-scheduler, run-to-completion, superloop, task-scheduler, non-preemptive, event-flags, wfi, bare-metal-architecture, firmware-embedded-development]
level: practitioner
status: draft
description: "Build a non-preemptive run-to-completion scheduler for bare-metal firmware: task table, ISR-set ready flags, priority order, sleep when idle, and worst-case latency."
sources:
  - https://www.safetty.net/publications/pttes
  - https://www.state-machine.com/doc/AN_Super_Simple_Tasker.pdf
  - https://developer.arm.com/documentation/ddi0403/latest
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cooperative run-to-completion scheduler

**Goal:** structure a bare-metal application as small tasks that each run to completion,
triggered by interrupts or time, with no RTOS, no per-task stacks and predictable latency.

## Shape
```c
typedef void (*task_fn)(void);
static task_fn const tasks[] = { comms_task, control_task, ui_task };  /* priority order */
static volatile uint32_t ready;                                       /* bit n = task n */

void task_post(unsigned n) { __atomic_fetch_or(&ready, 1u << n, __ATOMIC_RELAXED); }  /* from ISRs */

int main(void) {
    init();
    for (;;) {
        __disable_irq();
        uint32_t r = ready;
        if (r == 0) { __WFI(); __enable_irq(); continue; }   /* sleep atomically */
        unsigned n = __builtin_ctz(r);                        /* highest priority = lowest bit */
        ready &= ~(1u << n);
        __enable_irq();
        tasks[n]();                                           /* runs to completion */
    }
}
```
- ISRs do the minimum (grab data into a buffer) and `task_post()`.
- Restarting the scan after each task gives priority ordering: a high-priority task
  never waits for more than one lower-priority task to finish.
- On ARMv6-M (no `__atomic_fetch_or` without lock-free support) wrap the OR in a
  PRIMASK section.

## The WFI race
Checking `ready` with interrupts enabled and then calling `__WFI()` can sleep through an
event posted between the check and the WFI. Disabling interrupts with PRIMASK before the
check is safe: a pending interrupt still wakes WFI even while masked, and it runs as soon
as `__enable_irq()` executes.

## Timing analysis
- Worst-case latency of task k = its own WCET + longest single lower-priority task +
  all higher-priority tasks that can become ready meanwhile. Keep every task short; split
  long work into state-machine steps that re-post themselves.
- Periodic tasks: a SysTick ISR posts them; or use a time-triggered table (see
  `time-triggered-scheduler`).
- Measure each task's WCET with the DWT cycle counter and log the max.

## When to move to an RTOS
Blocking APIs you cannot restructure (third-party stacks), many independent timing
domains, or a task whose WCET cannot be chopped below the latency budget of others. A
preemptive but single-stack alternative is an SST/QK-style kernel using PendSV.

## Verify
- [ ] Idle current shows the core sleeping between events.
- [ ] Max measured task WCET < tightest latency requirement of any higher-priority task.
- [ ] Event storms do not starve the lowest task forever (or that is an accepted design).

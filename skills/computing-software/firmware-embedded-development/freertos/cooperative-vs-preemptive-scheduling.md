---
id: computing-software.firmware-embedded-development.freertos.cooperative-vs-preemptive-scheduling
name: cooperative-vs-preemptive-scheduling
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [freertos-scheduler, configuse-preemption, cooperative-scheduling, preemptive-scheduling, context-switch, freertos, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Choose between FreeRTOS preemptive and co-operative scheduling with configUSE_PREEMPTION: latency, shared-data safety, yield points and migrating between them."
sources:
  - https://github.com/FreeRTOS/FreeRTOS-Kernel-Book/blob/main/ch04.md
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/FreeRTOS.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Co-operative vs preemptive scheduling

```c
#define configUSE_PREEMPTION 1   /* 1 = preemptive, 0 = co-operative */
```

## Preemptive (1)
A higher-priority task that becomes ready (from an ISR, a give, a tick timeout) runs
**immediately**, interrupting the current task. Latency to a high-priority event is bounded
by ISR time plus critical sections, independent of what low-priority code is doing. The price:
any task can be interrupted between any two instructions, so every piece of data shared
between tasks needs a mutex, critical section or ownership rule.

## Co-operative (0)
A context switch happens only when the running task **blocks** (delay, queue wait, take) or
calls `taskYIELD()`. Ticks don't preempt and readiness of a higher-priority task waits until
the current one gives up the CPU. Interrupts still run.
- Shared data between tasks needs no locking as long as nobody blocks or yields mid-update
  (ISRs still need protection).
- Worst-case latency = the longest stretch any task runs without blocking or yielding. One
  slow `flash_erase()` delays everything.
- The Kernel Book describes co-operative scheduling on the assumption that ISRs do not
  explicitly request context switches: a switch then happens only when the running task blocks
  or yields.
- Tasks are never preempted, so time slicing cannot be used.

## Choosing
| Situation | Choose |
|---|---|
| Hard latency requirements (motor control, comms with tight timeouts) | preemptive |
| Mixed-criticality tasks, third-party stacks (lwIP, USB) | preemptive |
| Tiny MCU, a few simple tasks, legacy superloop being converted | co-operative can be fine |
| Team unfamiliar with concurrency, all tasks short and cooperative | co-operative as a stepping stone |

A middle path is preemptive with `configUSE_TIME_SLICING 0` (the default is 1): priority-based preemption without tick-driven rotation between
equals (see time-slicing-equal-priority-tasks).

## Migrating co-operative to preemptive
1. List every global/static touched by more than one task: these become races.
2. Protect with mutexes (or convert to message passing).
3. Remove `taskYIELD()` calls that were only there to share the CPU.
4. Turn on `configASSERT` and run a soak test with tracing.

## Verify
- [ ] Measured worst-case event latency (GPIO toggle in ISR and in task) meets the requirement.
- [ ] In co-operative builds, longest non-yielding run is measured and documented.
- [ ] Shared-data inventory exists for preemptive builds.

## Checked

Checked 2026-10-25 against FreeRTOS-Kernel V11.3.2 (History.txt, released 16 October 2026, current main) and the FreeRTOS Kernel Book source. Confirmed: in co-operative mode a context switch occurs only when the running task blocks or calls taskYIELD(), tasks are never preempted and time slicing cannot be used (Kernel Book 4.12.5); configUSE_TIME_SLICING defaults to 1 (FreeRTOS.h). Removed the port-dependence claim, the stack-depth claim and the prevalence claim. 
Method: documentation only; no commands were run.

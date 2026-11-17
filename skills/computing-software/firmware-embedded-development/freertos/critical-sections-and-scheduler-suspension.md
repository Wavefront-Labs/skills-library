---
id: computing-software.firmware-embedded-development.freertos.critical-sections-and-scheduler-suspension
name: critical-sections-and-scheduler-suspension
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [freertos-interrupts, taskenter-critical, taskexit-critical, taskenter-critical-from-isr, vtasksuspendall, xtaskresumeall, critical-section-nesting, freertos, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Choose between taskENTER_CRITICAL, the FromISR variant, scheduler suspension and a mutex for protecting shared data in FreeRTOS, and keep critical sections short."
sources:
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/task.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/atomic.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel-Book/blob/main/ch08.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Critical sections and scheduler suspension

**Goal:** protect shared data with the cheapest mechanism that is actually correct for who
can access it.

## The options
| Mechanism | Blocks | Use when |
|---|---|---|
| `taskENTER_CRITICAL()` / `taskEXIT_CRITICAL()` | context switches **and** ISRs at or below the syscall priority | data shared with kernel-aware ISRs; a few lines |
| `taskENTER_CRITICAL_FROM_ISR()` / `taskEXIT_CRITICAL_FROM_ISR(saved)` | same, from inside an ISR | ISR shares data with a higher-priority ISR |
| `vTaskSuspendAll()` / `xTaskResumeAll()` | context switches only, interrupts stay enabled | longer sections shared between tasks only |
| mutex | only the tasks contending | long sections, may block, priority inheritance |
| atomic ops (`Atomic_*` functions in `atomic.h`) | nothing | single-variable counters/flags |

## Rules for taskENTER_CRITICAL
- Nests (counted); every enter needs exactly one exit on every path, including error returns.
- **Do not call blocking APIs inside** (`vTaskDelay`, queue send with timeout).
- Keep it very short: the Kernel Book warns that long critical sections adversely affect
  interrupt response times.
- Only interrupts at or below `configMAX_SYSCALL_INTERRUPT_PRIORITY` are masked on ports with
  priority-based masking. Higher-priority interrupts keep running and must not call FreeRTOS
  API functions, so they can't share data through this mechanism.
- In ISRs use the `_FROM_ISR` form and pass the saved mask back:
  ```c
  UBaseType_t s = taskENTER_CRITICAL_FROM_ISR();
  shared.count++;
  taskEXIT_CRITICAL_FROM_ISR(s);
  ```

## Rules for scheduler suspension
- Don't call any API that could cause a context switch (for example `xTaskDelayUntil()` or
  `xQueueSend()`) between suspend and resume.
- ISRs still run; data shared with ISRs needs a critical section instead.
- `xTaskResumeAll()` returns pdTRUE if a pending context switch was performed before it returned; long
  suspensions delay higher-priority tasks, so measure.

## SMP note
When `configNUMBER_OF_CORES` is greater than 1, `taskENTER_CRITICAL_FROM_ISR` maps to the port's
`portENTER_CRITICAL_FROM_ISR` rather than the single-core interrupt-mask macro (task.h), so
behaviour is port-specific. Read the SMP port documentation before reusing single-core
patterns.

## Verify
- [ ] Code review: every `taskENTER_CRITICAL` has a matching exit on all paths, and contains no
      blocking calls or loops of unbounded length.
- [ ] Measured worst-case critical-section length (GPIO marker or trace) under load.

## Checked

Checked 2026-10-25 against FreeRTOS-Kernel V11.3.2 (History.txt, released 16 October 2026, current main) and the FreeRTOS Kernel Book source. Confirmed: taskENTER_CRITICAL nests with a depth count, short critical sections only, and interrupts above configMAX_SYSCALL_INTERRUPT_PRIORITY are not masked and may not call the API (Kernel Book 8.2.1); vTaskSuspendAll leaves interrupts running and forbids context-switching API calls (task.h); xTaskResumeAll return value (Book 8.2.4); taskENTER_CRITICAL_FROM_ISR definitions for one core versus several (task.h); Atomic_ functions exist in atomic.h. Removed the BASEPRI, undefined-behaviour, C11-atomics and ESP-IDF claims. 
Method: documentation only; no commands were run.

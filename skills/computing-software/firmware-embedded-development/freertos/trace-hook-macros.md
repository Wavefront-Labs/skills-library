---
id: computing-software.firmware-embedded-development.freertos.trace-hook-macros
name: trace-hook-macros
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [freertos-debugging, trace-hook-macros, tracetask-switched-in, tracetask-switched-out, tracequeue-send, gpio-trace, application-task-tag, freertos, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Instrument the FreeRTOS kernel with trace hook macros (traceTASK_SWITCHED_IN etc.) to drive GPIO timing pins, custom event logs or a homemade tracer."
sources:
  - https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-RTOS-trace-feature
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FreeRTOS trace hook macros

**Goal:** observe scheduler behaviour (which task runs when, queue blocks, ISR wakes) with a
logic analyser or a tiny RAM log, when a commercial tracer isn't available.

## How they work
`FreeRTOS.h` defines dozens of empty macros (`traceTASK_SWITCHED_IN()`,
`traceTASK_SWITCHED_OUT()`, `traceQUEUE_SEND(pxQueue)`, `traceBLOCKING_ON_QUEUE_RECEIVE(pxQueue)`,
`traceTASK_INCREMENT_TICK(xTickCount)`, `traceMALLOC(pv, size)`, ...). Define them in
`FreeRTOSConfig.h` and the kernel calls them at those points. They run inside the kernel, often
in critical sections or ISRs: **keep them tiny**, no API calls, no printf.

## GPIO task visualisation
Give each interesting task a tag (pin mask), output it on switch-in:
```c
/* FreeRTOSConfig.h */
#define configUSE_APPLICATION_TASK_TAG 1
#define traceTASK_SWITCHED_IN()  do { \
    uint32_t t = (uint32_t)pxCurrentTCB->pxTaskTag; if (t) GPIOB->BSRR = t; } while (0)
#define traceTASK_SWITCHED_OUT() do { \
    uint32_t t = (uint32_t)pxCurrentTCB->pxTaskTag; if (t) GPIOB->BSRR = t << 16; } while (0)
/* app: */ vTaskSetApplicationTaskTag(NULL, (TaskHookFunction_t)(1u << 3));  /* PB3 */
```
On a logic analyser each pin shows when its task runs: exact jitter, preemption and
starvation visible at nanosecond resolution. `pxCurrentTCB` is accessible because the macros
expand inside `tasks.c`.

## RAM event log
```c
#define traceQUEUE_SEND_FAILED(q)  trace_log(EV_QSEND_FAIL, (uint32_t)(q))
#define traceMALLOC(p, sz)         trace_log(EV_MALLOC, (uint32_t)(sz))
```
`trace_log` writes {timestamp (DWT CYCCNT), event, arg} into a circular buffer; dump it after a
fault via the debugger or post-mortem. Use the queue registry (`vQueueAddToRegistry`) to map
handles to names when decoding.

## Gotchas
- Macros must be defined **before** `FreeRTOS.h` includes its defaults (i.e. in
  `FreeRTOSConfig.h`), otherwise the empty defaults win.
- Only one owner: SystemView/Tracealyzer also define these macros; don't combine with your own
  without merging.
- Some hooks run with interrupts masked; slow hooks add latency to everything.

## Verify
- [ ] Logic analyser shows one pin per tagged task with sensible switching.
- [ ] RAM log decodes with names; overhead measured against your latency budget.

## Checked
2026-11-01. Confirmed in FreeRTOS-Kernel include/FreeRTOS.h and tasks.c: each trace macro named here exists as an
empty default guarded by `#ifndef` (so defining it earlier in `FreeRTOSConfig.h` wins), with the argument lists shown;
`pxTaskTag` is a TCB member under `configUSE_APPLICATION_TASK_TAG`; `vTaskSetApplicationTaskTag` and
`vQueueAddToRegistry` exist. Removed the "tens of cycles" overhead figure (not documented).
Method: documentation only; no commands were run.

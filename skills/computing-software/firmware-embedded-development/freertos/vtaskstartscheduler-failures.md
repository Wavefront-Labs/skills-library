---
id: computing-software.firmware-embedded-development.freertos.vtaskstartscheduler-failures
name: vtaskstartscheduler-failures
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [vtaskstartscheduler, scheduler-start, svc-handler, first-task-start, freertos, firmware-embedded-development]
level: practitioner
status: gated
description: "Debug FreeRTOS vTaskStartScheduler failures: returning due to heap, faulting in the first task start, vector table mapping, MSP reset, and pre-scheduler interrupts."
sources:
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/tasks.c
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/FreeRTOS.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vTaskStartScheduler failures

`vTaskStartScheduler()` creates the idle task (and timer task), configures the tick, and jumps
into the first task. It never returns on success.

```c
vTaskStartScheduler();
/* Only reached on failure */
configASSERT(0);
for (;;);
```

## It returned
Cause: idle or timer task (or timer queue) could not be allocated.
- Dynamic allocation: `configTOTAL_HEAP_SIZE` too small for everything created so far plus
  idle stack (`configMINIMAL_STACK_SIZE` words) and timer stack (`configTIMER_TASK_STACK_DEPTH`).
  Print your heap implementation's free-size figure right before the call.
- `configUSE_MALLOC_FAILED_HOOK 1` will catch it at the failed allocation.

## Hard fault inside it (Cortex-M)
On Cortex-M the port starts the first task through an SVC handler and switches contexts with PendSV; if those vectors still point at default handlers you get a fault or a
silent hang. (gated: unconfirmed, source is paywalled or blocked)
```c
/* FreeRTOSConfig.h mapping when the vector table uses CMSIS names */
#define vPortSVCHandler      SVC_Handler
#define xPortPendSVHandler   PendSV_Handler
#define xPortSysTickHandler  SysTick_Handler   /* only if SysTick is not also the HAL timebase */
```
`configCHECK_HANDLER_INSTALLATION` (default 1 in FreeRTOS.h) enables a check that the handlers are installed; see your port for details.

## Other first-switch faults
- Cortex-M startup state, VTOR after a bootloader jump, and FPU enablement are port-specific; check your port's documentation and the Arm architecture reference. (gated: unconfirmed, source is paywalled or blocked)
- **Interrupts firing before start:** an ISR enabled before the scheduler that calls FromISR APIs
  may try to context switch before any task exists; enable peripheral IRQs inside tasks or ensure
  ISRs tolerate it.

## Tick never runs
First task runs but `vTaskDelay` hangs: the tick interrupt is not routed to the port's tick handler (for example a HAL owns SysTick), or the CPU clock setting is wrong so the reload value is wrong. (gated: unconfirmed, source is paywalled or blocked)

## Verify
- [ ] Code after `vTaskStartScheduler` asserts.
- [ ] SVC, PendSV and tick vectors resolve to FreeRTOS port handlers in the map file.
- [ ] After a bootloader jump: VTOR, MSP, CONTROL reset before `main`.

## Checked

2026-10-28: confirmed against the FreeRTOS-Kernel sources and headers read this batch: the scheduler creates the idle and timer tasks before starting (FreeRTOS.h hook comment), `configUSE_MALLOC_FAILED_HOOK` and `configCHECK_HANDLER_INSTALLATION` exist with their defaults (FreeRTOS.h). Removed or rewritten: the 10.6+ version claim, `xPortGetFreeHeapSize` (heap files not fetched), the CONTROL/VTOR/CPACR specifics and the interrupt-masking claim. Cortex-M port internals (SVC/PendSV start-up, SysTick routing, bootloader state) are port files and Arm manuals not fetched (gated).
Method: documentation only; no commands were run.

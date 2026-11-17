---
id: computing-software.firmware-embedded-development.freertos.configassert-and-defensive-checks
name: configassert-and-defensive-checks
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [freertosconfig-h, configassert, assert-handler, vassertcalled, interrupt-priority-assert, debug-build, freertos, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Define configASSERT so FreeRTOS catches its own misuse (wrong ISR priority, API from ISR, NULL handles), and decide what assert does in production builds."
sources:
  - https://github.com/FreeRTOS/FreeRTOS-Kernel-Book/blob/main/ch12.md
  - https://github.com/FreeRTOS/FreeRTOS-Kernel-Book/blob/main/ch13.md
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/portable/GCC/ARM_CM4F/port.c
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/queue.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# configASSERT and defensive checks

**Goal:** turn the kernel's built-in sanity checks on, so configuration mistakes stop at the
offending line instead of corrupting the scheduler minutes later.

## Define it
```c
/* FreeRTOSConfig.h */
void vAssertCalled(const char *file, int line);
#define configASSERT(x) do { if ((x) == 0) vAssertCalled(__FILE__, __LINE__); } while (0)
```
```c
void vAssertCalled(const char *file, int line) {
    taskDISABLE_INTERRUPTS();
    g_crash.file = file; g_crash.line = line;   /* no-init RAM for post-mortem */
#ifdef DEBUG
    __BKPT(0);                                    /* halt in the debugger */
    for (;;) { }
#else
    NVIC_SystemReset();
#endif
}
```
Leaving `configASSERT` undefined disables every check below: the default empty definition is
removed by the preprocessor. Treat a failed assertion as fatal and do not execute past it.

## What it catches (Cortex-M ports)
- **ISR priority above `configMAX_SYSCALL_INTERRUPT_PRIORITY` calling a FromISR API**
  (`vPortValidateInterruptPriority`). Interrupts left at the default priority of zero are the
  highest priority and always fail this check. Fix the priority, never the assert.
- **Priority grouping with sub-priority bits** (the Cortex-M port asserts that all priority bits
  are pre-emption bits; its comment suggests `NVIC_SetPriorityGrouping(0)` with CMSIS, but vendor
  libraries may assume another grouping).
- Non-FromISR API called from an ISR (`portASSERT_IF_IN_ISR` in tasks.c).
- Blocking with a non-zero timeout while the scheduler is suspended (queue.c asserts this).

## Production policy
- The Kernel Book notes that defining `configASSERT` increases code size and slows execution;
  keep asserts in release builds only if that cost is acceptable, and drop the file string if
  flash is tight.
- Record file/line in no-init RAM, reset, and report after boot. A silent hang is worse than a
  logged reset.
- Avoid `printf` inside the assert handler: the driver it depends on may be what failed.

## Related hooks
`configCHECK_FOR_STACK_OVERFLOW` (1, 2 or 3) + `vApplicationStackOverflowHook`, and
`configUSE_MALLOC_FAILED_HOOK 1` + `vApplicationMallocFailedHook`: same handler style.

## Verify
- [ ] Deliberately call `xQueueSendFromISR` from an ISR at priority 0: assert fires with the
      port.c line.
- [ ] Release build reset reason log shows assert file/line after a forced failure.

## Checked

Checked 2026-10-25 against FreeRTOS-Kernel V11.3.2 (History.txt, released 16 October 2026, current main) and the FreeRTOS Kernel Book source. Confirmed: configASSERT is application-defined in FreeRTOSConfig.h and compiles away when undefined, and a failed assertion must be treated as fatal (Kernel Book 12.2); the Cortex-M4F port asserts interrupt priority (>= configMAX_SYSCALL_INTERRUPT_PRIORITY) and priority grouping; queue.c asserts against blocking with the scheduler suspended; configCHECK_FOR_STACK_OVERFLOW values 1, 2, 3 (Book 13). Removed vendor HAL claims and the vague list of other checks. 
Method: documentation only; no commands were run.

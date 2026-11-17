---
id: computing-software.firmware-embedded-development.freertos.malloc-failed-hook
name: malloc-failed-hook
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [malloc-failed-hook, vapplicationmallocfailedhook, configuse-malloc-failed-hook, heap-exhaustion, vportgetheapstats, freertos, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Catch FreeRTOS heap exhaustion at the moment it happens with vApplicationMallocFailedHook, record useful context, and size the heap from minimum-ever-free data."
sources:
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/portable/MemMang/heap_1.c
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/portable/MemMang/heap_2.c
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/portable/MemMang/heap_3.c
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/portable/MemMang/heap_4.c
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/portable/MemMang/heap_5.c
  - https://github.com/FreeRTOS/FreeRTOS-Kernel-Book/blob/main/ch03.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Malloc-failed hook

Kernel object creation (`xTaskCreate`, `xQueueCreate`, timers, event groups) and any
`pvPortMalloc` call can return NULL. Code that ignores it crashes later somewhere unrelated.
The hook catches the failure where it happens.

## Enable
```c
/* FreeRTOSConfig.h */
#define configUSE_MALLOC_FAILED_HOOK 1
```
```c
void vApplicationMallocFailedHook(void)
{
    /* Called from pvPortMalloc in the context of the failing caller. Don't block,
       don't call APIs that allocate, keep it short. */
    taskDISABLE_INTERRUPTS();
    fault_record.reason      = FAULT_HEAP;
    fault_record.task        = pcTaskGetName(NULL);       /* who asked */
    fault_record.free_now    = xPortGetFreeHeapSize();
    fault_record.min_ever    = xPortGetMinimumEverFreeHeapSize();
    fault_record.lr          = (uint32_t)__builtin_return_address(0);
    for (;;) { }   /* let the watchdog reset; fault_record lives in .noinit RAM */
}
```
The hook is called by `heap_1` to `heap_5` when `pvPortMalloc` would return NULL (heap_3
included). It takes no parameters, so it isn't told the requested size; if you need it, wrap `pvPortMalloc` in your own allocator that
records size and caller before calling through.

## Production policy
Halting is right during development. In the field, decide per product:
- Reset and report on next boot (noinit fault record, then upload). Usual choice.
- Return NULL and let callers degrade, if every caller really handles NULL (rare; audit it).

## Sizing the heap with data
```c
HeapStats_t s; vPortGetHeapStats(&s);              /* heap_4 / heap_5 */
printf("free %u min-ever %u largest %u blocks %u\n",
       s.xAvailableHeapSpaceInBytes, s.xMinimumEverFreeBytesRemaining,
       s.xSizeOfLargestFreeBlockInBytes, s.xNumberOfFreeBlocks);
```
- `xMinimumEverFreeBytesRemaining` after a full soak test with every feature exercised is your
  real margin; choose headroom deliberately.
- Large total free but small largest block means **fragmentation**: allocations will fail even
  though "there is memory". Allocate long-lived objects at startup, or use static allocation
  (`configSUPPORT_STATIC_ALLOCATION`) for kernel objects.
- With `configSUPPORT_DYNAMIC_ALLOCATION 0` no heap is used for kernel objects, so the hook is
  not called for them.

## Related hooks
Pair with the stack overflow hook (`configCHECK_FOR_STACK_OVERFLOW`,
`vApplicationStackOverflowHook`); heap_4 also contains `configASSERT` checks on block state.

## Verify
- [ ] Force a failure (allocate in a loop in a test build): hook runs, fault record survives reset.
- [ ] Every kernel create call checks for NULL or `configASSERT`s it.
- [ ] Min-ever-free is reported in telemetry from field units.

## Checked

Checked 2026-10-25 against FreeRTOS-Kernel V11.3.2 (History.txt, released 16 October 2026, current main) and the FreeRTOS Kernel Book source. Confirmed: heap_1 to heap_5 each call vApplicationMallocFailedHook() (void) when the allocation returns NULL and configUSE_MALLOC_FAILED_HOOK is 1; heap_4 calls it after xTaskResumeAll, so the scheduler is not suspended (the skill previously said it might be); vPortGetHeapStats exists only in heap_4 and heap_5; Kernel Book 3.3.6 on the hook. Removed the headroom percentage and the stack-overflow-corrupts-heap claim. 
Method: documentation only; no commands were run.

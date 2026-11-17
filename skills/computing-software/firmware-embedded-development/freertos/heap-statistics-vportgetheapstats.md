---
id: computing-software.firmware-embedded-development.freertos.heap-statistics-vportgetheapstats
name: heap-statistics-vportgetheapstats
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [heap-stats, heapstats-t, xportgetminimumeverfreeheapsize, heap-fragmentation, freertos, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Read FreeRTOS heap statistics (free, minimum-ever free, largest block, allocation counts) to size configTOTAL_HEAP_SIZE and detect leaks and fragmentation."
sources:
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/portable/MemMang/heap_1.c
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/portable/MemMang/heap_2.c
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/portable/MemMang/heap_4.c
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/portable/MemMang/heap_5.c
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/portable.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/task.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Heap statistics

## The calls
| Call | heap_1 | heap_2 | heap_3 | heap_4 | heap_5 |
|---|---|---|---|---|---|
| `xPortGetFreeHeapSize()` | yes | yes | no | yes | yes |
| `xPortGetMinimumEverFreeHeapSize()` | no | no | no | yes | yes |
| `vPortGetHeapStats(HeapStats_t *)` | no | no | no | yes | yes |

heap_3 wraps the C library `malloc`, so none of these calls are provided by it; use your C library's own facilities.

```c
HeapStats_t hs;
vPortGetHeapStats(&hs);
printf("free=%u min=%u largest=%u smallest=%u blocks=%u allocs=%u frees=%u\n",
       (unsigned)hs.xAvailableHeapSpaceInBytes,
       (unsigned)hs.xMinimumEverFreeBytesRemaining,
       (unsigned)hs.xSizeOfLargestFreeBlockInBytes,
       (unsigned)hs.xSizeOfSmallestFreeBlockInBytes,
       (unsigned)hs.xNumberOfFreeBlocks,
       (unsigned)hs.xNumberOfSuccessfulAllocations,
       (unsigned)hs.xNumberOfSuccessfulFrees);
```
`vPortGetHeapStats` in heap_4 walks the free list with the scheduler suspended; call it from a
low-priority diagnostics task or shell command, not a tight loop.

## Reading the numbers
- **Sizing:** run every feature at worst case for a long time, then set
  `configTOTAL_HEAP_SIZE` from the observed peak use (`configTOTAL_HEAP_SIZE` minus
  `xMinimumEverFreeBytesRemaining`) plus a margin you choose. The minimum-ever value is the
  number that captures the peak.
- **Leak:** `allocs - frees` grows steadily in steady state, and free size trends down.
- **Fragmentation:** free total is large but `largest block` is small and `free blocks` count is
  high. Allocations bigger than the largest block fail even with plenty "free". Cures: allocate
  long-lived objects at startup, use fixed-size pools for churny objects, or switch to static
  allocation.
- **Heap exhausted at boot:** compare startup allocations with heap size; task stacks
  (`depth * sizeof(StackType_t)`) plus TCBs usually dominate.

## Exposing it
- A shell `heap` command printing the struct.
- Periodic telemetry of `free`, `min_ever`, `largest` so field devices reveal slow leaks.
- Pair with `vApplicationMallocFailedHook` so an actual failure is caught at the call site.

## Gotchas
- The stack depth passed to `xTaskCreate` is in **words** (StackType_t), not bytes; heap stats
  are in bytes.
- Allocations made by the C library (printf buffers, newlib) don't appear here unless malloc is
  routed to pvPortMalloc.
- Sizes include a per-block header (`xHeapStructSize` in heap_4) and alignment padding.

## Verify
- [ ] Heap size justified by a recorded minimum-ever-free figure from a soak test.
- [ ] Alloc/free counters stable over a 24 h soak.

## Checked

Checked 2026-10-25 against FreeRTOS-Kernel V11.3.2 (History.txt, released 16 October 2026, current main) and the FreeRTOS Kernel Book source. Confirmed: the function table (xPortGetFreeHeapSize in heap_1, heap_2, heap_4 and heap_5; xPortGetMinimumEverFreeHeapSize and vPortGetHeapStats only in heap_4 and heap_5, none in heap_3, checked by searching each heap file; the skill previously listed vPortGetHeapStats for heap_2, which was wrong); HeapStats_t members including xSizeOfSmallestFreeBlockInBytes and xNumberOfSuccessfulAllocations (portable.h); heap_4 walks the list under vTaskSuspendAll; stack depth is in words (task.h). Removed the mallinfo advice and the 1.2 sizing multiplier. 
Method: documentation only; no commands were run.

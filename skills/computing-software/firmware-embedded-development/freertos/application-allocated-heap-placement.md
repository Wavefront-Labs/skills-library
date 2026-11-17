---
id: computing-software.firmware-embedded-development.freertos.application-allocated-heap-placement
name: application-allocated-heap-placement
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [application-allocated-heap, configapplication-allocated-heap, ucheap, vportdefineheapregions, linker-section, freertos, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Place the FreeRTOS heap where you want it: configAPPLICATION_ALLOCATED_HEAP with ucHeap in a linker section, or heap_5 regions spanning several RAM banks."
sources:
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/portable/MemMang/heap_4.c
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/portable/MemMang/heap_5.c
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/portable/MemMang/heap_1.c
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/portable/MemMang/heap_2.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Application-allocated heap placement

By default heap_1, heap_2 and heap_4 declare `static uint8_t ucHeap[configTOTAL_HEAP_SIZE];` and the linker
drops it wherever `.bss` goes. On parts with several RAM banks (DTCM, SRAM1/2, external SDRAM),
you usually want to choose.

## Option 1: own the array (heap_1, heap_2, heap_4)
```c
/* FreeRTOSConfig.h */
#define configAPPLICATION_ALLOCATED_HEAP 1
#define configTOTAL_HEAP_SIZE            (64 * 1024)

/* heap_mem.c */
#include "FreeRTOS.h"
uint8_t ucHeap[configTOTAL_HEAP_SIZE] __attribute__((section(".freertos_heap"), aligned(8)));
```
Linker script:
```
.freertos_heap (NOLOAD) :
{
    . = ALIGN(8);
    *(.freertos_heap)
} > RAM_D1
```
With `configAPPLICATION_ALLOCATED_HEAP` set to 1 the heap source declares `ucHeap` as `extern`,
so your own definition must have exactly that name and size. Use your toolchain's mechanism
(linker script, scatter file or section pragma) to place it.

## Option 2: heap_5 across multiple regions
```c
#include "FreeRTOS.h"
static uint8_t heapA[32 * 1024] __attribute__((section(".sram1_bss")));
static uint8_t heapB[96 * 1024] __attribute__((section(".sdram_bss")));

static const HeapRegion_t regions[] = {
    { heapA, sizeof heapA },          /* low to high address order required (this example assumes heapA is the lower) */
    { heapB, sizeof heapB },
    { NULL, 0 }                        /* terminator */
};

int main(void) {
    board_init_sdram();               /* external RAM must work BEFORE this */
    vPortDefineHeapRegions(regions);  /* before ANY pvPortMalloc, incl. xTaskCreate */
    ...
}
```
heap_5 gives no control over which region an allocation lands in. If something (DMA buffers,
task stacks) must be in a particular RAM, allocate it statically there.

## Choosing the bank
- Check your device's reference manual for which RAM banks the DMA engines can reach and which
  are cached before deciding what may live on the heap; keep DMA buffers static in a suitable
  region when in doubt.

## Verify
- [ ] Map file shows `ucHeap` (or heap_5 regions) at the intended addresses.
- [ ] `vPortDefineHeapRegions` called before the first allocation (assert on NULL if not).
- [ ] No DMA buffer comes from a heap placed in DMA-unreachable RAM.

## Checked

Checked 2026-10-25 against FreeRTOS-Kernel V11.3.2 (History.txt, released 16 October 2026, current main) and the FreeRTOS Kernel Book source. Confirmed: with configAPPLICATION_ALLOCATED_HEAP == 1 heap_1, heap_2 and heap_4 declare `extern uint8_t ucHeap[configTOTAL_HEAP_SIZE]` instead of a static array; heap_5 takes a HeapRegion_t array terminated by { NULL, 0 }, in address order low to high, and vPortDefineHeapRegions must be called before any object that allocates is created. Removed toolchain-specific placement notes, the NOLOAD claim and the device-specific DMA and DTCM claims. 
Method: documentation only; no commands were run.

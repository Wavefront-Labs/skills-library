---
id: computing-software.firmware-embedded-development.freertos.heap-schemes-and-memory-management
name: heap-schemes-and-memory-management
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [freertos, heap-1, heap-2, heap-3, heap-4, heap-5, static-allocation, pvportmalloc, vportfree, fragmentation, xportgetfreeheapsize, heap-overflow, configsupport-static-allocation, memory-pool, xtaskcreatestatic, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Pick and verify the right FreeRTOS heap scheme (heap_1..5) for the memory profile, use static allocation to eliminate fragmentation risk, and catch heap corruption before it corrupts something else."
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

# FreeRTOS heap schemes and memory management

**Goal:** choose the heap implementation that matches the product's memory
behavior, and know when to skip dynamic allocation entirely — extending
`computing-software.firmware-embedded-development.freertos.task-and-queue-design`'s
stack-sizing advice to the heap side of RTOS memory.

## The five heap schemes, and when each is right
- **heap_1**: the simplest possible implementation; allocated memory can **not** be freed.
  Only viable if nothing is ever freed for the product's life (all tasks and queues
  created once at boot and never deleted).
- **heap_2**: allocate and free, but adjacent free blocks are not combined, so memory
  will fragment; the file header points to heap_4 as the alternative. Avoid in new projects.
- **heap_3**: wraps the toolchain's `malloc`/`free`, made thread-safe by suspending the
  scheduler. It inherits whatever behaviour that allocator has, and the linker must be
  configured to generate a heap area for it; the size is not set by `configTOTAL_HEAP_SIZE`.
- **heap_4**: allocate/free with coalescing of adjacent free blocks, which limits (but does
  not eliminate) fragmentation. It provides `xPortGetFreeHeapSize()` and
  `xPortGetMinimumEverFreeHeapSize()`; watch the *minimum ever* value over a long soak
  test, not just current free, because it reveals the low-water mark that current free hides.
- **heap_5**: like heap_4 but the heap can span multiple non-contiguous blocks (for example
  internal SRAM plus external RAM); the regions are passed to `vPortDefineHeapRegions()`.

## Static allocation: the "don't need a heap at all" option
`configSUPPORT_STATIC_ALLOCATION = 1` enables `xTaskCreateStatic`,
`xQueueCreateStatic`, etc., which take caller-supplied buffers instead of
heap allocations. For a fixed, known-at-compile-time set of tasks/queues
(the common case in a product that doesn't dynamically spin up work), this
removes heap fragmentation and out-of-memory failures for those RTOS objects. Any *application* dynamic allocation (buffers sized at
runtime, variable-length messages) still needs a heap scheme chosen above.

## Detecting heap corruption early
`configCHECK_FOR_STACK_OVERFLOW` catches stack smashes but not a bad pointer write landing
in heap metadata. heap_4 contains `configASSERT` checks (for example that a block being freed
is marked allocated and that returned pointers are aligned), so a build with `configASSERT`
wired to actually halt (not compiled out) can catch some corruption at the next alloc or free
after it. Don't ship `configASSERT` as a no-op in a build still doing active development.

## Verify
- [ ] Heap scheme choice matches the actual free-pattern of the product (never-freed → heap_1 is viable; varied alloc/free sizes → heap_4; split RAM regions → heap_5).
- [ ] `configSUPPORT_STATIC_ALLOCATION` is used for all tasks/queues whose count and size are known at compile time.
- [ ] A multi-hour soak test logs `xPortGetMinimumEverFreeHeapSize()`, not just current free, and it stays above a safety margin.
- [ ] `configASSERT` is wired to a real halt/trap in the build used for soak testing, not compiled to nothing.

## Checked

Checked 2026-10-25 against FreeRTOS-Kernel V11.3.2 (History.txt, released 16 October 2026, current main) and the FreeRTOS Kernel Book source. Confirmed: heap_1 cannot free, heap_2 frees without combining adjacent blocks and names heap_4 as the alternative, heap_3 wraps malloc/free under vTaskSuspendAll and needs a linker-generated heap, heap_4 coalesces, heap_5 spans non-contiguous regions (file headers and heap_3.c/heap_4.c bodies); xPortGetMinimumEverFreeHeapSize semantics (Kernel Book 3.3.3); heap_4 configASSERT checks on block state and alignment. Removed the heap_2 deprecation claim, the heap_3 critical-section claim, the sentinel-field claim and unsupported prevalence and determinism claims. 
Method: documentation only; no commands were run.

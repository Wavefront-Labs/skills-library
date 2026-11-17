---
id: computing-software.firmware-embedded-development.freertos.thread-safe-newlib-malloc
name: thread-safe-newlib-malloc
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [newlib-reentrant, configuse-newlib-reentrant, malloc-lock, newlib-nano, freertos, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Make newlib malloc, printf and errno safe under FreeRTOS: configUSE_NEWLIB_REENTRANT, __malloc_lock hooks, routing malloc to pvPortMalloc, and newlib-nano caveats."
sources:
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/FreeRTOS.h
  - https://sourceware.org/newlib/libc.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thread-safe newlib under FreeRTOS

Newlib keeps global state (errno, stdio buffers, strtok pointer, the malloc arena) in a
`struct _reent`. With several tasks calling `printf`, `malloc` or `strtok`, that shared state
gets corrupted unless you set things up.

## Step 1: per-task reent struct
```c
/* FreeRTOSConfig.h */
#define configUSE_NEWLIB_REENTRANT 1
```
Each task gets its own `struct _reent` and newlib's global `_impure_ptr` has to point at the running task's structure (newlib documents this requirement for multithreaded use). This fixes errno and stdio state per
task. It costs RAM per task; account for it in the heap or static TCB sizing.

## Step 2: lock the malloc arena
Per-task reent does not protect the shared heap. Provide the locking hooks newlib calls:
```c
#include <malloc.h>
#include "FreeRTOS.h"
#include "task.h"

void __malloc_lock(struct _reent *r)   { (void)r; vTaskSuspendAll(); }
void __malloc_unlock(struct _reent *r) { (void)r; (void)xTaskResumeAll(); }
```
Scheduler suspension is enough because malloc is not called from ISRs (and must not be). If
some ISR does call malloc (e.g. a vendor driver), you need a critical section instead, or better,
remove the ISR allocation.

Also supply `_sbrk` bounded by the linker's heap symbols so an exhausted newlib heap returns
NULL instead of growing into stacks.

## Alternative: route malloc to the FreeRTOS heap
Wrap with the linker's `--wrap` option and implement the wrapped functions on top of `pvPortMalloc`. One heap, one set of statistics. `realloc` needs your own implementation. Some
toolchains' internal calls go through `_malloc_r` (newlib documents the `_r` variants); wrap those too.

## Vendor glue
Newlib 3+ documents retargetable locks (`__retarget_lock_*`); vendor tool-chains may generate glue for them, so check your vendor's documentation before writing your own.

## Gotchas
- `printf` from an ISR is never safe, reentrant config or not.
- `configUSE_PICOLIBC_TLS` is a separate FreeRTOS option for picolibc (FreeRTOS.h); don't mix it with the newlib option.

## Verify
- [ ] `configUSE_NEWLIB_REENTRANT 1` and malloc lock hooks (or vendor glue) both present.
- [ ] Stress: two tasks looping malloc/free plus printf for hours, no corruption or hard fault.
- [ ] `_sbrk` returns NULL at the heap limit (test by exhausting it).

## Checked

2026-10-28: confirmed against the FreeRTOS-Kernel sources and headers read this batch: `configUSE_NEWLIB_REENTRANT` and `configUSE_PICOLIBC_TLS` exist in FreeRTOS.h; newlib documents `__malloc_lock`/`__malloc_unlock`, `_sbrk_r`, `_malloc_r`, `__retarget_lock_*`, `_impure_ptr` and `strtok` (libc.html). Removed or rewritten: the 1 KB reent size, `-u _printf_float`, the per-printf stack figure, the STM32CubeIDE glue file name, and the 'kernel 11' version claim.
Method: documentation only; no commands were run.

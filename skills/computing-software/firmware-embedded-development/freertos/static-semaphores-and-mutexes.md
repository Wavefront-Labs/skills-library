---
id: computing-software.firmware-embedded-development.freertos.static-semaphores-and-mutexes
name: static-semaphores-and-mutexes
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [static-semaphore, staticsemaphore-t, xsemaphorecreatemutexstatic, xsemaphorecreatebinarystatic, freertos, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Create FreeRTOS binary, counting, mutex and recursive-mutex semaphores without heap using StaticSemaphore_t buffers, and avoid the lifetime and init-order traps."
sources:
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/semphr.h
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/queue.h
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/FreeRTOS.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static semaphores and mutexes

All four semaphore kinds have a `...Static` creator that takes a caller-owned
`StaticSemaphore_t`. Requires `configSUPPORT_STATIC_ALLOCATION 1`.

```c
static StaticSemaphore_t sBinBuf, sCntBuf, mBusBuf, mRecBuf;
static SemaphoreHandle_t sDataReady, sSlots, mBus, mLog;

void sync_init(void)
{
    sDataReady = xSemaphoreCreateBinaryStatic(&sBinBuf);
    sSlots     = xSemaphoreCreateCountingStatic(4 /*max*/, 4 /*initial*/, &sCntBuf);
    mBus       = xSemaphoreCreateMutexStatic(&mBusBuf);            /* configUSE_MUTEXES 1 */
    mLog       = xSemaphoreCreateRecursiveMutexStatic(&mRecBuf);   /* configUSE_RECURSIVE_MUTEXES 1 */
    configASSERT(sDataReady && sSlots && mBus && mLog);
}
```
These never return NULL for a valid buffer, but keep the assert to catch a NULL buffer pointer.

## Rules
- One `StaticSemaphore_t` per semaphore, with static lifetime. Reusing a buffer for two objects
  corrupts both silently.
- Don't copy a `StaticSemaphore_t` after creation; its address is the handle.
- With a static object the buffer is yours; only reuse it once no task
  can be blocked on or hold the semaphore.
- Create every sync object **before** `vTaskStartScheduler()` or before any task that uses it
  can run. A task taking a NULL handle asserts or hard-faults.

## Wrapping a driver's lock
```c
typedef struct { StaticSemaphore_t buf; SemaphoreHandle_t h; } lock_t;
static inline void lock_init(lock_t *l) { l->h = xSemaphoreCreateMutexStatic(&l->buf); }
```
Embedding the buffer in the driver's own struct keeps RAM accounting per driver and avoids a
global table.

## Gotchas
- Static mutexes still do priority inheritance and still must not be used from ISRs.
- With `configSUPPORT_DYNAMIC_ALLOCATION 0`, any leftover `xSemaphoreCreateMutex()` fails to
  link, which is a useful audit.

## Verify
- [ ] Each semaphore has its own static buffer (grep for duplicate `&...Buf` arguments).
- [ ] All creates happen in an init function called before tasks start.
- [ ] Map file shows no heap use from sync objects.

## Checked

2026-10-28: confirmed against the FreeRTOS-Kernel sources and headers read this batch: `xSemaphoreCreateBinaryStatic`, `xSemaphoreCreateCountingStatic`, `xSemaphoreCreateMutexStatic` and `xSemaphoreCreateRecursiveMutexStatic` take caller-supplied buffers; static creators return NULL for a NULL buffer; `configUSE_MUTEXES` and `configUSE_RECURSIVE_MUTEXES` default 0 (semphr.h, queue.h, FreeRTOS.h). Removed or rewritten: the C++ static-init bullet and the claim that `vSemaphoreDelete` leaves static memory alone.
Method: documentation only; no commands were run.

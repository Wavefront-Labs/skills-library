---
id: computing-software.firmware-embedded-development.freertos.recursive-mutexes
name: recursive-mutexes
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [recursive-mutex, xsemaphorecreaterecursivemutex, xsemaphoretakerecursive, xsemaphoregiverecursive, reentrant-locking, freertos, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Use FreeRTOS recursive mutexes for re-entrant library code that may lock the same resource in nested calls, with the balanced give rule and the design smell they hide."
sources:
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/semphr.h
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/FreeRTOS.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recursive mutexes

**Problem:** `log_write()` takes the flash mutex, then calls `flash_erase()`, which also takes
it. A normal mutex deadlocks the task against itself: the second take blocks forever (or until
timeout) because the holder is the caller.

## API
```c
/* configUSE_RECURSIVE_MUTEXES 1 (configUSE_MUTEXES 1) */
static SemaphoreHandle_t flash_lock;
flash_lock = xSemaphoreCreateRecursiveMutex();

void flash_erase(uint32_t addr) {
    if (xSemaphoreTakeRecursive(flash_lock, pdMS_TO_TICKS(100)) != pdTRUE) { fail(); return; }
    do_erase(addr);
    xSemaphoreGiveRecursive(flash_lock);
}
void log_write(const void *p, size_t n) {
    xSemaphoreTakeRecursive(flash_lock, portMAX_DELAY);
    if (need_erase()) flash_erase(next_sector());   /* nested take: count 2 */
    do_program(p, n);
    xSemaphoreGiveRecursive(flash_lock);            /* count 0: released */
}
```

## Rules
- Use the **Recursive** take/give pair on a recursive mutex.
- The mutex is released only when gives equal takes. Every early `return` path must give.
  A missed give keeps the lock held forever; other tasks time out and the holder doesn't notice.
- Only the owner can take and give a recursive mutex repeatedly; it is released once gives equal takes (semphr.h).
- Static version: `xSemaphoreCreateRecursiveMutexStatic(&buf)`.
- Debug: `xSemaphoreGetMutexHolder()` shows who holds it.

## The smell
Recursive locking often means the lock boundary is in the wrong place. Preferred refactor:
public functions lock, then call internal `_unlocked` versions that assume the lock is held:
```c
void flash_erase(uint32_t a) { lock(); flash_erase_unlocked(a); unlock(); }
void log_write(...)          { lock(); if (...) flash_erase_unlocked(...); ...; unlock(); }
```
This makes lock scope visible and costs less. Keep recursive mutexes for third-party or
callback-heavy code (file systems, network stacks) where you can't control the call graph.

## Verify
- [ ] Every code path between take and give has a matching give (review early returns and error branches).
- [ ] Stress test with the mutex wrapped to assert holder == NULL at task idle points.
- [ ] No plain take/give calls on the recursive handle (grep).

## Checked

2026-10-28: confirmed against the FreeRTOS-Kernel sources and headers read this batch: `xSemaphoreCreateRecursiveMutex`, `xSemaphoreCreateRecursiveMutexStatic`, `xSemaphoreTakeRecursive`, `xSemaphoreGiveRecursive` and `xSemaphoreGetMutexHolder`; the mutex is released only when the owner has given as many times as it took; `configUSE_RECURSIVE_MUTEXES` default 0 (semphr.h, queue.h, FreeRTOS.h). Removed or rewritten: the undefined-behaviour wording for mixed take/give, the ISR claim, the priority-inheritance claim and the no-recursion-depth-API claim.
Method: documentation only; no commands were run.

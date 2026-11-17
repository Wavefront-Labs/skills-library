---
id: computing-software.firmware-embedded-development.freertos.thread-local-storage-pointers
name: thread-local-storage-pointers
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [thread-local-storage-pointers, vtasksetthreadlocalstoragepointer, pvtaskgetthreadlocalstoragepointer, per-task-errno, freertos, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Store per-task data in FreeRTOS thread local storage pointers: configuring the slot count, per-task errno and contexts, and cleanup with deletion callbacks."
sources:
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/task.h
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/FreeRTOS.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thread local storage pointers

**Goal:** per-task values (errno, a library context, a log prefix) reachable from shared code
without passing a handle through every call.

## Enable
```c
/* FreeRTOSConfig.h */
#define configNUM_THREAD_LOCAL_STORAGE_POINTERS  2   /* slots per TCB, each a void* */
```
Each slot costs `sizeof(void*)` in every TCB, so keep the count small and assign indices in a
single header:
```c
enum { TLS_IDX_ERRNO = 0, TLS_IDX_CTX = 1 };
```

## Use
```c
static my_ctx_t ctx;
vTaskSetThreadLocalStoragePointer(NULL, TLS_IDX_CTX, &ctx);  /* NULL = calling task */

/* anywhere in code running on that task */
my_ctx_t *c = pvTaskGetThreadLocalStoragePointer(NULL, TLS_IDX_CTX);
```
Storing an integer: cast through `uintptr_t`, e.g. a per-task errno:
```c
#define my_errno_set(e) vTaskSetThreadLocalStoragePointer(NULL, TLS_IDX_ERRNO, (void *)(uintptr_t)(e))
#define my_errno_get()  ((int)(uintptr_t)pvTaskGetThreadLocalStoragePointer(NULL, TLS_IDX_ERRNO))
```
A creator can also set a slot on another task by passing its handle instead of NULL.

## Cleanup on delete
Free the slot data yourself before `vTaskDelete(NULL)`; the current kernel headers show no delete-callback API for these slots.

## Gotchas
- Not for ISRs: there is no meaningful "current task" there.
- Slots start NULL; shared code must handle an unset slot (e.g. a task created by a library).
- Compiler `__thread`/`_Thread_local` is a separate mechanism needing toolchain and port
  support (`configUSE_C_RUNTIME_TLS_SUPPORT`, default 0 in FreeRTOS.h).
- Newlib's reent struct is handled by `configUSE_NEWLIB_REENTRANT`, not by these slots.

## Verify
- [ ] Indices defined once; `configNUM_THREAD_LOCAL_STORAGE_POINTERS` exceeds the highest index.
- [ ] Two tasks running the same library see their own context (log both pointers).
- [ ] Deleted tasks free their slot data (free heap returns to baseline).

## Checked

2026-10-28: confirmed against the FreeRTOS-Kernel sources and headers read this batch: `configNUM_THREAD_LOCAL_STORAGE_POINTERS` (default 0), `vTaskSetThreadLocalStoragePointer`, `pvTaskGetThreadLocalStoragePointer`, `configUSE_C_RUNTIME_TLS_SUPPORT` default 0 (FreeRTOS.h, task.h). Removed or rewritten: `vTaskSetThreadLocalStoragePointerAndDelCallback` and `configTHREAD_LOCAL_STORAGE_DELETE_CALLBACKS` (absent from the current kernel headers), the 10.6+ version claim and the 'before that task first runs' wording.
Method: documentation only; no commands were run.

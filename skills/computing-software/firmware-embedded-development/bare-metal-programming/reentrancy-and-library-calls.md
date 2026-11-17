---
id: computing-software.firmware-embedded-development.bare-metal-programming.reentrancy-and-library-calls
name: reentrancy-and-library-calls
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [reentrancy, bare-metal-concurrency, newlib-reent, isr-safe-functions, static-locals, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Identify non-reentrant functions (static state, newlib printf/malloc/strtok, errno) and make code safe to call from both ISRs and main or multiple RTOS tasks."
sources:
  - https://sourceware.org/newlib/libc.html
  - https://sourceware.org/git/?p=newlib-cygwin.git;a=blob_plain;f=newlib/README
  - https://pubs.opengroup.org/onlinepubs/9699919799/functions/V2_chap02.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reentrancy and non-reentrant library calls

A function is **reentrant** if it can be interrupted mid-execution and called again (from an ISR
or another task) without corrupting either call. Non-reentrant code works in every unit test and
fails in the field when the timing lines up.

## What breaks reentrancy
- `static` or global state modified without protection (internal buffers, counters, "last
  result" caches).
- Returning pointers to static buffers (`strtok`, `asctime`, `inet_ntoa`, vendor
  `xxx_to_string` helpers).
- Hardware state sequences: selecting a register bank then reading it; two callers interleave.
- Shared peripherals (one SPI used by an ISR and main).

## What the standards and newlib say
- POSIX.1-2017 section 2.9.1 requires its functions to be thread-safe except a listed set that
  "need not be thread-safe". The list includes `asctime`, `ctime`, `gmtime`, `localtime`,
  `getenv`, `setenv`, `inet_ntoa`, `rand`, `drand48`, `strerror`, `strtok`, `setlocale` and
  `system`. Treat each as non-reentrant on any target unless your library documents otherwise.
- newlib's `rand`/`srand` are documented as unsafe for multi-threaded applications and `rand_r`
  as thread-safe. `strtok_r` behaves like `strtok` except that the caller supplies the
  placeholder pointer (`*lasts`).
- newlib's OS-interface layer records `errno` in a reentrancy structure (`struct _reent`): the
  `errno` macro from `errno.h` reads it, and the `_r` cover routines (`_write_r`, `_sbrk_r`, ...)
  take a pointer to that structure.
- `malloc`, `realloc` and `free` (and their `_r` forms) must be protected if several threads can
  call them or they can be called reentrantly: you provide `__malloc_lock(struct _reent *)` and
  `__malloc_unlock(struct _reent *)`; without them the pool may be corrupted. `malloc` may call
  the lock recursively, so the lock must tolerate a thread that already holds it. The default
  versions in the library use the `sys/lock.h` lock API.
- Float formatting needs heap: the newlib README says the default gdtoa conversion sometimes
  requires 16 KB of heap and the legacy ldtoa mallocs about 1 KB. So calling `printf` with floats
  from an ISR while main is inside `malloc` risks heap corruption unless the locks are
  implemented and usable from that context. Keep stdio out of ISRs.
- How your RTOS gives each task its own reentrancy structure and wires the malloc locks is
  RTOS-specific: read its port documentation.

## Making functions safe
1. Prefer pure functions: inputs in, outputs via caller-provided buffers.
2. Move state into a context struct passed by pointer (multi-instance drivers do this).
3. Protect unavoidable shared state with a critical section (short) or mutex (tasks only,
   never in ISRs).
4. ISR boundaries: ISRs only call functions documented as ISR-safe; defer everything else.

## Audit checklist
```sh
arm-none-eabi-nm -S --size-sort app.elf     # symbols with sizes; look for data symbols and check which functions own them
```
Search source for mutable function-local `static` variables, and ISR call graphs for `printf`,
`malloc`, `free`, `strtok`, `rand`, `localtime`, `errno` use.

## Verify
- [ ] Each ISR's call tree contains only ISR-safe functions.
- [ ] `__malloc_lock` is implemented if more than one context allocates.
- [ ] Stress test calling the shared function from main and a fast timer ISR shows consistent results.

## Checked
Checked 2026-11-08 against POSIX.1-2017 XSH section 2.9.1 (Thread-Safety list), the newlib libc
manual (System Calls, `malloc`, `__malloc_lock`, `rand`/`rand_r`, `strtok_r`) and the newlib
README (gdtoa/ldtoa heap use). Removed because no readable page states them: the per-thread
`_impure_ptr`, `strtok` pointer and `rand` seed layout, the `_dtoa_r` name, the FreeRTOS
`configUSE_NEWLIB_REENTRANT` and `heap_useNewlib` notes (the FreeRTOS page was unreadable),
and the claim that newlib-nano's `printf` has the same constraints.
Method: documentation only; no commands were run.

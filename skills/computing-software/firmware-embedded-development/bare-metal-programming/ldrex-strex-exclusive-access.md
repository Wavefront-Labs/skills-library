---
id: computing-software.firmware-embedded-development.bare-metal-programming.ldrex-strex-exclusive-access
name: ldrex-strex-exclusive-access
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [bare-metal-concurrency, ldrex-strex, exclusive-monitor, clrex, atomic-increment, compare-and-swap, cmsis-ldrexw, armv7-m, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Build lock-free atomic operations on Cortex-M3+ with the CMSIS LDREX/STREX intrinsics: retry loops, CLREX, and why the intrinsics are missing on Cortex-M0."
sources:
  - https://arm-software.github.io/CMSIS_5/Core/html/group__intrinsic__CPU__gr.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LDREX/STREX exclusive access

**Goal:** atomic read-modify-write on shared variables without disabling interrupts, so
high-priority ISRs keep zero added latency.

## The pattern
```c
static inline uint32_t atomic_add(volatile uint32_t *p, uint32_t v) {
    uint32_t old, res;
    do {
        old = __LDREXW(p);                /* load and set exclusive monitor */
        res = __STREXW(old + v, p);       /* returns 0 on success, 1 on failure */
    } while (res != 0);
    __DMB();                              /* order with surrounding accesses if used as a lock */
    return old;
}

static inline bool atomic_cas(volatile uint32_t *p, uint32_t expected, uint32_t desired) {
    do {
        if (__LDREXW(p) != expected) { __CLREX(); return false; }
    } while (__STREXW(desired, p) != 0);
    return true;
}
```
The CMSIS intrinsics page documents `__STREXW` (and `__STREXB`, `__STREXH`) as returning 0 when the
store succeeded and 1 when it failed, so a failed store retries the loop. `__CLREX` removes the
exclusive lock created by an LDREX; use it when abandoning a sequence, as in the CAS failure path.

## Rules
- Keep the code between LDREX and STREX tiny: no function calls and as few other memory accesses as possible.
- Byte and halfword variants: `__LDREXB/__STREXB`, `__LDREXH/__STREXH`.
- `__DMB` ensures the apparent order of explicit memory operations before and after it, without
  ensuring their completion.

## Availability
CMSIS marks `__LDREXB/H/W`, `__STREXB/H/W` and `__CLREX` as not available for Cortex-M0,
Cortex-M0+ and SC000. On those cores briefly mask interrupts instead (see
`computing-software.firmware-embedded-development.bare-metal-programming.nesting-safe-irq-save-restore`)
or use a hardware semaphore if the part has one.

## Verify
- [ ] Disassembly of `atomic_add` shows `ldrex`/`strex` with a branch back on failure.
- [ ] Stress test: main loop and a high-rate ISR both increment a counter many times; the final value equals the sum.

## Checked
Method: docs-checked 2026-11-09 against the CMSIS-5 Core "Intrinsic Functions for CPU Instructions" page (`__LDREXB/H/W`, `__STREXB/H/W` return values, `__CLREX`, `__DMB`, Cortex-M0 exclusions) read by search of the saved page.
Removed as unconfirmed: that exception entry or return clears the local monitor, the global-monitor and multi-master discussion, which cores implement the instructions beyond the CMSIS M0 exclusions (ARMv8-M Baseline), the C11 stdatomic code generation statement, the RP2040 spinlock note, and the Arm ARM source (unreadable).

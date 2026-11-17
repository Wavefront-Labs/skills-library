---
id: computing-software.firmware-embedded-development.bare-metal-programming.nesting-safe-irq-save-restore
name: nesting-safe-irq-save-restore
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [irq-save-restore, bare-metal-concurrency, primask, critical-section, nested-critical-section, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Write critical sections that nest safely by saving and restoring PRIMASK (or BASEPRI) instead of unconditionally re-enabling interrupts, with a scoped macro pattern."
sources:
  - https://arm-software.github.io/CMSIS_6/latest/Core/group__Core__Register__gr.html
  - https://github.com/ARM-software/CMSIS_6/blob/main/CMSIS/Core/Include/m-profile/cmsis_gcc_m.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nesting-safe interrupt save and restore

## The bug
```c
void fifo_put(uint8_t b) { __disable_irq(); /* ... */ __enable_irq(); }
void send_frame(void) {
    __disable_irq();
    fifo_put(hdr);        /* re-enables interrupts on return */
    fifo_put(len);        /* now running with interrupts ON inside "critical" code */
    __enable_irq();
}
```
`__enable_irq()` clears PRIMASK unconditionally, so an inner critical section ends the outer one.
The same happens when `fifo_put` is called from startup code that runs with interrupts disabled.

## Save/restore pattern
```c
static inline uint32_t irq_save(void) {
    uint32_t m = __get_PRIMASK();
    __disable_irq();                 /* CPSID i */
    return m;
}
static inline void irq_restore(uint32_t m) {
    __set_PRIMASK(m);                /* restores the previous state, enabled or not */
}

void fifo_put(uint8_t b) {
    uint32_t key = irq_save();
    buf[head] = b; head = (head + 1) & MASK;
    irq_restore(key);
}
```
CMSIS documents `__get_PRIMASK` and `__set_PRIMASK` as MRS and MSR accesses to the 1-bit PRIMASK
register; `__disable_irq` uses `CPSID i` and `__enable_irq` uses `CPSIE i`. PRIMASK set blocks all
exceptions with configurable priority; NMI and HardFault are not blocked. In the CMSIS GCC
header the `MSR primask` inline assembly carries a `"memory"` clobber, so the compiler does not
move memory accesses across it.

## Scoped macro (C)
```c
#define CRITICAL_SECTION() \
    for (uint32_t _k = irq_save(), _once = 1; _once; irq_restore(_k), _once = 0)

CRITICAL_SECTION() { counter++; }
```
`return`, `break` or `goto` out of the block skips the restore. Use only for straight-line code.

## BASEPRI variant (leave high-priority IRQs running)
```c
static inline uint32_t irq_mask_below(uint32_t prio) {
    uint32_t old = __get_BASEPRI();
    __set_BASEPRI_MAX(prio << (8U - __NVIC_PRIO_BITS));  /* only raises the mask, never lowers it */
    return old;
}
static inline void irq_unmask(uint32_t old) { __set_BASEPRI(old); }
```
`__set_BASEPRI_MAX` only increases BASEPRI: it has no effect when the new value is lower than the
current one, so an inner call with a weaker mask leaves the outer mask in place. `__set_BASEPRI`
lowers it again. BASEPRI functions are not available on Cortex-M0, Cortex-M0+ or SC000 (Armv6-M).
The `prio << (8U - __NVIC_PRIO_BITS)` shift is the same conversion CMSIS uses in `NVIC_SetPriority`.

## Verify
- [ ] Grep the code base: no bare `__enable_irq()` outside startup.
- [ ] Unit test: call the function with interrupts already masked; PRIMASK is still 1 afterwards.
- [ ] Measure the longest critical section against your interrupt latency budget.

## Checked
Method: docs-checked 2026-11-09 against the CMSIS-Core "Core Register Access" page (`__get_PRIMASK`, `__set_PRIMASK`, `__disable_irq`, `__enable_irq`, `__get_BASEPRI`, `__set_BASEPRI`, `__set_BASEPRI_MAX`, Cortex-M0 exclusions) read in full, and the CMSIS_6 `cmsis_gcc_m.h` header (memory clobber on MSR primask and basepri_max) and `core_cm4.h` (priority shift by `8U - __NVIC_PRIO_BITS`) read by search.
Removed as unconfirmed: the claim that CPSID needs no ISB and that a pending interrupt is taken within a couple of instructions, the GCC cleanup-attribute and C++ RAII alternatives, and the Arm user-guide source (unreadable).

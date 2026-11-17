---
id: computing-software.firmware-embedded-development.bare-metal-programming.basepri-critical-sections
name: basepri-critical-sections
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [basepri, primask, critical-section, interrupt-masking, basepri-max, nvic-priority, cmsis-core, cortex-m, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Write nestable Cortex-M critical sections with the CMSIS-Core PRIMASK and BASEPRI functions: save and restore, BASEPRI_MAX raise-only behaviour, and cores without BASEPRI."
sources:
  - https://arm-software.github.io/CMSIS_5/Core/html/group__Core__Register__gr.html
  - https://arm-software.github.io/CMSIS_6/latest/Core/group__NVIC__gr.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Critical sections with PRIMASK and BASEPRI

**Goal:** protect shared state with the smallest blast radius: mask only the interrupts that
touch the data, keep time-critical interrupts running, and make sections nest correctly.

## PRIMASK: mask everything configurable
```c
static inline uint32_t cs_enter(void) { uint32_t s = __get_PRIMASK(); __disable_irq(); return s; }
static inline void cs_exit(uint32_t s) { __set_PRIMASK(s); }
```
- CMSIS-Core: PRIMASK is a 1-bit-wide mask; when set it blocks all interrupts apart from NMI and
  hard fault, i.e. all exceptions with configurable priority. `__disable_irq()` sets PRIMASK using
  `CPSID i`; `__enable_irq()` clears it with `CPSIE i`.
- Save the old value and restore it, rather than calling `__enable_irq()` blindly, so sections
  nest and work when called from an already-masked context.
- `__get_PRIMASK` and `__set_PRIMASK` are available on all cores; the BASEPRI functions below are
  marked "not for Cortex-M0, Cortex-M0+, or SC000".

## BASEPRI: mask at or below a priority
CMSIS-Core: BASEPRI defines the minimum priority for exception processing. When it is non-zero it
prevents activation of all exceptions with the same or lower priority level (a numerically equal
or higher value) as the BASEPRI value.
```c
static inline uint32_t cs_enter(uint32_t basepri_value) {
    uint32_t old = __get_BASEPRI();
    __set_BASEPRI_MAX(basepri_value);
    return old;
}
static inline void cs_exit(uint32_t old) { __set_BASEPRI(old); }
```
- `__set_BASEPRI_MAX` only increases the masking: per CMSIS, the value is set only if BASEPRI
  masking is disabled or the new value raises the priority level, and it has no effect when the new
  value is lower than the current one. That makes nested entry safe. Use `__set_BASEPRI` to lower
  it again.
- The value you pass is the raw register value. How many priority bits your device implements and
  where they sit in the register is device-specific (CMSIS exposes `__NVIC_PRIO_BITS`): confirm in
  the device reference manual and read BASEPRI back in the debugger to check it.
- Every interrupt that touches the protected data must have a priority that BASEPRI masks. Check
  at init with `NVIC_GetPriority(irq)`.
- Interrupts that BASEPRI does not mask must not touch the protected data or call code that uses
  these sections.

## Choosing
| Need | Use |
|---|---|
| Core without BASEPRI, or a few cycles of protection | PRIMASK |
| Keep a high-priority IRQ running | BASEPRI |
| Single word shared with an ISR | an atomic operation instead of masking |

## Gotchas
- Keep sections short; the masked time adds directly to interrupt latency. Measure the worst case.
- Check your core's errata list for BASEPRI write behaviour before relying on it immediately
  taking effect (not covered by the pages cited here).

## Verify
- [ ] BASEPRI read back in the debugger has the value you intend.
- [ ] A high-priority interrupt that should stay live still fires during a long critical section.

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed on the CMSIS-Core Core Register and NVIC pages: PRIMASK and BASEPRI semantics, function names, CPSID/CPSIE use, BASEPRI_MAX raise-only rule, availability note for M0/M0+/SC000, NVIC_GetPriority.
Removed because the readable pages do not state them: the left-alignment shift by 8 minus priority bits, ARMv6-M/v8-M mainline specifics, FreeRTOS configMAX_SYSCALL_INTERRUPT_PRIORITY, and the Cortex-M7 erratum 837070 claim. The Arm ARM and the FreeRTOS page returned no readable text.

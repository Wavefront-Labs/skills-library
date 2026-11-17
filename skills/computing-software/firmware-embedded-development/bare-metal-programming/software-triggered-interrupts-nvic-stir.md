---
id: computing-software.firmware-embedded-development.bare-metal-programming.software-triggered-interrupts-nvic-stir
name: software-triggered-interrupts-nvic-stir
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [nvic-set-pending, nvic, stir, software-interrupt, deferred-processing, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Pend an unused peripheral IRQ from code (NVIC_SetPendingIRQ or STIR) to defer work to a lower priority or to exercise an ISR without its peripheral event."
sources:
  - https://arm-software.github.io/CMSIS_6/latest/Core/group__NVIC__gr.html
  - https://github.com/ARM-software/CMSIS_6/blob/main/CMSIS/Core/Include/core_cm4.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Software-triggered interrupts (NVIC_SetPendingIRQ and STIR)

A device-specific interrupt can be made pending by software. This gives bare-metal code a cheap
"bottom half": a high-priority ISR captures data and pends a low-priority interrupt that does the
heavy processing.

## API
```c
NVIC_SetPriority(SWI_IRQn, LOW_PRIO);      /* a priority below the capture ISR; value must fit __NVIC_PRIO_BITS */
NVIC_EnableIRQ(SWI_IRQn);

void ADC_IRQHandler(void) {                /* high priority: fast capture */
    buf[n++] = ADC1->DR;
    if (n == N) { n = 0; NVIC_SetPendingIRQ(SWI_IRQn); }
}
void SWI_IRQHandler(void) { filter_and_publish(); }   /* low priority */
```
Pick an IRQ line whose peripheral you never use, and do not enable the peripheral itself.

CMSIS documents `NVIC_SetPendingIRQ(IRQn)` as setting the pending bit of a device-specific
interrupt; `IRQn` must not be negative, so it cannot pend core exceptions such as PendSV.
`NVIC_GetPendingIRQ`, `NVIC_ClearPendingIRQ` and `NVIC_GetActive` read or clear the matching state.

The Cortex-M3/M4 register block in the CMSIS core header also has a write-only Software Trigger
Interrupt Register, `NVIC->STIR`, at offset 0xE00 with an interrupt-ID field in its low bits
(`NVIC_STIR_INTID_Msk`), so `NVIC->STIR = SWI_IRQn;` pends the same interrupt with one store. Check
that your core's header defines `STIR` before using it.

## Other uses
- **Testing ISRs:** pend the real IRQ to execute the handler path without the peripheral event;
  check `NVIC_GetPendingIRQ` and `NVIC_GetActive`.
- **PendSV** is the core software exception, set with `SCB->ICSR = SCB_ICSR_PENDSVSET_Msk`
  (the CMSIS header defines this mask); an RTOS normally owns it, so use a spare device IRQ
  for your own deferral when an RTOS is present.

## Gotchas
- Clear any stale pending state with `NVIC_ClearPendingIRQ` before enabling the line.
- Pick the priority deliberately: whether the handler runs immediately or after the current
  ISR depends on its priority relative to the running code.

## Verify
- [ ] Toggle a GPIO at entry and exit of both handlers: the low-priority handler runs after the capture ISR returns.
- [ ] `NVIC_GetPendingIRQ(SWI_IRQn)` is 0 after the handler runs.

## Checked
Method: docs-checked 2026-11-09 against the CMSIS_6 NVIC functions page (`NVIC_SetPendingIRQ`, `NVIC_GetPendingIRQ`, `NVIC_ClearPendingIRQ`, `NVIC_GetActive`, `NVIC_EnableIRQ`, `NVIC_SetPriority`, `IRQn` must not be negative) and `core_cm4.h` (`STIR` register at offset 0xE00, `NVIC_STIR_INTID_Msk`, `SCB_ICSR_PENDSVSET_Msk`) read by search.
Removed as unconfirmed: the USERSETMPEND rule for unprivileged STIR writes, Nordic SWI/EGU names, the dual-core doorbell note, tail-chaining and DSB/ISB timing advice, level-sensitive re-pend behaviour, and a fixed priority value of 14 (not valid for every `__NVIC_PRIO_BITS`). The Arm user guide source was unreadable and was dropped.

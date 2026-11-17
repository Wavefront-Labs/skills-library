---
id: computing-software.firmware-embedded-development.bare-metal-programming.interrupt-vector-table-and-nvic-priority
name: interrupt-vector-table-and-nvic-priority
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [bare-metal, cortex-m, nvic, vector-table, interrupt-priority, priority-grouping, preempt-priority, sub-priority, scb-vtor, isr, weak-symbol, default-handler, tail-chaining, late-arrival, cmsis, nvic-setpriority, nvic-enableirq, firmware-embedded-development]
level: advanced
status: draft
description: "Wire and prioritize Cortex-M interrupts from scratch: vector table placement, weak default handlers, NVIC priority grouping (preempt vs sub-priority), and tail-chaining behavior."
sources:
  - https://developer.arm.com/documentation/dui0552/latest
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Interrupt vector table and NVIC priority on bare-metal Cortex-M

**Goal:** get the right ISR to run, at the right priority relative to the others,
without CubeMX/CMSIS hiding what the hardware is actually doing.

## Vector table layout
The vector table is just an array of 32-bit function pointers at a fixed address
(normally the start of flash, or wherever `SCB->VTOR` points). Entry 0 is the
initial stack pointer value, entry 1 is `Reset_Handler`, entries 2+ are
`NMI_Handler`, `HardFault_Handler`, ... then the device-specific IRQs in the
order the reference manual lists them — that order is fixed per MCU family and
must match exactly or interrupt N fires the wrong handler.
```c
__attribute__((section(".isr_vector")))
void (* const vector_table[])(void) = {
  (void*)&_estack, Reset_Handler, NMI_Handler, HardFault_Handler, /* ... */
  USART2_IRQHandler,
};
```
Give every unused entry a `Default_Handler` that spins or resets — an
unpopulated vector table entry (0x00000000 or garbage) jumped-to on a stray
interrupt is a silent hang that looks nothing like its cause.

## Weak symbols so "unused" IRQs still have a home
Declare every possible handler `weak` and aliased to `Default_Handler`, so a
project that never touches `USART2` still has a safe entry, and defining
`USART2_IRQHandler` in your own code overrides it at link time with zero
vector-table editing:
```c
void USART2_IRQHandler(void) __attribute__((weak, alias("Default_Handler")));
```
If you define the handler with a typo in the name, the linker silently keeps the
weak default and your interrupt appears to "not fire" — check `arm-none-eabi-nm
output.elf | grep IRQHandler` to confirm the real one got linked in.

## Relocating the table — `SCB->VTOR`
Bootloaders and apps running from a non-zero flash offset must set `SCB->VTOR`
to the table's actual address before enabling any interrupt, and the table must
itself be aligned to its own size (power of 2) per the architecture reference —
misalignment is a classic silent-fault source after adding a bootloader.

## NVIC priority: preempt vs sub-priority
`NVIC_SetPriority(irq, priority)` takes a single number, but that number is split
by the priority grouping (`NVIC_SetPriorityGrouping`, or `HAL_NVIC_SetPriorityGrouping`)
into **preempt priority** (can this interrupt interrupt a lower-preempt one
already running?) and **sub-priority** (tie-break for pending order at equal
preempt, no actual preemption). Two interrupts with the same preempt priority
never nest regardless of sub-priority — the second waits even if "higher" by
sub-priority. Most Cortex-M3/4/7 implement only 3-4 priority bits (check
`__NVIC_PRIO_BITS` in the CMSIS device header); values are left-shifted into the
top bits, so `NVIC_SetPriority(irq, 1)` on a 4-bit-priority part is priority 16,
not 1 — use `NVIC_EncodePriority()`/`NVIC_SetPriority` from CMSIS rather than
writing the register directly.

## Tail-chaining and late arrival
Back-to-back pending interrupts of equal/lower priority execute without the
usual 6-cycle exception entry/exit overhead ("tail-chaining") — don't assume
every ISR entry costs the full published latency when profiling. "Late arrival"
lets a higher-priority interrupt that arrives during another's entry sequence
preempt before the first handler's body runs.

## Verify
- [ ] Vector table order matches the reference manual's IRQ numbering exactly, checked entry by entry for the chosen MCU.
- [ ] Every IRQ handler name is confirmed linked (not silently aliased to `Default_Handler`) via `nm`/map file.
- [ ] `SCB->VTOR` and table alignment are correct when running from a non-default offset (bootloader present).
- [ ] Priority grouping is set once, early, before any `NVIC_SetPriority` call, and preempt vs sub-priority behavior was tested with two real nested interrupts on a scope/logic analyzer.

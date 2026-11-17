---
id: computing-software.firmware-embedded-development.bare-metal-programming.memory-mapped-register-access-patterns
name: memory-mapped-register-access-patterns
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [bare-metal, mmio, volatile, read-modify-write, bitfields, struct-overlay, bit-banding, atomic-register-access, compiler-reordering, memory-barrier, dsb, isb, dmb, peripheral-register, register-struct, cortex-m, firmware-embedded-development]
level: advanced
status: draft
description: "Access memory-mapped peripheral registers correctly: volatile struct overlays vs raw pointers, read-modify-write races, bit-banding, and when a compiler/CPU memory barrier is actually needed."
sources:
  - https://developer.arm.com/documentation/dui0552/latest
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Memory-mapped register access patterns

**Goal:** read and write peripheral registers in a way that does what the
datasheet says, not what the compiler decided was equivalent.

## Why `volatile` is non-negotiable
A register access has side effects invisible to the compiler (it changes
hardware state, or its value changes without your code writing it). Without
`volatile`, the compiler may cache a read in a register across loop iterations,
reorder it past other code, or eliminate a "dead" write entirely:
```c
#define GPIOA_ODR (*(volatile uint32_t*)0x40020014)
```
Casting away `volatile` to "simplify" code, or reading through a non-volatile
pointer alias to the same address, reintroduces the bug — the qualifier lives on
the access, not the address.

## Struct overlay vs raw pointer macros
CMSIS-style device headers overlay a `volatile`-qualified struct onto the
peripheral base address:
```c
typedef struct { volatile uint32_t MODER, OTYPER, ... } GPIO_TypeDef;
#define GPIOA ((GPIO_TypeDef*)0x40020000)
```
This gives named-field access (`GPIOA->MODER`) and lets the compiler check types,
but it depends on the struct's layout exactly matching the hardware's register
offsets and padding — a hand-rolled header with one wrong-sized field after it
shifts every subsequent register silently. Prefer the vendor's CMSIS header over
writing your own unless you have a specific reason not to.

## Read-modify-write races
`GPIOA->ODR |= (1 << 5)` is read, OR, write — three instructions, not one. If an
ISR modifies the same register between your read and write, its change is lost
(classic lost-update race). For single-bit pin sets, use the hardware's
dedicated set/reset register where it exists (`GPIOA->BSRR` on STM32: writing a
bit to the upper or lower half atomically sets or clears, no RMW) instead of
RMW on `ODR`. Where no atomic set/clear register exists, disable the specific
interrupt (or use `LDREX`/`STREX` exclusive access on Cortex-M3/4/7) around the
RMW sequence.

## Bit-banding (Cortex-M3/M4, where present)
Some Cortex-M3/M4 parts map a region of SRAM/peripheral space through a
"bit-band alias" where each word corresponds to one bit of the real memory,
giving atomic single-bit set/clear via an ordinary store — check the specific
MCU's memory map; not all Cortex-M parts implement it (M0/M0+/M7 generally
don't), and ST/NXP/TI documentation differs on which regions are bit-banded.

## Memory barriers: when the CPU itself reorders you
`volatile` stops the *compiler* reordering; it does not stop the *CPU's*
write buffer or multiple-outstanding-transaction behavior on a bus. After
writing a register that must take effect before the next instruction (e.g.
disabling a peripheral clock right before a sleep instruction, or updating
`SCB->VTOR` before enabling interrupts), insert `__DSB()` (data synchronization
barrier, waits for memory accesses to complete) and `__ISB()` (instruction
synchronization barrier, flushes the pipeline so following instructions see the
new state) from CMSIS. Skipping this is a real source of "it works 99% of the
time" bugs around clock/power domain changes.

## Verify
- [ ] Every peripheral register access goes through a `volatile`-qualified pointer or struct, no cached non-volatile alias exists.
- [ ] Any bit set/clear shared with an ISR uses an atomic set/reset register or exclusive-access instructions, not bare RMW.
- [ ] Barriers (`__DSB`/`__ISB`) are present after any write whose effect must be visible before the next instruction (clock gating, VTOR, sleep entry).
- [ ] Device header struct offsets spot-checked against the reference manual for at least one register per peripheral used.

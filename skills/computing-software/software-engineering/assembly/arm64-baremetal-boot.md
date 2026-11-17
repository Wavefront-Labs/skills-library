---
id: computing-software.software-engineering.assembly.arm64-baremetal-boot
name: arm64-baremetal-boot
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, arm64-baremetal-boot, asm-baremetal]
level: sme
status: draft
description: "AArch64 bare-metal boot on the QEMU virt machine: entry state, stack setup, UART output, exception levels, vector table and enabling FP/SIMD."
sources:
  - https://developer.arm.com/documentation/ddi0487/latest
  - https://llvm.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# AArch64 boot: exception levels and vector table
**Goal:** run your own AArch64 code with no OS.

```asm
// boot.S
    .section .text.boot
    .globl _start
_start:
    mrs   x0, mpidr_el1
    and   x0, x0, #0xff
    cbnz  x0, park                // only core 0 continues
    adrp  x1, stack_top
    add   x1, x1, :lo12:stack_top
    mov   sp, x1
    mrs   x2, cpacr_el1
    orr   x2, x2, #(3 << 20)      // allow FP/SIMD at EL1/EL0
    msr   cpacr_el1, x2
    isb
    mov   x3, #0x09000000         // PL011 UART base on QEMU virt
    mov   w4, #'H'
    strb  w4, [x3]
    mov   w4, #'i'
    strb  w4, [x3]
park:
    wfe
    b     park
    .section .bss
    .balign 16
    .space 4096
stack_top:
```
```sh
aarch64-linux-gnu-gcc -c boot.S -o boot.o
aarch64-linux-gnu-ld -Ttext=0x40080000 boot.o -o kernel.elf
qemu-system-aarch64 -M virt -cpu cortex-a57 -nographic -kernel kernel.elf
```
- QEMU `virt` places RAM at `0x40000000` and the first PL011 UART at `0x09000000`; writing bytes to its data register prints them without further setup.
- Read `CurrentEL` (`mrs x0, CurrentEL`; the level is in bits [3:2]) to learn the entry exception level; QEMU boots `-kernel` images in EL1 unless virtualization or secure mode is requested.
- Install exception handlers by writing the 2 KiB-aligned vector table address to `VBAR_EL1`; it has 16 slots of 128 bytes each.
- Real boards differ in addresses and entry state (firmware, boot protocol); read the board documentation.

## Gotchas
- Not enabling FP/SIMD traps any floating-point or NEON instruction (compilers use them even for memcpy).
- Park secondary cores; they all start executing at the same entry on many systems.

## Self-check
Run the sample, see "Hi", then read CurrentEL and print it as a digit.

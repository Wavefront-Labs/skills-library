---
id: computing-software.software-engineering.assembly.instruction-encoding-basics
name: instruction-encoding-basics
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, instruction-encoding-basics, asm-concepts]
level: intro
status: draft
description: "How instructions are encoded: variable-length x86-64 (prefix, REX, opcode, ModRM, SIB) versus fixed 32-bit AArch64, with worked byte examples."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
  - https://developer.arm.com/documentation/ddi0487/latest
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Instruction encoding basics
**Goal:** read raw instruction bytes and understand why disassembly needs a known start address.

- x86-64 instructions are 1 to 15 bytes: optional legacy prefixes, REX (0x40-0x4F), opcode, ModRM, optional SIB, displacement, immediate.
- AArch64 instructions are always 4 bytes, aligned, little-endian words.
```
x86-64:  C3                ret
         55                push rbp
         48 89 E5          mov rbp, rsp
         31 C0             xor eax, eax
         B8 01 00 00 00    mov eax, 1
AArch64: D65F03C0          ret
         D503201F          nop
```
- REX.W (0x48 prefix on 64-bit ops) selects 64-bit operand size; REX.R/X/B extend register fields to reach r8-r15.
- Because x86 is variable length, starting a disassembly mid-instruction yields different but valid-looking instructions.
- A64 immediates are small bit-fields; large constants are built with `movz`/`movk` or loaded from a literal pool.

## Gotchas
- The same mnemonic can have several encodings (`mov r64, imm32` sign-extended vs `mov r64, imm64`); assemblers pick the shortest unless forced.
- Verify any byte pattern you rely on against the SDM opcode map or `objdump -d`; do not trust memory for rarely used opcodes.

## Self-check
Assemble a three-line function, run `objdump -d`, and match each byte group to prefix/opcode/ModRM.

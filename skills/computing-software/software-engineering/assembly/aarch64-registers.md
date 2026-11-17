---
id: computing-software.software-engineering.assembly.aarch64-registers
name: aarch64-registers
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, aarch64-registers, asm-arm64-registers]
level: intro
status: docs-checked
description: "AArch64 register file: X0-X30 and W views, SP, link register X30, frame pointer, scratch and platform registers, and the vector registers."
sources:
  - https://github.com/ARM-software/abi-aa/blob/main/aapcs64/aapcs64.rst
  - https://sourceware.org/binutils/docs/as/AArch64_002dRegs.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# AArch64 registers
**Goal:** know what each name refers to and what role the ABI gives it.

- 31 general-purpose registers `r0`-`r30`, written `x0`-`x30` for 64-bit access and `w0`-`w30` for 32-bit access. A separate stack pointer `sp` can be used with only a restricted set of instructions.
- AAPCS64 gives roles to some of them: `x8` indirect result location, `x16` (IP0) and `x17` (IP1) intra-procedure-call temporaries, `x18` the platform register (if the platform needs one), `x29` the frame pointer (FP) and `x30` the link register (LR). The special names are meant for those roles only; disassemblers should print the architectural names.
- `bl` and `blr` put the return address in `x30`.
- One status register, NZCV, holds the condition flags.
- 32 SIMD/FP registers `v0`-`v31`. The `q`, `d` and `s` views of one register all refer to the same entry in the register bank, unlike AArch32 where narrower views overlap several registers.
- Register names may be written in upper or lower case in assembly.

## Gotchas
- The exact encodings, the zero register and instruction aliases are defined in the Arm Architecture Reference Manual (the GNU assembler manual points there); this skill does not restate them.
- Use the ABI role names only when a register is acting in that role.

## Self-check
Disassemble a small function and map every register in it to its AAPCS64 role.

## Checked
2026-11-02. Checked against AAPCS64 (abi-aa, aapcs64.rst: general-purpose register table and notes, SIMD and floating-point registers) and the GNU as AArch64 "Register Names" page (defers to the Arm ARM). Removed: the zero register/`sp` register-31 behaviour, "writing a `w` register zeroes the upper half", the `adr`-for-PC remark and the alias examples, which are in the Arm Architecture Reference Manual (not readable).

Method: documentation only; no commands were run.

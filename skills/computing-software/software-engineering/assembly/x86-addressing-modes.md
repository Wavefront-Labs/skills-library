---
id: computing-software.software-engineering.assembly.x86-addressing-modes
name: x86-addressing-modes
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, x86-addressing-modes, asm-x86-addressing]
level: practitioner
status: draft
description: "x86-64 memory operand forms base + index*scale + displacement, encoding limits, size specifiers, and operand-size rules."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
  - https://www.nasm.us/doc/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# x86-64 addressing modes
**Goal:** write correct memory operands and know the limits.

- General form: `[base + index*scale + disp]`; scale is 1, 2, 4 or 8; disp is 8 or 32 bit signed; base and index are 64-bit GPRs (32-bit with an address-size prefix).
```nasm
mov eax, [rdi]                ; base only
mov eax, [rdi + 4]            ; base + disp
mov eax, [rdi + rsi*4]        ; array of dwords
mov eax, [rdi + rsi*4 + 16]   ; array field
mov dword [rdi], 0            ; size needed when no register implies it
```
- `rsp` cannot be an index register; `rsp`/`r12` as base forces a SIB byte.
- `rbp`/`r13` as base with no displacement is encoded with a zero disp8.
- Absolute `[disp32]` without a base needs a SIB or RIP-relative form; code in position-independent executables must use RIP-relative.
- Immediate stores need an explicit size (`dword`, `qword`); there is no 64-bit immediate store, only sign-extended imm32.

## Gotchas
- A bare `[rax*2]` has no base and needs a 32-bit displacement; assemblers may rewrite it as `[rax+rax]` (unconfirmed per assembler).
- Unaligned access is legal on x86 but may cost cycles across cache lines.

## Self-check
Rewrite a C loop `sum += a[i]` using one scaled-index operand.

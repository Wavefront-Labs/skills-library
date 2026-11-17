---
id: computing-software.software-engineering.assembly.mov-movzx-movsx
name: mov-movzx-movsx
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, mov-movzx-movsx, asm-x86-integer]
level: practitioner
status: draft
description: "MOV and its extension forms on x86-64: zero and sign extension, 32-bit write zeroing, imm64 and imm32 forms, and partial-register hazards."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
  - https://www.nasm.us/doc/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# MOV, MOVZX, MOVSX
**Goal:** move and widen data with the right instruction and no hidden stalls.

```nasm
mov  eax, 1                 ; also clears upper 32 bits of rax
mov  rax, 0x1122334455667788 ; the only mov with a 64-bit immediate (movabs in objdump/GAS)
mov  qword [rdi], -1        ; imm32 sign-extended to 64 bits
movzx eax, byte [rsi]       ; zero-extend 8 -> 32 (and 64)
movzx eax, word [rsi]
movsx rax, byte [rsi]       ; sign-extend 8 -> 64
movsxd rax, dword [rsi]     ; sign-extend 32 -> 64 (NASM name; GAS: movslq / movsxd)
```
- A 32-bit source needs no `movzx`: `mov eax, [rsi]` already zero-extends into rax.
- `mov` does not change flags; memory-to-memory moves do not exist.
- GAS suffixes: `movzbl`, `movsbq`, `movslq`. Intel syntax uses movzx/movsx/movsxd.

## Gotchas
- `mov al, [x]` merges into rax and creates a dependency on the old rax; prefer `movzx eax, byte [x]`.
- C `char` may be signed or unsigned depending on platform; pick movsx or movzx to match the declared type.

## Self-check
Load a signed byte 0xFF into a 64-bit register both ways and print the two results.

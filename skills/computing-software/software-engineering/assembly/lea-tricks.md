---
id: computing-software.software-engineering.assembly.lea-tricks
name: lea-tricks
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, lea-tricks, asm-x86-addressing]
level: practitioner
status: draft
description: "Use LEA for address and small-constant arithmetic without touching flags, including multiply by 3, 5, 9 and three-operand adds."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# LEA as arithmetic
**Goal:** compute with the address generator when it saves instructions or preserves flags.

- `lea` computes an effective address and stores it in a register; it does not read memory and does not modify flags.
```nasm
lea rax, [rdi + rsi]          ; rax = rdi + rsi (non-destructive add)
lea eax, [rdi + rdi*2]        ; x * 3
lea eax, [rdi + rdi*4]        ; x * 5
lea rax, [rdi*8 + 5]          ; x * 8 + 5
lea rdx, [rax + rcx*4 + 12]   ; array element address
```
- Multiplying by 3, 5 and 9 comes from `x + x*2`, `x + x*4`, `x + x*8`.
- Compilers use `lea` for adds that must not clobber a source or must keep flags intact between a compare and a jump.
- 32-bit destination (`lea eax, ...`) truncates and zero-extends like any 32-bit write.

## Gotchas
- Result wraps modulo 2^64 (or 2^32 with 32-bit destination); no overflow flag.
- Some microarchitectures run complex three-component `lea` slower than a simple one; measure if it is hot (unconfirmed per CPU; see vendor optimisation manuals).

## Self-check
Compute x*10 with two `lea`-based instructions (hint: x*5 then double it).

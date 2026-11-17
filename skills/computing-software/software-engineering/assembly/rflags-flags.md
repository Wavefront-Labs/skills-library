---
id: computing-software.software-engineering.assembly.rflags-flags
name: rflags-flags
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, rflags-flags, asm-x86-registers]
level: practitioner
status: draft
description: "RFLAGS status flags CF ZF SF OF PF AF, which instructions set them, and how conditions combine them for signed and unsigned compares."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# RFLAGS status flags
**Goal:** know which instruction last set the flags you branch on.

- CF carry/borrow (unsigned), ZF zero, SF sign, OF signed overflow, PF parity of low byte, AF auxiliary carry; DF direction (string ops).
- `cmp a, b` computes a-b and discards the result; `test a, b` computes a&b (CF=OF=0).
- Unsigned conditions: `ja`/`jb`/`jae`/`jbe` (CF, ZF). Signed: `jg`/`jl`/`jge`/`jle` (SF, OF, ZF). Equality: `je`/`jne` (ZF).
- `mov`, `lea`, `push`, `pop` do not change flags. `inc`/`dec` change all but CF.
- Shifts by a count of 0 leave flags untouched; logic ops clear CF and OF.
```nasm
cmp rdi, rsi
ja  .unsigned_bigger     ; rdi > rsi as unsigned
jg  .signed_bigger       ; rdi > rsi as signed
```

## Gotchas
- Using `jl` after an unsigned compare is a classic sign bug; pick the condition by data type.
- Anything between the compare and the jump (even `add`) may overwrite flags.
- `adc`/`sbb` consume CF; clear it first (`clc` or `xor`) when starting a chain.

## Self-check
Compare 0xFFFFFFFF with 1 as 32-bit values and explain why `ja` and `jg` disagree.

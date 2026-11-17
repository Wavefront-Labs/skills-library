---
id: computing-software.software-engineering.assembly.cmp-test-jcc
name: cmp-test-jcc
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, cmp-test-jcc, asm-x86-control]
level: practitioner
status: draft
description: "Build conditionals and loops on x86-64 with CMP, TEST and Jcc: condition choice by signedness, zero tests, loop shapes and branch range."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# CMP, TEST and conditional jumps
**Goal:** translate C conditions and loops into compare-and-branch.

```nasm
; size_t count_nonzero(const uint8_t *p, size_t n)  (SysV: rdi, rsi)
count_nonzero:
    xor  eax, eax
    test rsi, rsi
    jz   .done                 ; n == 0
.loop:
    cmp  byte [rdi], 0
    setne dl
    movzx edx, dl
    add  rax, rdx
    inc  rdi
    dec  rsi
    jnz  .loop                 ; dec sets ZF
.done:
    ret
```
- `test r, r` sets ZF if r is zero (shorter than `cmp r, 0`).
- Pick `ja/jb/jae/jbe` for unsigned, `jg/jl/jge/jle` for signed, `je/jne` for equality, `js/jns` for sign, `jo/jno` for overflow.
- Jcc has rel8 (-128..127) and rel32 forms; assemblers choose the size, so far targets only cost code bytes.
- A bottom-tested loop (condition at the end) saves one jump per iteration versus a top-tested loop.

## Gotchas
- `inc`/`dec` do not set CF, so unsigned-carry logic after them is wrong.
- After `dec` or `sub` use `jnz`/`jz`; after `cmp` use the relational forms.

## Self-check
Rewrite the loop as top-tested and compare instruction counts per iteration.

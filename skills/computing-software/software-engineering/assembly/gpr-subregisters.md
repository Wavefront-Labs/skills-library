---
id: computing-software.software-engineering.assembly.gpr-subregisters
name: gpr-subregisters
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, gpr-subregisters, asm-x86-registers]
level: intro
status: draft
description: "x86-64 general-purpose registers and their 32/16/8-bit names, including the zero-extension rule and REX byte-register restrictions."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# General-purpose registers and sub-registers
**Goal:** use the correct register name for each operand width and avoid partial-register surprises.

| 64 | 32 | 16 | 8 low | 8 high |
|----|----|----|-------|--------|
| rax | eax | ax | al | ah |
| rbx | ebx | bx | bl | bh |
| rsi | esi | si | sil | - |
| r8 | r8d | r8w | r8b | - |

- Sixteen 64-bit GPRs: rax rbx rcx rdx rsi rdi rbp rsp r8-r15.
- Writing a 32-bit register zeroes bits 63:32. `mov eax, eax` is a zero-extend; `xor eax, eax` clears all of rax.
- Writing 8-bit or 16-bit sub-registers leaves the remaining bits unchanged (a merge, which can create a dependency on the old value).
- `sil`, `dil`, `bpl`, `spl` and r8b-r15b need a REX prefix; an instruction using REX cannot also name `ah`/`bh`/`ch`/`dh`.
```nasm
mov rax, -1
mov eax, 5        ; rax = 5 (upper half cleared)
mov al, 7         ; rax = 7 (only low byte replaced)
```

## Gotchas
- Prefer 32-bit forms for small constants (`mov eax, 1`): shorter encoding, same result.
- `rsp` is the stack pointer; using it as a general register breaks calls, signals and unwinding.

## Self-check
Predict rax after `mov rax,-1 ; mov ax,0 ; mov eax,eax`, then step in a debugger to confirm.

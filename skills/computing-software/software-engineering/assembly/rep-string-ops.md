---
id: computing-software.software-engineering.assembly.rep-string-ops
name: rep-string-ops
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, rep-string-ops, asm-x86-string-atomic]
level: practitioner
status: draft
description: "x86-64 REP string instructions MOVS, STOS, SCAS, CMPS: register contract, direction flag, ABI rule that DF is clear, and performance notes."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
  - https://gitlab.com/x86-psABIs/x86-64-ABI
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# REP string operations
**Goal:** use rep movs/stos correctly and know when libc is faster.

- Implicit operands: source `rsi`, destination `rdi`, count `rcx`, value in `al/ax/eax/rax`; DF=0 moves upward.
```nasm
cld                       ; make DF explicit when unsure
mov  rcx, rdx             ; byte count
rep  movsb                ; memcpy(rdi, rsi, rcx)

xor  eax, eax
mov  rcx, 128
rep  stosq                ; memset 1024 bytes to zero (8 bytes each)
```
- `repe cmpsb` compares until mismatch or rcx=0; `repne scasb` scans for the byte in `al` (a slow strlen).
- The psABI requires DF clear on function entry and exit; set it with `std` only briefly and `cld` afterwards.
- CPUs advertising ERMS (CPUID leaf 7 EBX bit 9) run `rep movsb` efficiently for medium and large sizes; very small copies have startup cost (microarchitecture dependent).

## Gotchas
- rsi, rdi and rcx are modified; save them if they hold live values.
- Overlapping copies need the right direction (or `memmove` logic).

## Self-check
Implement memcpy with `rep movsb` and benchmark 16, 256 and 64K bytes against libc.

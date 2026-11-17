---
id: computing-software.software-engineering.assembly.sysv-red-zone-alignment
name: sysv-red-zone-alignment
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, sysv-red-zone-alignment, asm-abi-sysv]
level: advanced
status: docs-checked
description: "SysV AMD64 red zone (128 bytes beyond RSP) and the stack alignment rule at function entry: who may use the red zone and how to disable it with GCC."
sources:
  - https://raw.githubusercontent.com/hjl-tools/x86-psABI/master/low-level-sys-info.tex
  - https://gcc.gnu.org/onlinedocs/gcc/x86-Options.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Red zone and stack alignment (SysV)
**Goal:** use scratch stack space safely.

- The 128 bytes beyond `rsp` are the red zone: signal and interrupt handlers do not modify it, so a function may keep data there without adjusting `rsp`. The ABI says leaf functions may use it for their entire frame.
```nasm
leaf:
    mov  qword [rsp-8], rdi     ; red-zone local, no sub rsp needed
    mov  rax, [rsp-8]
    ret
```
- Alignment: `(rsp + 8)` is a multiple of 16 at function entry (32 or 64 if `__m256` / `__m512` is passed on the stack). Equivalently, `rsp` is 16-byte aligned just before a `call`, because the call pushes the 8-byte return address.
- GCC's `-mno-red-zone` stops it generating red-zone code for x86-64.

## Gotchas
- Keep red-zone data only in functions that make no calls: a `call` pushes the return address at `rsp-8`, inside the zone.
- Code that runs where something else may push onto the current stack (so the "not modified by handlers" guarantee does not hold) must not rely on the red zone; compile it with `-mno-red-zone`.

## Self-check
Compile a leaf C function at -O2 and spot `[rsp-N]` accesses without a prior `sub rsp`.

## Checked
2026-11-08. Confirmed against the x86-64 psABI source (red zone 128 bytes, not modified by signal or interrupt handlers, usable by leaf functions; `(%rsp + 8)` multiple of 16/32/64 at entry) and the GCC x86 Options page (`-mno-red-zone`). Removed: the claims that Windows x64 has no red zone, that kernels specifically must build with `-mno-red-zone`, and that `movaps`/`movdqa` fault on misalignment (none of these are on the cited pages).
Method: documentation only; no commands were run.

---
id: computing-software.software-engineering.assembly.jump-tables
name: jump-tables
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, jump-tables, asm-x86-control]
level: advanced
status: draft
description: "Implement a dense switch on x86-64 with a bounds check and a table of relative offsets that is position-independent, plus CET notrack note."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
  - https://www.nasm.us/doc/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Indirect jumps and jump tables
**Goal:** dispatch on a small integer in constant time without absolute addresses.

```nasm
; switch (edi) { case 0..3 } ; default otherwise
    cmp  edi, 3
    ja   .default
    lea  rcx, [rel .table]
    movsxd rax, dword [rcx + rdi*4]
    add  rax, rcx
    jmp  rax                      ; compilers emit "notrack jmp" under -fcf-protection
.table:
    dd .c0 - .table, .c1 - .table, .c2 - .table, .c3 - .table
.c0: ...
```
- Table entries are offsets from the table base, so the table has no relocations and works in PIE and shared objects.
- Keep the table in `.rodata` (or the code section for tiny tables); jumping into data is not executable-safe if data is NX.
- `movsxd` handles negative offsets (targets before the table).
- With CET IBT enabled, each case label reached by an indirect jump needs `endbr64`, unless the `notrack` prefix (3E) is used on the jump; compilers choose `notrack` for switch tables.

## Gotchas
- Sparse cases waste table space; compilers use binary search or hash instead.
- Use the unsigned `ja` bound check so negative selectors also fall to default.

## Self-check
Compile a 4-case C switch at -O2 and compare its table and bounds check to the above.

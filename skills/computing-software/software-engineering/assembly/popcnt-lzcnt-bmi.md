---
id: computing-software.software-engineering.assembly.popcnt-lzcnt-bmi
name: popcnt-lzcnt-bmi
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, popcnt-lzcnt-bmi, asm-x86-bitmanip]
level: practitioner
status: draft
description: "Bit-counting and BMI instructions on x86-64: POPCNT, LZCNT, TZCNT, ANDN, BLSR, BEXTR, PEXT/PDEP, SHLX with CPUID guards."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# POPCNT, LZCNT, TZCNT and BMI1/BMI2
**Goal:** use hardware bit tricks safely.

```nasm
popcnt rax, rdi          ; number of set bits
lzcnt  rax, rdi          ; leading zeros (64 if rdi == 0)
tzcnt  rax, rdi          ; trailing zeros (64 if rdi == 0)
blsr   rax, rdi          ; rdi & (rdi-1): clear lowest set bit
blsi   rax, rdi          ; rdi & -rdi: isolate lowest set bit
andn   rax, rsi, rdi     ; ~rsi & rdi
bextr  rax, rdi, rsi     ; extract bits: start in rsi[7:0], length in rsi[15:8]
pext   rax, rdi, rsi     ; gather bits selected by mask rsi
pdep   rax, rdi, rsi     ; scatter bits to mask positions
shlx   rax, rdi, rcx     ; shift by any register, no flags
```
- Feature bits: POPCNT is CPUID.1:ECX bit 23; BMI1 and BMI2 are leaf 7 EBX bits 3 and 8; LZCNT is in extended leaf 0x80000001 ECX (ABM/LZCNT).
- Iterating set bits: `tzcnt` the index, `blsr` to clear it, loop until zero.
- `lzcnt` and `tzcnt` encode as `rep bsr`/`rep bsf`: on CPUs without the feature they run as `bsr`/`bsf`, which behave differently for zero input and return different values. Guard with CPUID.
- `pext`/`pdep` have been reported slow (microcoded) on AMD Zen 1 and Zen 2; check the target.

## Gotchas
- `bsf`/`bsr` leave the destination undefined for a zero source; `tzcnt`/`lzcnt` define it.
- In C use `__builtin_popcountll`, `__builtin_ctzll` with `-mbmi -mlzcnt`.

## Self-check
Write a loop that sums the indices of set bits in a 64-bit mask and verify against a naive loop.

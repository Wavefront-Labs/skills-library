---
id: computing-software.software-engineering.assembly.arm64-lse-atomics
name: arm64-lse-atomics
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, arm64-lse-atomics, asm-arm64-atomics]
level: advanced
status: draft
description: "AArch64 Large System Extensions atomics: LDADD, SWP, CAS and their acquire/release suffixes, assembling with the right architecture and runtime detection."
sources:
  - https://developer.arm.com/documentation/ddi0487/latest
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# LSE atomics: LDADD, CAS, SWP
**Goal:** single-instruction atomics on ARMv8.1-A and later.

```asm
.arch_extension lse
ldadd  w1, w2, [x0]        // w2 = old [x0]; [x0] += w1
ldadda  w1, w2, [x0]       // with acquire
ldaddl  w1, w2, [x0]       // with release
ldaddal w1, w2, [x0]       // acquire + release
stadd  w1, [x0]            // add without returning old value
swp    w1, w2, [x0]        // swap
cas    w1, w2, [x0]        // compare w1 with [x0]; if equal store w2; w1 = old
casal  x1, x2, [x0]
ldset w1, w2, [x0] ; ldclr w1, w2, [x0] ; ldeor w1, w2, [x0]
```
- Suffixes: `a` acquire, `l` release, `al` both; size suffix `b`, `h` for byte, half (`ldaddb`, `casah`).
- Needs FEAT_LSE: assemble with `-march=armv8.1-a` (or `.arch_extension lse`). On Linux check `getauxval(AT_HWCAP) & HWCAP_ATOMICS`.
- GCC/Clang `-moutline-atomics` (GCC 10+) generates helper functions that pick LSE or exclusives at run time.

## Gotchas
- `cas` overwrites its first operand with the observed value; copy the expected value first if you reuse it.
- Not present on early ARMv8.0 cores; running it there raises SIGILL.

## Self-check
Re-implement the previous exclusive-loop increment with `ldadd` and compare disassembly size.

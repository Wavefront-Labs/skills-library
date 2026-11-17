---
id: computing-software.software-engineering.assembly.ldxr-stxr-exclusives
name: ldxr-stxr-exclusives
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, ldxr-stxr-exclusives, asm-arm64-atomics]
level: advanced
status: draft
description: "AArch64 load/store-exclusive loops with LDXR/STXR and acquire/release variants to build atomic increments and spinlocks, plus monitor limits."
sources:
  - https://developer.arm.com/documentation/ddi0487/latest
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# LDXR/STXR exclusive loops
**Goal:** build atomic read-modify-write with the exclusive monitor on cores without LSE.

```asm
// atomic increment of *x0 (w)
1:  ldxr  w1, [x0]
    add   w1, w1, #1
    stxr  w2, w1, [x0]        // w2 = 0 on success, 1 on failure
    cbnz  w2, 1b
// acquire/release versions
    ldaxr w1, [x0]            // load-acquire exclusive
    stlxr w2, w3, [x0]        // store-release exclusive
    clrex                     // clear the exclusive monitor
```
- `stxr` succeeds only if no other observer wrote the location (or lost the monitor) since the `ldxr`; the status register must differ from the data and address registers.
- The loop may fail spuriously; keep the code between `ldxr` and `stxr` short and free of other memory accesses and system instructions.
- Use `ldaxr`/`stlxr` (or `ldar`/`stlr` for plain acquire/release) to get ordering; plain exclusives give atomicity only.
- On ARMv8.1+ prefer the LSE single-instruction atomics (see arm64-lse-atomics).

## Gotchas
- Accesses must be naturally aligned or the exclusive faults.
- An exception return or `clrex` clears the monitor; debuggers single-stepping the loop can livelock it.

## Self-check
Run the increment from several threads and verify the total.

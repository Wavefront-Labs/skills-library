---
id: computing-software.software-engineering.assembly.arm64-barriers
name: arm64-barriers
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, arm64-barriers, asm-arm64-atomics]
level: advanced
status: draft
description: "AArch64 weak memory model: DMB/DSB/ISB, load-acquire and store-release instructions, and a message-passing example."
sources:
  - https://developer.arm.com/documentation/ddi0487/latest
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# DMB, DSB, ISB and acquire/release
**Goal:** order memory accesses on a weakly ordered CPU.

- AArch64 permits loads and stores to different addresses to be reordered unless you add ordering.
- `dmb ish` orders all prior and later memory accesses in the inner-shareable domain (full barrier for normal SMP code); `dmb ishld` orders prior loads against later loads/stores; `dmb ishst` orders stores.
- `dsb` waits for completion of prior memory accesses (and cache/TLB maintenance); `isb` flushes the pipeline (needed after changing system registers or self-modifying code).
- `ldar`/`stlr` are load-acquire and store-release: cheaper than full barriers for locks and flags.
```asm
// producer
str  w1, [x0]            // data
stlr w2, [x3]            // flag = 1 with release
// consumer
1:  ldar w4, [x3]        // acquire load of flag
    cbz  w4, 1b
    ldr  w5, [x0]        // sees data
```
- C11/C++ `memory_order_seq_cst` loads/stores compile to `ldar`/`stlr` on AArch64.

## Gotchas
- Code that works on x86 because of total-store-order often needs these on ARM.
- `dmb` with the wrong domain/type (`sy`, `ish`, `ld`, `st`) may be too weak or needlessly slow.

## Self-check
Remove `stlr` and `ldar` from the example and try to provoke a stale read with a stress test.

---
id: computing-software.software-engineering.assembly.x86-memory-ordering
name: x86-memory-ordering
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, x86-memory-ordering, asm-x86-string-atomic]
level: advanced
status: draft
description: "The x86-64 memory model (total store order): which reorderings occur, when MFENCE or a locked instruction is needed, and SFENCE/LFENCE roles."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# x86 memory ordering and fences
**Goal:** know exactly which ordering x86 gives for free.

- x86 is TSO-like: loads are not reordered with older loads, stores are not reordered with older stores, and stores are not reordered before older loads.
- The one visible reordering: a load may complete before an older store to a different address (store buffer).
- Locked instructions (`lock`-prefixed, `xchg` with memory) are full barriers; `mfence` is the explicit full barrier.
- `sfence` orders weakly-ordered (non-temporal) stores; `lfence` orders loads and, on current CPUs, serialises instruction execution (used in Spectre mitigations and with `rdtsc`).
```nasm
; sequentially consistent store: use xchg instead of mov + mfence
mov  eax, 1
xchg [rdi], eax
```
- Release stores and acquire loads are plain `mov` on x86; the compiler (not the CPU) must be kept from reordering them.

## Gotchas
- Store-buffer litmus (Dekker) fails without `mfence`/xchg even on x86.
- Non-temporal stores (`movnt*`) are weakly ordered and need `sfence` before publishing.
- Porting to AArch64 breaks code that relied on x86 ordering; see arm64-barriers.

## Self-check
Run the Dekker/store-buffer litmus test, observe both loads reading 0, then fix with xchg.

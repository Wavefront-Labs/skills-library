---
id: computing-software.software-engineering.assembly.segment-fs-gs
name: segment-fs-gs
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, segment-fs-gs, asm-x86-registers]
level: advanced
status: draft
description: "Using the FS and GS segment base registers on x86-64 for thread-local storage and the Windows TEB/PEB, including how to read them in assembly."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
  - https://gitlab.com/x86-psABIs/x86-64-ABI
  - https://learn.microsoft.com/en-us/cpp/build/x64-software-conventions
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# FS/GS segment bases and TLS
**Goal:** access thread-local data via segment-override addressing.

- In 64-bit mode CS/DS/ES/SS bases are treated as zero; FS and GS bases are real and set per thread.
- Linux x86-64 user space: FS base points at the thread control block; the glibc convention is that `fs:0` holds the TCB's own address.
```nasm
mov rax, [fs:0]        ; thread pointer (glibc/psABI TLS convention)
mov eax, [fs:-8]       ; example negative offset to a static TLS variable (offset from the linker)
```
- Windows x64: GS base is the TEB. `gs:[0x30]` is the TEB self pointer and `gs:[0x60]` the PEB pointer in current 64-bit Windows layouts (documented in public TEB/PEB structures; layouts are not a stable API).
- macOS x86-64 uses GS for its thread pointer.
- Set the base from user space on Linux with `arch_prctl(ARCH_SET_FS, addr)` or, where enabled, `wrfsbase`.
- Static TLS offsets are produced by the linker (`@tpoff` relocations); do not hard-code them.

## Gotchas
- A new thread created with raw `clone` must set TLS (`CLONE_SETTLS`) or FS-relative code faults.
- The `fs:`/`gs:` override applies to a single memory operand, not to `lea` results (lea ignores segment bases).

## Self-check
Print `fs:0` in a small program and compare with `pthread_self()`.

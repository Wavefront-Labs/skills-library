---
id: computing-software.software-engineering.assembly.endbr-cet-ibt
name: endbr-cet-ibt
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, endbr-cet-ibt, asm-x86-system]
level: advanced
status: draft
description: "ENDBR64 landing pads for Intel CET indirect-branch tracking: where to place them in hand-written assembly and how objects are marked for CET."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
  - https://sourceware.org/binutils/docs/as/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# ENDBR64 and indirect-branch tracking
**Goal:** keep hand-written assembly compatible with CET-enabled binaries.

- `endbr64` (bytes F3 0F 1E FA) marks a legal target of an indirect `call` or `jmp`. It executes as a no-op on CPUs without CET.
- With IBT enforced, an indirect branch to an address that does not begin with `endbr64` raises a control-protection fault.
```nasm
global my_callback
my_callback:
    endbr64                  ; address-taken or exported function
    ...
    ret
```
- Place it at the start of every function whose address is taken or that is exported (reachable through PLT/function pointers). Direct-call-only local helpers do not need it.
- Compilers emit it automatically with `-fcf-protection` (default on some distribution toolchains).
- CET support is advertised to the loader through a `.note.gnu.property` section in each object; an output is marked CET-capable only if all inputs carry the note. In GAS source the helper header `cet.h` supplies a macro for this (header availability depends on the C library; unconfirmed).
- Switch tables use the `notrack` prefix on the indirect `jmp` rather than `endbr64` on every case.

## Gotchas
- Missing property notes silently disable CET for the whole binary.
- User-space IBT/shadow stack enforcement depends on OS and kernel version; check your platform.

## Self-check
Disassemble a distro-compiled function and find `endbr64` as its first instruction.

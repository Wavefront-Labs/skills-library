---
id: computing-software.software-engineering.assembly.shadow-stack-cfi
name: shadow-stack-cfi
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, shadow-stack-cfi, asm-security]
level: sme
status: draft
description: "Control-flow integrity in hardware and software: Intel CET shadow stack, Arm PAC/BTI/GCS, shadow call stacks and what hand-written assembly must not do."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
  - https://developer.arm.com/documentation/ddi0487/latest
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Shadow stacks and CFI
**Goal:** keep assembly compatible with return-address protection.

- Intel CET shadow stack (SHSTK): `call` pushes the return address on both the normal stack and a separate shadow stack; `ret` compares them and faults on mismatch. Related instructions: `rdsspq` (read shadow stack pointer), `incsspq` (pop entries), `rstorssp`/`saveprevssp` for switching stacks.
- Arm: PAC signs the return address (`paciasp`/`autiasp`), BTI restricts indirect branch targets, and newer Arm architecture revisions add a guarded control stack (FEAT_GCS) as a hardware shadow stack. See pointer-auth-bti.
- Software variants: Clang `-fsanitize=shadow-call-stack` on AArch64 keeps return addresses on a separate stack addressed by `x18` (the platform must reserve `x18`); `-fsanitize=cfi` checks indirect call types and needs LTO.
- Enable on x86 Linux at build time with `-fcf-protection=full`; user-space shadow stack needs both CPU and kernel support (kernel 6.6 or newer; confirm for your distribution).
- Hand-written assembly breaks these protections if it:
  - jumps with a pushed address and `ret` (a ROP-style trick);
  - implements `longjmp`, coroutines or context switches without adjusting the shadow stack;
  - lacks `endbr64` / `bti` landing pads at indirect targets.
```nasm
; coroutine switch must also swap the shadow stack pointer when CET SHSTK is active
; (use the platform's makecontext/swapcontext or adapt using rdsspq/rstorssp)
```

## Gotchas
- Missing property notes disable the feature for the entire process.
- Do not assume CET is on or off; test code with it enabled.

## Self-check
Read the `.note.gnu.property` of a distribution binary with `readelf -n` and identify the SHSTK/IBT bits.

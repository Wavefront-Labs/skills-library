---
id: computing-software.software-engineering.assembly.asm-clobbers-volatile
name: asm-clobbers-volatile
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, asm-clobbers-volatile, asm-inline]
level: advanced
status: docs-checked
description: "Inline asm clobber lists, the memory and cc clobbers, volatile semantics, compiler barriers, red zone caution and asm goto."
sources:
  - https://gcc.gnu.org/onlinedocs/gcc/Extended-Asm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Clobbers and volatile
**Goal:** keep the optimiser from invalidating your assumptions.

```c
#define barrier() __asm__ volatile ("" ::: "memory")    /* compiler-only barrier */
```
- The clobber list can name registers, `"cc"` (condition flags; valid on every target, no effect on some) and `"memory"` (the asm reads or writes memory other than the listed inputs and outputs).
- `volatile` disables optimizations that could remove or merge an asm; asm statements with no output operands and `asm goto` statements are implicitly volatile.
- `asm goto` lets assembly jump to C labels listed in the GotoLabels section.
- The `"redzone"` clobber tells the compiler the assembly may write to the stack red zone (the area below the stack pointer); it is ignored on targets without a red zone.

## Gotchas
- Forgetting `"memory"` lets the compiler cache values across your asm.

## Self-check
Remove `"memory"` from a barrier in a loop that reads a buffer and compare -O2 output.
## Checked
2026-11-02. Confirmed against the GCC manual "Extended Asm" (Qualifiers, Clobbers and Scratch Registers, Goto Labels). Removed: the syscall example, CPU-fence advice, `-mno-red-zone`, version availability claims and frame-register note (not on the page).
Method: documentation only; no commands were run.

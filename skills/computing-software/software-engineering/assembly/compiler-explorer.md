---
id: computing-software.software-engineering.assembly.compiler-explorer
name: compiler-explorer
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, compiler-explorer, asm-reading-output]
level: intro
status: draft
description: "Use Compiler Explorer (godbolt.org) to inspect assembly: choosing compilers and flags, filters, colour mapping, tools like llvm-mca, and avoiding misleading results."
sources:
  - https://gcc.gnu.org/onlinedocs/gcc/Extended-Asm.html
  - https://llvm.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Compiler Explorer workflow
**Goal:** iterate quickly on how a compiler translates code.

- Choose language and compiler (several versions of GCC, Clang, MSVC and others, for x86-64, AArch64 and more), then type flags such as `-O2 -march=x86-64-v3`.
- Output filters hide directives, comment-only lines and unused labels; "Compile to binary" shows what the assembler actually produced. Source lines are colour-matched to assembly.
- Add a second compiler pane or use the diff view to compare versions, optimisation levels or architectures.
- The tools menu offers analysers such as `llvm-mca` for throughput estimates (see llvm-mca).
- Links to sessions can be shared; the project can also be run locally if your code cannot leave your machine.
```c
// make code observable: take inputs from parameters, return a result
int sum(const int *a, int n) { int s = 0; for (int i = 0; i < n; i++) s += a[i]; return s; }
```
Tips:
- A function with constant inputs may fold to a constant; pass values through parameters.
- Unused functions are discarded unless exported; mark them `extern` or non-static.
- Use `-O2` first, then compare `-O3` and `-Os`.
- Match your production flags, including `-march`, or the assembly is not what you ship.

## Gotchas
- Online output shows the compiler's choice, not real performance; measure on hardware.
- Hidden defaults (PIE, stack protector, CET) may differ between your local gcc and the site.

## Self-check
Compare the loop above at -O2 and -O3 and find the vector instructions.

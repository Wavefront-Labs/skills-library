---
id: computing-software.software-engineering.assembly.clang-integrated-as
name: clang-integrated-as
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, clang-integrated-as, asm-llvm]
level: practitioner
status: draft
description: "Assemble .s and .S files with clang's integrated assembler: preprocessing, target triples, cross-assembling for x86-64 and AArch64, and using -fno-integrated-as."
sources:
  - https://llvm.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# clang as the assembler driver
**Goal:** build assembly through clang for any target from one toolchain.

```sh
clang -c add.s -o add.o                          # assemble only, no preprocessor
clang -c add.S -o add.o                          # .S runs the C preprocessor first
clang --target=aarch64-linux-gnu -c a64.s -o a64.o
clang --target=x86_64-pc-windows-msvc -c win.s
clang -x assembler-with-cpp -c file.asm
clang -fno-integrated-as -c add.s                # use the system GNU as instead
clang -S -masm=intel foo.c                       # emit Intel-syntax assembly from C
```
- The integrated assembler is on by default for most targets; it understands GNU as syntax and most directives and macros.
- Uppercase `.S` enables `#include`, `#define` and `#if`, which is how kernels and libc share headers with assembly.
- One clang binary assembles for every enabled backend; choose the target with `--target=<triple>` and CPU features with `-march=`/`-mcpu=`.
- Add `-g` to emit DWARF line info for assembly sources.

## Gotchas
- A few GAS corner cases (complex macros, certain expression forms) differ in LLVM's assembler; check by assembling with both when porting.
- Without the preprocessor (`.s`), `#define` lines are treated as assembler comments or errors.

## Self-check
Assemble one file for x86-64 and AArch64 with the same clang binary and compare `file` output.

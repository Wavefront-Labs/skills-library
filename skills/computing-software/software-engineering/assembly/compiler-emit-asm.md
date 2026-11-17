---
id: computing-software.software-engineering.assembly.compiler-emit-asm
name: compiler-emit-asm
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, compiler-emit-asm, asm-reading-output]
level: intro
status: draft
description: "Produce assembly from C with gcc, clang and MSVC: -S, Intel syntax, noise-reduction flags, objdump interleaving and saving intermediates."
sources:
  - https://gcc.gnu.org/onlinedocs/gcc/Extended-Asm.html
  - https://llvm.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Generating assembly with -S
**Goal:** get readable compiler output for a function.

```sh
gcc -O2 -S foo.c -o foo.s                      # AT&T syntax
gcc -O2 -S -masm=intel foo.c -o foo.s          # Intel syntax
gcc -O2 -S -fverbose-asm foo.c                 # comments naming source variables
gcc -O2 -S -fno-asynchronous-unwind-tables -fcf-protection=none foo.c   # fewer directives
clang -O2 -S foo.c -o foo.s ; clang -O2 -S -emit-llvm foo.c -o foo.ll
gcc -O2 -c -g foo.c && objdump -d -M intel -S --no-show-raw-insn foo.o   # interleave source
gcc -save-temps -O2 foo.c                       # keep .i .s .o
cl /FA /O2 foo.c                                # MSVC listing (.asm); /FAs adds source
```
```c
int f(int x) { return x * 3; }     /* -O2 x86-64: lea eax, [rdi+rdi*2] ; ret */
```
- Add `-march=native` or a target such as `-march=armv8.2-a` to see which instructions the compiler is allowed to use.
- Mark the function of interest `__attribute__((noinline))` so it stays separate, and use `extern` or volatile inputs to prevent constant folding.
- For cross targets use the cross compiler (for example `aarch64-linux-gnu-gcc -S`) or `clang --target=aarch64-linux-gnu -S`.

## Gotchas
- `-O0` output is verbose and not representative of released code.
- Directives starting with `.cfi_` and `.loc` are noise; filter or disable them when reading.

## Self-check
Compile the same function for x86-64 and AArch64 and compare instruction counts.

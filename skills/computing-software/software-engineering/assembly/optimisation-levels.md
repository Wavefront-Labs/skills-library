---
id: computing-software.software-engineering.assembly.optimisation-levels
name: optimisation-levels
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, optimisation-levels, asm-reading-output]
level: practitioner
status: draft
description: "How compiler optimisation levels change generated assembly: -O0 stack-slot code versus -O2 registers, inlining, lea tricks and vectorisation at -O3."
sources:
  - https://gcc.gnu.org/onlinedocs/gcc/Extended-Asm.html
  - https://llvm.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# What -O0 vs -O2 does to code
**Goal:** recognise optimisation effects when reading disassembly.

```c
int add(int a, int b) { return a + b; }
```
`-O0` (x86-64, GCC style): every variable lives in a stack slot.
```nasm
push rbp
mov  rbp, rsp
mov  DWORD PTR [rbp-4], edi
mov  DWORD PTR [rbp-8], esi
mov  edx, DWORD PTR [rbp-4]
mov  eax, DWORD PTR [rbp-8]
add  eax, edx
pop  rbp
ret
```
`-O2`:
```nasm
lea  eax, [rdi+rsi]
ret
```
- `-O0` keeps a debuggable one-to-one mapping from source to code; `-O1/-O2` allocate registers, inline small functions, remove dead code, strength-reduce (multiply by 3 to `lea`), unroll or use `cmov`; `-O3` adds more aggressive vectorisation; `-Os` favours size; `-Og` favours debugging experience.
- Signed overflow is undefined in C, so the optimiser may assume it never happens and delete checks.
- Frame pointers are omitted at `-O2` on most targets (`-fno-omit-frame-pointer` restores them).
- Link-time optimisation (`-flto`) lets inlining cross files, so the function you call may not exist in the output.

## Gotchas
- Debugging optimised code shows variables as "optimized out"; use `-Og` or `-O1 -g`.
- Benchmarks at `-O0` are meaningless.

## Self-check
Compile a sum loop at -O0, -O2 and -O3 and describe the three inner loops.

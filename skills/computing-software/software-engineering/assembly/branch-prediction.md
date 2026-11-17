---
id: computing-software.software-engineering.assembly.branch-prediction
name: branch-prediction
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, branch-prediction, asm-performance]
level: advanced
status: draft
description: "Branch prediction effects in assembly: misprediction cost, predictable versus data-dependent branches, branchless alternatives, indirect branches and the return stack."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
  - https://developer.arm.com/documentation/ddi0487/latest
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Branch prediction and mispredicts
**Goal:** keep hot branches predictable and recognise when to go branchless.

- Modern cores predict direction (taken or not), target, and returns. A misprediction flushes work in flight and costs on the order of 10 to 20 cycles (core dependent).
- A loop branch taken N-1 times is cheap. A branch on random data (for example `if (x[i] < t)` on unsorted input) mispredicts about half the time.
```nasm
; branchless: count elements < t
xor  eax, eax
.l: cmp  qword [rdi], rdx
    setl cl                    ; data-dependent result, no branch
    movzx ecx, cl
    add  eax, ecx
    add  rdi, 8
    dec  rsi
    jnz  .l
```
- Replace unpredictable branches with `cmov`/`csel`/`setcc` or arithmetic masks; keep branches when the condition is almost always one way, because a correct prediction breaks the data dependency.
- Return instructions use a return-address stack; do not `push addr; ret` or manipulate the return address, which causes mispredicts (and breaks shadow stacks).
- Indirect branches (`jmp [table+rax*8]`) predict by history; a polymorphic call site can mispredict frequently.
- Measure with hardware counters: `perf stat -e branches,branch-misses ./prog`.
- Layout: put the likely path as fall-through; compilers use `__builtin_expect` and profile data for this.

## Gotchas
- Branchless versions add work and dependencies; they win only on unpredictable data.
- Benchmarks with repeating data get learned by the predictor; use realistic inputs.

## Self-check
Run the count on sorted versus shuffled data and report branch-miss rates.

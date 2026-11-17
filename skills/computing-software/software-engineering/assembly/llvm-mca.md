---
id: computing-software.software-engineering.assembly.llvm-mca
name: llvm-mca
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, llvm-mca, asm-performance]
level: advanced
status: draft
description: "Estimate loop throughput with llvm-mca: CPU models, iteration counts, MCA-BEGIN/END markers, timeline view, resource pressure and its limits."
sources:
  - https://llvm.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# llvm-mca throughput analysis
**Goal:** get a static estimate of cycles, IPC and bottlenecks for a code block.

```sh
llvm-mca -mtriple=x86_64-unknown-linux-gnu -mcpu=skylake -iterations=100 loop.s
llvm-mca -mcpu=znver3 -timeline -resource-pressure loop.s
llvm-mca -mtriple=aarch64 -mcpu=neoverse-n1 loop.s
clang -O2 -S foo.c -o - | llvm-mca -mcpu=skylake
```
Mark regions inside larger assembly with comments:
```asm
# LLVM-MCA-BEGIN hot_loop
    addsd xmm0, [rdi]
    add   rdi, 8
# LLVM-MCA-END
```
- Output includes Iterations, Instructions, Total Cycles, IPC, Block RThroughput (the lower bound on cycles per iteration), per-instruction latency/throughput, and resource pressure per port.
- `-timeline` shows each instruction's dispatch, execute and retire cycles; useful for spotting dependency stalls.
- It simulates the block repeated in a loop with perfect caches and perfect branch prediction. It does not model memory misses, front-end effects or taken-branch costs.
- Pick the CPU model closest to your target with `-mcpu`; `-mcpu=help` lists available names.
- Compiler Explorer integrates `llvm-mca` as a tool for compiled code.

## Gotchas
- Results are only as good as the scheduling model for that CPU; compare with real measurements.
- Include the loop-carried instructions (the counter increment and branch) or the dependency chain is incomplete.

## Self-check
Run the 1-accumulator and 4-accumulator loops from latency-throughput and compare predicted cycles.

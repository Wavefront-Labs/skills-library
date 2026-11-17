---
id: computing-software.software-engineering.assembly.latency-throughput
name: latency-throughput
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, latency-throughput, asm-performance]
level: advanced
status: draft
description: "Model instruction latency, reciprocal throughput and dependency chains: multiple accumulators, loop-carried dependencies and where to find per-CPU numbers."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
  - https://developer.arm.com/documentation/ddi0487/latest
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Latency, throughput and dependencies
**Goal:** predict loop speed from the critical dependency chain.

- Latency is cycles from inputs ready to result ready; reciprocal throughput is cycles between independent issues of the same instruction. Out-of-order cores overlap independent work, so a loop is limited by whichever is larger: the longest loop-carried dependency chain, or total work divided by issue/port capacity.
```nasm
; one accumulator: bound by add latency every iteration
.l: addsd xmm0, [rdi]
    add   rdi, 8
    dec   rsi
    jnz   .l
; four accumulators hide the latency
.l4: addsd xmm0, [rdi]
     addsd xmm1, [rdi+8]
     addsd xmm2, [rdi+16]
     addsd xmm3, [rdi+24]
     add   rdi, 32
     sub   rsi, 4
     jnz   .l4
; then add xmm0..xmm3 together after the loop
```
- Floating-point add/multiply latency is several cycles on current cores, while integer add is one; the exact values depend on the CPU, so look them up: uops.info and Agner Fog's instruction tables for x86, and the Arm Software Optimization Guide for each core.
- Division, square root and `cpuid` are slow; some instructions run only on certain ports.
- Zeroing idioms (`xor eax, eax`, `pxor xmm0, xmm0`) break dependencies; partial register writes can add them.
- Re-associating floating-point sums changes rounding; compilers need `-ffast-math` or `-fassociative-math` to do it for you.

## Gotchas
- Counting instructions without accounting for chains gives wrong estimates.
- Hyper-threading siblings share ports.

## Self-check
Time the one- and four-accumulator loops on a 1 MB array in L2 and compute cycles per element.

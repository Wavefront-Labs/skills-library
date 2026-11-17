---
id: computing-software.software-engineering.assembly.rdtsc-timing
name: rdtsc-timing
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, rdtsc-timing, asm-x86-system]
level: advanced
status: draft
description: "Read the x86 time-stamp counter with RDTSC/RDTSCP, serialise with LFENCE or CPUID, combine EDX:EAX, and interpret it as a constant-rate counter."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# RDTSC and cycle timing
**Goal:** time short code regions without misleading out-of-order effects.

```nasm
; uint64_t now()
now:
    lfence                 ; wait for prior instructions to complete locally
    rdtsc                  ; edx:eax
    shl  rdx, 32
    or   rax, rdx
    ret
```
- `rdtsc` returns the 64-bit counter split across edx:eax (upper halves of rax/rdx are cleared).
- It is not serialising: it can execute before earlier instructions finish. Use `lfence; rdtsc` to start and `rdtscp; lfence` to stop (rdtscp waits for prior instructions and also returns IA32_TSC_AUX in ecx).
- On modern CPUs the TSC is invariant (CPUID.80000007H:EDX bit 8): it ticks at a constant rate independent of core frequency, so counts are not core cycles. Calibrate against a wall clock if you need seconds.
- Run measurements pinned to one core and repeat many times; report the minimum or a percentile, not a single sample.

## Gotchas
- `rdtsc` may be disabled for user mode (CR4.TSD) or virtualised; the portable alternative is `clock_gettime` via the vDSO.
- Frequency scaling and SMT neighbours add noise.

## Self-check
Time an empty region 1000 times, subtract that overhead from real measurements.

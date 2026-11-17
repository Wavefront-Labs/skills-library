---
id: computing-software.software-engineering.assembly.microbenchmark-asm
name: microbenchmark-asm
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, microbenchmark-asm, asm-profiling]
level: advanced
status: draft
description: "Build a reliable microbenchmark for an assembly routine: avoiding dead-code removal, warm-up, pinning, latency versus throughput variants and statistics."
sources:
  - https://man7.org/linux/man-pages/man2/syscall.2.html
  - https://gcc.gnu.org/onlinedocs/gcc/Extended-Asm.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Microbenchmarking assembly routines
**Goal:** get numbers you can trust.

```c
#include <stdint.h>
#include <stdio.h>
#include <time.h>
extern long my_func(long);                  /* routine under test */

static inline uint64_t now_ns(void) {
    struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t);
    return (uint64_t)t.tv_sec * 1000000000u + t.tv_nsec;
}
int main(void) {
    long acc = 1;
    for (int i = 0; i < 1000; i++) acc = my_func(acc);          /* warm-up */
    uint64_t best = ~0ull;
    for (int rep = 0; rep < 50; rep++) {
        uint64_t t0 = now_ns();
        for (int i = 0; i < 100000; i++) acc = my_func(acc);    /* dependent: measures latency */
        uint64_t dt = now_ns() - t0;
        if (dt < best) best = dt;
    }
    __asm__ volatile ("" : : "r"(acc));                          /* keep the result alive */
    printf("%.2f ns per call\n", best / 100000.0);
}
```
- Dependent chain (output feeds the next input) measures latency; independent calls on different data measure throughput. Report both when relevant.
- Prevent the compiler from deleting or hoisting the call: consume the result and make inputs opaque (an empty asm with `"+r"` constraints, or Google Benchmark's `DoNotOptimize`).
- Pin to one core (`taskset -c 2`), use the performance frequency governor if you can, run many repetitions, and report the minimum or median, not the mean.
- Subtract loop overhead by timing an empty-body version.
- Use hardware counters (`perf stat`) to confirm instructions and cycles per iteration.
- Run on realistic data sizes: cache-resident inputs hide memory effects.

## Gotchas
- Timer resolution and call overhead dominate very short routines; batch many calls per sample.
- Turbo and thermal throttling change results over a long run.

## Self-check
Benchmark a function that adds one to its argument and verify the result is about one cycle of latency plus call overhead.

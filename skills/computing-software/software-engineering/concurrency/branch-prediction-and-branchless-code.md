---
id: computing-software.software-engineering.concurrency.branch-prediction-and-branchless-code
name: branch-prediction-and-branchless-code
category: computing-software
field: software-engineering
product: concurrency
tags: [performance, branch-prediction, branchless-code, branch-mispredictions, perf, cmov]
level: sme
status: draft
description: "Find and fix branch misprediction costs: measure with perf, make data predictable (sorting, partitioning), write branchless code with cmov/masks, and verify the compiler output."
sources: ["https://www.agner.org/optimize/microarchitecture.pdf", "https://perf.wiki.kernel.org/index.php/Tutorial", "https://stackoverflow.com/questions/11227809/why-is-processing-a-sorted-array-faster-than-processing-an-unsorted-array", "https://godbolt.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Branch prediction and branchless code

Modern CPUs speculate past branches; a misprediction flushes the pipeline (~15-20 cycles). In a hot
loop over unpredictable data, mispredictions can dominate run time (the famous "sorted array is 6x
faster" example).

## Measure first
```
perf stat -e branches,branch-misses ./app        # miss rate; > ~2-5% in a hot loop is worth a look
perf record -e branch-misses -g ./app && perf report     # which branches
```
`perf stat --topdown` "bad speculation" share also points here. Microbenchmark with realistic data
distributions: random vs sorted inputs behave completely differently.

## Fixes, in order of preference
1. **Make the data predictable**: sort or partition by the condition first, process each group
   without branching; separate rare cases (error paths) out of the hot loop.
2. **Remove the branch arithmetically**:
   ```c
   // branchy
   if (x >= 128) sum += x;
   // branchless: mask
   int m = -(x >= 128);   sum += x & m;
   // or let the compiler emit cmov
   sum += (x >= 128) ? x : 0;
   ```
   Min/max/abs/clamp usually compile to `cmov`/`csel` or SIMD min/max.
3. **Table lookups** instead of chains of comparisons (small tables in L1).
4. **Vectorise**: SIMD compares produce masks; blend instead of branch (`_mm256_blendv_ps`), and
   compilers auto-vectorise branch-free loops more readily.
5. Hints: C++20 `[[likely]]`/`[[unlikely]]`, `__builtin_expect`, Rust `#[cold]` on error paths. They
   affect code layout, not the dynamic predictor; useful for rare paths.

## Verify the codegen
Check assembly on Compiler Explorer (godbolt.org) or `objdump -d`: compilers may turn a ternary into
a branch, or a branch into `cmov`, depending on flags and cost models. Branchless code is slower
when the branch is highly predictable (it always does both sides' work and creates data
dependencies), so benchmark both with production-like data.

## In managed languages
JIT compilers (HotSpot C2, RyuJIT) also emit cmov and profile-guided layouts; the same data-
predictability techniques work. Python-level code is dominated by interpreter overhead; vectorise
with NumPy (boolean masks) instead.

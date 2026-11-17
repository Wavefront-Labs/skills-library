---
id: computing-software.computer-graphics-engineering.graphics-math.kahan-compensated-summation
name: kahan-compensated-summation
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, numerical-robustness, kahan-summation, compensated-summation, pairwise-summation, reduction, floating-point]
level: practitioner
status: verified
description: "Sum many floats accurately: Kahan and Neumaier compensated summation, pairwise/tree reduction on GPUs, fast-math breaking compensation, and when to accumulate in double."
sources: ["https://en.wikipedia.org/wiki/Kahan_summation_algorithm", "https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html", "https://numpy.org/doc/stable/reference/generated/numpy.sum.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kahan summation

Naive summation of n floats has error growing like O(n eps) in the worst case: adding 0.1f repeatedly in float32 stops increasing at exactly 2,097,152 (2^21, after about 18 million adds; ulp
there is 0.25, so 0.1 is below half an ulp). Measured: naive sum of 1e7 copies of 0.1f is 1.0879e6, Kahan is 1.0e6, double is 1000000.015.

## Kahan
```cpp
float kahanSum(const float* x, size_t n) {
    float sum = 0.0f, c = 0.0f;                  // c accumulates lost low-order bits
    for (size_t i = 0; i < n; ++i) {
        float y = x[i] - c;
        float t = sum + y;
        c = (t - sum) - y;
        sum = t;
    }
    return sum;
}
```
Error bound O(eps) independent of n (plus O(n eps^2)).

## Neumaier (improved Kahan)
Handles terms larger than the running sum:
```cpp
float t = sum + x;
c += fabsf(sum) >= fabsf(x) ? (sum - t) + x : (x - t) + sum;
sum = t;      // final result: sum + c
```

## Fast-math kills it
`-ffast-math`, `/fp:fast`, and shader compilers may simplify `(t - sum) - y` to 0, removing the
compensation. Compile that function with strict FP (`#pragma float_control(precise, on)`,
`__attribute__((optimize("no-fast-math")))`, HLSL `precise`, GLSL `precise` qualifier).

## Alternatives
- **Pairwise / tree reduction**: O(log n eps) error, naturally parallel; GPU reductions and
  `numpy.sum` (pairwise in blocks) already do this.
- Accumulate in **double** for CPU float data: simplest and usually enough.
- Integer/fixed-point accumulation for exact, order-independent results (deterministic GPU sums with
  atomics).

## Graphics uses
Progressive path-tracing accumulation over many samples (per-pixel running mean in float32 drifts:
store sum in float32 with Kahan or in float64, or use incremental mean `m += (x - m) / n`), area/volume
integrals over large meshes, statistics over big images, long simulation time accumulators
(`time += dt`: use a double or integer tick counter).

## Verify
Sum 1e7 copies of 0.1f: naive float result far from 1e6, Kahan within 1 ulp (0.0625 at 1e6) of the double result (measured).

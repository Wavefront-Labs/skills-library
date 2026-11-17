---
id: computing-software.firmware-embedded-development.bare-metal-programming.helium-mve-vectorisation
name: helium-mve-vectorisation
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [helium-mve, cortex-m55, cortex-m85, simd, auto-vectorization, armv8-1m, firmware-embedded-development]
level: sme
status: draft
description: "Use Helium (M-Profile Vector Extension) on Cortex-M55/M85: compiler flags, MVE intrinsics, tail predication loops, beat-wise execution, and context-saving costs."
sources:
  - https://developer.arm.com/Architectures/Helium
  - https://developer.arm.com/documentation/101028/latest/
  - https://developer.arm.com/documentation/ddi0553/latest/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Helium (MVE) vector extension on Cortex-M55/M85

Helium is the ARMv8.1-M vector extension: eight 128-bit Q registers (aliased onto the FPU's
D/S registers), integer MVE-I and optional float MVE-F (f16/f32). Cortex-M55, M85 and M52
implement it.

## Compiler setup
```sh
arm-none-eabi-gcc -mcpu=cortex-m55 -mfloat-abi=hard -O3 ...        # +mve.fp implied by cortex-m55 default
arm-none-eabi-gcc -mcpu=cortex-m55+nomve.fp ...                      # integer MVE only
armclang --target=arm-arm-none-eabi -mcpu=cortex-m55 -O3 ...
```
Check `__ARM_FEATURE_MVE` (1 = integer, 3 = integer + float) in code. GCC 13+/LLVM 15+ give
reasonable auto-vectorisation; inspect with `-fopt-info-vec` (GCC) or `-Rpass=loop-vectorize`.

## Intrinsics with tail predication
```c
#include <arm_mve.h>
void add_f32(const float *a, const float *b, float *y, int n) {
    while (n > 0) {
        mve_pred16_t p = vctp32q(n);              /* lanes still valid */
        float32x4_t va = vldrwq_z_f32(a, p);
        float32x4_t vb = vldrwq_z_f32(b, p);
        vstrwq_p_f32(y, vaddq_x_f32(va, vb, p), p);
        a += 4; b += 4; y += 4; n -= 4;
    }
}
```
With `-O2` the compiler turns this into a **low-overhead loop with tail predication**
(`DLSTP.32 / LETP`): no scalar epilogue for leftovers.

## Performance model
- M55 executes vector instructions in **beats** (32 bits per beat, 2 beats/cycle on M55 for many
  ops): a 128-bit op takes 2 cycles but overlaps with the next instruction. Interleave loads and
  MACs (`VLDRW` then `VFMA`) so they overlap; back-to-back dependent ops stall.
- Use CMSIS-DSP/CMSIS-NN built for Helium before hand-writing intrinsics: most kernels already
  exist (FIR, FFT, matrix, conv).
- Data in DTCM avoids cache misses; Helium gathers/scatters (`vldrwq_gather_offset`) are slow.

## Context switch cost
Q registers share the FP register file, so lazy stacking covers them: an ISR that uses
neither FP nor MVE pays nothing. An RTOS must save S16-S31 (= Q4-Q7) and `VPR` (vector predicate
register) for tasks that use MVE; check your RTOS port supports ARMv8.1-M (FreeRTOS `ARM_CM55`
port, Zephyr).

## Verify
- [ ] Disassembly contains `vldrw`, `vfma`, `dlstp`/`letp` in hot loops.
- [ ] Cycle counts vs scalar build show the expected 2-6x speedup on vectorisable kernels.
- [ ] Results bit-match the scalar reference (or within f32 tolerance for reordered sums).

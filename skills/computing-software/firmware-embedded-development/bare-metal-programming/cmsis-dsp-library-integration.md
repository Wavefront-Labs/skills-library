---
id: computing-software.firmware-embedded-development.bare-metal-programming.cmsis-dsp-library-integration
name: cmsis-dsp-library-integration
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [cmsis-dsp, fpu, fir-filter, fft, signal-processing, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Build and use CMSIS-DSP on Cortex-M: CMake and ARM_MATH options, FIR state and coefficient order, biquad coefficient sign, real FFT lengths and packing, Python prototyping."
sources:
  - https://arm-software.github.io/CMSIS-DSP/latest/
  - https://github.com/ARM-software/CMSIS-DSP
  - https://arm-software.github.io/CMSIS-DSP/latest/group__FIR.html
  - https://arm-software.github.io/CMSIS-DSP/latest/group__BiquadCascadeDF2T.html
  - https://arm-software.github.io/CMSIS-DSP/latest/group__RealFFT.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CMSIS-DSP library

An optimised compute library for Cortex-M and Cortex-A (the "DSP" name is legacy). Kernels cover
basic math, filtering, transforms, statistics, matrix, motor control and more, in f64, f32, f16,
q31, q15 and q7. Most functions use a vectorised version when Helium (M-profile) or Neon
(A-profile) is available.

## Getting it into the build
The standard route is the CMSIS pack with CMSIS-Toolbox or Keil MDK. With CMake, per the README:
- Add the `Source` folder as a subdirectory; for Cortex-M builds define `CMSISCORE` so the CMSIS
  Core includes are found.
- Select a Helium build with `MVEF`, `MVEI` or `HELIUM`; Neon with `NEON` and/or `NEONEXPERIMENTAL`;
  `HOST=ON` for host builds. Installing exports the `CMSISDSP::CMSISDSP` target.
- Recommended compiler flags: `-O3 -ffast-math` (README); the docs page recommends `-Ofast` and
  says to avoid `-fno-builtin` and `-ffreestanding`.
- The README warns that GCC performs poorly on Helium and suggests the Arm compiler.

Optional macros from the docs page: `ARM_MATH_LOOPUNROLL` (manual loop unrolling),
`ARM_MATH_MATRIX_CHECK` (check matrix sizes), `ARM_MATH_BIG_ENDIAN`, `ARM_MATH_HELIUM` (implies
`ARM_MATH_MVEF`, `ARM_MATH_MVEI`, `ARM_MATH_MVE_FLOAT16`), `ARM_MATH_NEON`, and
`ARM_DSP_CUSTOM_CONFIG` to supply your own `arm_dsp_config.h`. For code size, use the
size-specific FFT init functions (for example `arm_cfft_init_1024_f32`) with linker garbage
collection.

## FIR with block processing
```c
void arm_fir_init_f32(arm_fir_instance_f32 *S, uint16_t numTaps,
                      const float32_t *pCoeffs, float32_t *pState, uint32_t blockSize);
void arm_fir_f32(const arm_fir_instance_f32 *S, const float32_t *pSrc,
                 float32_t *pDst, uint32_t blockSize);
```
- Coefficients are stored in time-reversed order: `b[numTaps-1]` down to `b[0]`.
- The state array has `numTaps + blockSize - 1` entries.
- Q15 init requires `numTaps` even and at least 4 (pad odd filters with a zero tap). `arm_fir_q15`
  uses a 64-bit accumulator; the fast Q15 version uses a 32-bit accumulator with one guard bit, so
  scale inputs down by log2(numTaps) bits. `arm_fir_q31` uses an internal 64-bit accumulator.
- Helium f32: the coefficient array length must be a multiple of 4 with the extra entries set to
  0 (keep the true `numTaps` in the init call), and the state buffer is `numTaps + 2*blockSize - 1`.
  Vectorised code may read a few words past a buffer end, so the docs advise padding buffers by
  about three words.

## Biquad cascade (direct form II transposed)
```c
void arm_biquad_cascade_df2T_init_f32(arm_biquad_cascade_df2T_instance_f32 *S,
                                      uint8_t numStages, const float32_t *pCoeffs,
                                      float32_t *pState);
```
- Coefficients per stage: `{b10, b11, b12, a11, a12, b20, ...}`, 5 per stage.
- State is `2*numStages` values.
- The library's difference equation adds `a1*y[n]` and `a2*y[n]` terms. If your design tool uses
  the minus form for feedback, negate `a1` and `a2` before passing them. The page does not mention
  SciPy or MATLAB, so check your tool's convention yourself.

## Real FFT
- `arm_rfft_fast_*` supports lengths 32, 64, 128, ... 4096.
- The float output holds N values for an N-point transform. The DC value is the real part of the
  first complex value; the Nyquist value is packed into the imaginary part of that first complex
  value. Input and output are in normal order (bit reversal is done inside).
- The page shows `arm_rfft_fast_f32(S, p, pOut, tmpbuf, ifftFlag)` and ties the temporary buffer to
  the Neon version. For Q15/Q31 it states the source buffer is modified by the rfft; the float
  page does not say. Check the header of the version you build against.

## Prototype in Python
The `cmsisdsp` Python wrapper (`pip install cmsisdsp`, per the README) closely mirrors the C API,
is NumPy-compatible and supports fixed-point arithmetic, to ease moving from prototype to C.

## Verify
- [ ] Impulse response of the target FIR equals the coefficient vector.
- [ ] Output for a test vector matches the Python model within a stated tolerance.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the CMSIS-DSP documentation main page, the FIR, Biquad DF2T and RealFFT group pages, and the GitHub README. The PyPI page could not be read (challenge page), so the wrapper is described from the README. Removed because the pages do not state them: the `-mcpu`/`-mfpu` link-failure claim, `ARM_MATH_CM4` history, `ARM_MATH_ROUNDING`, the DC/Nyquist `freq_buf[1]` index layout, the 1e-6 tolerance, DWT cycle count and gc-sections map checks, and the claim that SciPy `sos` has the opposite sign.

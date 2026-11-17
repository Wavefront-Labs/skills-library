---
id: computing-software.computer-graphics-engineering.opencv.opencv-universal-intrinsics-and-cpu-dispatch
name: opencv-universal-intrinsics-and-cpu-dispatch
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-build-deploy, universal-intrinsics, cpu-dispatch, simd, ipp, opencv-performance]
level: advanced
status: docs-checked
description: "Speed up OpenCV CPU code: CPU_BASELINE and CPU_DISPATCH build options, OPENCV_CPU_DISABLE for testing fallbacks, and universal intrinsics (vx_load, v_fma) for custom kernels."
sources: ["https://github.com/opencv/opencv/wiki/CPU-optimizations-build-options", "https://docs.opencv.org/4.x/df/d91/group__core__hal__intrin.html", "https://docs.opencv.org/4.x/db/d05/tutorial_config_reference.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SIMD (universal intrinsics) and CPU dispatch

## Build options
```bash
cmake -DCPU_BASELINE=AVX2 -DCPU_DISPATCH=AVX,AVX2 ../opencv
```
- **Baseline** (`CPU_BASELINE`): the minimal required instruction set. The executable will not run if the target
  processor lacks it, so keep it conservative for distributed binaries. Other platforms have their own levels
  (VFPV3 and NEON on ARM, VSX on PowerPC).
- **Dispatch** (`CPU_DISPATCH`): extra code paths compiled in and run only on processors that support them.
  `-DCPU_DISPATCH=` (empty) turns dispatching off.
- On x86_64 the wiki states the default is SSE3 baseline with dispatch for SSE4.2, AVX and AVX2 (the wiki is dated
  2017; read the CMake configuration status for your version).
- `CPU_BASELINE_REQUIRE` / `CPU_DISPATCH_REQUIRE` fail the build if the compiler lacks an optimisation;
  `CV_DISABLE_OPTIMIZATION` disables all explicit optimised code (debugging).
- The CMake status output has a "CPU/HW features" block listing Baseline and Dispatched code generation.
- Runtime override for testing: `OPENCV_CPU_DISABLE=AVX2,AVX` masks those features so the dispatched code does not
  run.
- These options do not control Intel IPP optimisations (the wiki says so explicitly). IPP-related build options are in
  the configuration reference tutorial; check it for your OpenCV version.

## Universal intrinsics for custom kernels (C++)
Include `opencv2/core/hal/intrin.hpp`. The intrinsics page documents one source targeting several instruction
sets (x86 SSE/AVX, ARM NEON and SVE via KleidiCV in 4.11+, RISC-V RVV).
- Load with `vx_load` (use it to get the maximum available register length), `vx_setall_*` to broadcast, store with
  `v_store`.
- Arithmetic is `v_add`, `v_sub`, `v_mul`, `v_div`; `v_fma` is the fused multiply-add.
- 64-bit float vectors are not available in every variant (NEON needs AArch64); check the `CV_SIMD128_64F`
  definition before using them.
- Always write a scalar tail loop for the elements left after the last full vector.

## Verify
Benchmark with `cv::TickMeter` against the scalar version and compare outputs within float tolerance; run once with
`OPENCV_CPU_DISABLE` to test the fallback path.

## Checked
2026-11-01. Confirmed in the OpenCV wiki "CPU optimizations build options", the configuration reference tutorial and
the core HAL intrinsics page: CPU_BASELINE and CPU_DISPATCH semantics, defaults (as of the wiki), the REQUIRE and
CV_DISABLE_OPTIMIZATION options, OPENCV_CPU_DISABLE, the intrinsic names above, 64F note, SVE via KleidiCV in 4.11+.
Removed unconfirmed: AVX512_SKX and NEON_DOTPROD flags, WITH_IPP details, IPPICV/LSB claims, Python
getBuildInformation/checkHardwareSupport/ipp helpers, the saxpy listing using VTraits and CV_SIMD_SCALABLE, the
function-style operator advice (4.8).
Method: documentation only; no commands were run.

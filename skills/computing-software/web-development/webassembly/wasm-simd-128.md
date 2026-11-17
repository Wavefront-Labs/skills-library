---
id: computing-software.web-development.webassembly.wasm-simd-128
name: wasm-simd-128
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasm-simd128, v128-ops, simd-intrinsics, wasm]
level: practitioner
status: docs-checked
description: "Vector instructions"
sources: ["https://emscripten.org/docs/porting/simd.html", "https://github.com/GoogleChromeLabs/wasm-feature-detect", "https://webassembly.github.io/spec/core/syntax/instructions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 128-bit SIMD

Goal: speed numeric loops.
- Enable with `-msimd128`; use `<wasm_simd128.h>` intrinsics or auto-vectorisation.
- Feature detection with `wasm-feature-detect` (`simd()`); ship fallback builds.
- Relaxed SIMD instructions (`relaxed_madd`, `relaxed_swizzle` and others) are in the core spec; `wasm-feature-detect` offers `relaxedSimd()`.
Verify: speedup vs scalar build.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: `-msimd128` and `<wasm_simd128.h>`; `-msimd128` also enables LLVM autovectorisation; `simd()` and `relaxedSimd()` detectors; relaxed instructions in the spec.
Removed or reworded as unconfirmed: the 'confirm status' hedge.
Method: documentation only; no commands were run.

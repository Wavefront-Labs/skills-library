---
id: computing-software.web-development.webassembly.wasm-simd-vs-webgpu-choice
name: wasm-simd-vs-webgpu-choice
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, simd-vs-gpu, workload-fit, transfer-overhead, wasm]
level: practitioner
status: draft
description: "Decision"
sources: ["https://webassembly.github.io/spec/core/", "https://developer.mozilla.org/en-US/docs/WebAssembly", "https://component-model.bytecodealliance.org/", "https://wasi.dev/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CPU SIMD vs GPU

Goal: choose the compute backend.
- Small, latency-sensitive kernels: SIMD; large parallel kernels: GPU; transfers dominate small sizes.
- Profile both; keep CPU fallback.
- Consider battery and thermal limits on mobile.
Verify: chosen path wins on target devices.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*

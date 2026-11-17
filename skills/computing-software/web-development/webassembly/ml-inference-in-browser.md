---
id: computing-software.web-development.webassembly.ml-inference-in-browser
name: ml-inference-in-browser
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, onnxruntime-web, tfjs-wasm-backend, webnn, onnx-runtime-web, wasm-ffmpeg, tfjs-wasm, wasm]
level: practitioner
status: draft
description: "Client-side ML"
sources: ["https://webassembly.github.io/spec/core/", "https://developer.mozilla.org/en-US/docs/WebAssembly", "https://component-model.bytecodealliance.org/", "https://wasi.dev/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ML inference

Goal: run models in the browser.
- ONNX Runtime Web with the Wasm (SIMD, threads) execution provider or WebGPU provider; TF.js WASM backend.
- Measure with real devices; model size dominates load time.
- Check cross-origin isolation for threads.
Verify: inference latency on target hardware recorded.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*

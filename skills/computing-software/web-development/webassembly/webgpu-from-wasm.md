---
id: computing-software.web-development.webassembly.webgpu-from-wasm
name: webgpu-from-wasm
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, webgpu-bindings, wgsl, wgpu-rs, webgpu-wasm, wgpu, compute-shader-wasm, wasm]
level: practitioner
status: docs-checked
description: "GPU compute"
sources: ["https://raw.githubusercontent.com/gfx-rs/wgpu/trunk/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebGPU from Wasm

Goal: use GPU compute from Wasm.
- Rust `wgpu` is a cross-platform, safe, pure-Rust graphics API based on the WebGPU standard. Natively it runs on Vulkan, Metal, D3D12 and OpenGL; on wasm it runs on top of WebGL2 and WebGPU.
- When compiled to WebAssembly and running in a browser, `wgpu` relies on the browser's own WebGPU implementation and passes WGSL shaders straight through, so the browser decides which WGSL features you can use.
- Natively, WGSL is translated by Naga, which may lag the WGSL specification.
- Check browser WebGPU availability at runtime and keep a fallback. Emscripten WebGPU bindings and buffer-mapping specifics are not covered by the source read here.
Verify: compute shader output matches the CPU result.

## Checked

2026-11-08. Confirmed in the wgpu README (searched the introduction, platform table and WGSL-tracking section, lines 8-163; not read end to end).
Removed as unconfirmed: `-sUSE_WEBGPU` and emdawnwebgpu, mapped-range buffer sharing, readback minimisation.
Method: documentation only; no commands were run.

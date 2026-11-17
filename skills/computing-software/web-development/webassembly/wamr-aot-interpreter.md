---
id: computing-software.web-development.webassembly.wamr-aot-interpreter
name: wamr-aot-interpreter
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wamr-iwasm, wamrc-aot, wamr-memory-footprint, wamr, wasm3, wasm-iot, wasm]
level: practitioner
status: docs-checked
description: "Small devices"
sources: ["https://raw.githubusercontent.com/bytecodealliance/wasm-micro-runtime/main/README.md", "https://raw.githubusercontent.com/bytecodealliance/wasm-micro-runtime/main/doc/build_wamr.md", "https://raw.githubusercontent.com/bytecodealliance/wasm-micro-runtime/main/wamr-compiler/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WAMR interpreter and AOT

Goal: run Wasm on constrained devices.
- WAMR offers classic and fast interpreters, AOT (compile with `wamrc`) and JIT (Fast JIT and LLVM JIT) modes; the build can pre-allocate a global heap pool (`WAMR_BUILD_GLOBAL_HEAP_POOL`) and export native APIs.
- Compare footprint to alternatives (wasm3).
Verify: module runs within the device's RAM budget.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: running modes, `wamrc`, `WAMR_BUILD_GLOBAL_HEAP_POOL`.
Removed or reworded as unconfirmed: the typical-use sentence about RTOS and gateways.
Method: documentation only; no commands were run.

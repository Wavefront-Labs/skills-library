---
id: computing-software.web-development.webassembly.wasm-threads-sharedarraybuffer
name: wasm-threads-sharedarraybuffer
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, sharedarraybuffer, wasm-atomics, pthreads-emscripten, wasm-threads, shared-memory-atomics, wasm-simd, wasm]
level: practitioner
status: docs-checked
description: "Parallelism"
sources: ["https://developer.mozilla.org/en-US/docs/WebAssembly/Reference/JavaScript_interface/Memory", "https://developer.mozilla.org/en-US/docs/Web/API/Window/crossOriginIsolated", "https://emscripten.org/docs/porting/pthreads.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Threads and atomics

Goal: use threads.
- Needs a shared `WebAssembly.Memory` (backed by a `SharedArrayBuffer`) and cross-origin isolation: `Cross-Origin-Opener-Policy: same-origin` and `Cross-Origin-Embedder-Policy: require-corp`.
- Emscripten `-pthread -sPTHREAD_POOL_SIZE=4`.
Verify: `crossOriginIsolated` is true and threads run.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: shared memory; COOP/COEP values; `crossOriginIsolated`; `-pthread` and `-sPTHREAD_POOL_SIZE=<expression>`.
Removed or reworded as unconfirmed: the atomic wait/notify instruction names (not in the core spec page read).
Method: documentation only; no commands were run.

---
id: computing-software.web-development.webassembly.wasm-in-web-workers
name: wasm-in-web-workers
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, web-worker-wasm, offscreencanvas, comlink, wasm-web-workers, audioworklet-wasm, wasm-webgl, wasm]
level: practitioner
status: docs-checked
description: "Run WebAssembly in Web Workers: send a compiled Module via postMessage, instantiate there, and render with OffscreenCanvas."
sources:
  - https://developer.mozilla.org/en-US/docs/WebAssembly/Reference/JavaScript_interface/Module
  - https://developer.mozilla.org/en-US/docs/Web/API/OffscreenCanvas
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running Wasm in workers

Goal: avoid blocking the UI.
- A `WebAssembly.Module` holds already-compiled, stateless Wasm code that can be shared with workers via `postMessage()` and instantiated multiple times. Compile on the main thread (for example with `WebAssembly.compileStreaming()`), `worker.postMessage(mod)`, then in the worker call `WebAssembly.instantiate()` on the received module.
- `OffscreenCanvas` can render inside a worker, keeping heavy drawing off the main thread; it is a transferable object.
- Sharing memory between threads with `SharedArrayBuffer` needs a secure context and cross-origin isolation (see serving-wasm-correctly).
Verify: the UI stays responsive during heavy computation.

## Checked
Read the intro and the "Sending a compiled module to a worker" example of the MDN WebAssembly.Module page, the intro of the OffscreenCanvas page, and the security-requirements section of the SharedArrayBuffer page on 2026-11-08; these pages were not read end to end. Confirmed the three bullets above. Removed: Comlink (no page read for it) and the generic spec, component-model and WASI sources.
Method: docs-only read of cited pages, 2026-11-08

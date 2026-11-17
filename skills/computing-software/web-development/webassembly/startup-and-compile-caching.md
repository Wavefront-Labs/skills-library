---
id: computing-software.web-development.webassembly.startup-and-compile-caching
name: startup-and-compile-caching
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, liftoff, code-caching, lazy-compilation, wasm-startup, tiered-compilation, wasm-size-budget, wasm]
level: practitioner
status: docs-checked
description: "Fast load"
sources: ["https://v8.dev/blog/liftoff", "https://v8.dev/blog/wasm-code-caching", "https://developer.mozilla.org/en-US/docs/WebAssembly/Reference/JavaScript_interface/instantiateStreaming_static"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Startup and compile caching

Goal: reduce time to interactive.
- Use streaming compile; engines tier from baseline to optimising compilers.
- Cache compiled modules (V8 code cache via HTTP caching) and split big modules.
- Lazy-load features with dynamic import.
Verify: time-to-first-call measured on cold and warm loads.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: baseline-to-optimising tiering (Liftoff/TurboFan), Chrome caching compiled code with the `.wasm` resource, streaming compilation.
Removed or reworded as unconfirmed: nothing.
Method: documentation only; no commands were run.

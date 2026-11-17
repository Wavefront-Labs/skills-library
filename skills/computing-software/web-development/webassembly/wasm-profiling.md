---
id: computing-software.web-development.webassembly.wasm-profiling
name: wasm-profiling
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasm-profiler, chrome-performance-wasm, name-section-profiling, wasm]
level: practitioner
status: docs-checked
description: "Finding hot spots"
sources: ["https://v8.dev/blog/liftoff", "https://docs.wasmtime.dev/examples-profiling-perf.html", "https://developer.chrome.com/docs/devtools/performance/reference", "https://developer.mozilla.org/en-US/docs/Web/API/Performance/now"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Profiling Wasm

Goal: profile performance.
- Keep the name section in profiling builds; use the Performance panel and `performance.now()` marks.
- Compare tiers: baseline vs optimising compilers (Liftoff is V8's baseline compiler, TurboFan the optimising one).
- Native-side: `perf` with runtimes supporting jitdump.
Verify: hot function identified with names.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: Liftoff and TurboFan tiers, `perf` with jitdump in Wasmtime, DevTools Performance panel, `performance.now()`.
Removed or reworded as unconfirmed: the 'confirm' hedge.
Method: documentation only; no commands were run.

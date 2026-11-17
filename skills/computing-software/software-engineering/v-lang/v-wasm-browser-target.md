---
id: computing-software.software-engineering.v-lang.v-wasm-browser-target
name: v-wasm-browser-target
category: computing-software
field: software-engineering
product: v-lang
tags: [v-wasm-browser-target, webassembly-backend, wasm, webassembly, -b wasm, emscripten, browser, wasm32, export, v-lang]
level: advanced
status: draft
description: "Use the wasm backend or emscripten path to produce .wasm for web pages, with exported functions and JS glue."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Compiling to WASM for the browser

Goal: run V in the browser.

- Native wasm backend (experimental): `v -b wasm -os browser -o app.wasm app.v`; supports a restricted subset (no GC, limited stdlib; confirm status in current docs).
- Export functions: `@[export: 'add'] pub fn add(a int, b int) int { return a + b }`; load with `WebAssembly.instantiateStreaming(fetch('app.wasm'), {})` and call `instance.exports.add(1, 2)`.
- Alternative: C backend with emscripten: `v -os wasm32_emscripten -o app.js app.v` (needs emsdk; confirm flag).
- Imports: declare host functions with `fn JS.console.log(...)`-style or `@[wasm_import]` (confirm).
- Keep memory simple: avoid arrays/strings heavy code until your version documents support.

Gotchas:
- The wasm backend is evolving quickly; examples in the V repo (`examples/wasm`) are the best source of truth.
- No threads or filesystem in the browser.

Verify: serve the page and call the exported add from the console.

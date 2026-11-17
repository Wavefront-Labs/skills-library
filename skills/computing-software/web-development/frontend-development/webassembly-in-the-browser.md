---
id: computing-software.web-development.frontend-development.webassembly-in-the-browser
name: webassembly-in-the-browser
category: computing-software
field: web-development
product: frontend-development
tags: [webassembly, wasm-instantiate, wasm-bindgen, wasm-pack, emscripten, wasm-unsafe-eval]
level: advanced
status: docs-checked
description: "Loading and using WebAssembly in web apps: instantiateStreaming and MIME types, wasm-pack/wasm-bindgen and Emscripten builds, bundler setup, workers, threads and CSP."
sources:
  - https://developer.mozilla.org/en-US/docs/WebAssembly/Guides/Using_the_JavaScript_API
  - https://developer.mozilla.org/en-US/docs/WebAssembly/Guides/Rust_to_Wasm
  - https://developer.mozilla.org/en-US/docs/WebAssembly/Guides/C_to_Wasm
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/script-src
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebAssembly in the browser

## 1. Raw loading
```js
const { instance } = await WebAssembly.instantiateStreaming(fetch("/img.wasm"), {
  env: { log: n => console.log(n) },
});
instance.exports.process(ptr, len);
```
`instantiateStreaming` rejects with a `TypeError` if the response MIME type is not `application/wasm`; fall back to `arrayBuffer()` + `WebAssembly.instantiate` if you cannot fix the server. Serve compressed with long-lived immutable caching.

## 2. Toolchains
- **Rust**: `wasm-pack build --target web` produces an ES module + `.wasm` with wasm-bindgen glue:
```js
import init, { resize } from "./pkg/imgtool.js";
await init();                       // fetches imgtool_bg.wasm
const out = resize(bytes, 800);     // Uint8Array in/out, glue copies across memory
```
- **C/C++**: Emscripten (`emcc hello.c -O3 -o hello.js`); see MDN's C to Wasm guide for output options.

## 3. Bundlers
Check your bundler's own docs for wasm support, and ensure the `.wasm` asset is emitted with a hashed name.

## 4. Performance rules
- Run heavy wasm in a Web Worker; a long wasm call blocks the main thread like JS.
- Crossing the JS/wasm boundary copies data; pass large buffers once, operate in linear memory, avoid chatty per-item calls.
- Threads (`-pthread`, Rust `wasm-bindgen-rayon`) need `SharedArrayBuffer`, i.e. cross-origin isolation (COOP `same-origin` + COEP `require-corp`/`credentialless`).

## 5. CSP
Compiling wasm needs `script-src 'wasm-unsafe-eval'` (not full `'unsafe-eval'`).

## Gotchas
- Big binaries hurt startup: optimise size, strip debug info, lazy-load the module only when the feature is used.
- Memory growth invalidates old `ArrayBuffer` views of `memory.buffer`; re-create views after calls that may grow.

## Checked

2026-11-01. Confirmed in MDN source: `instantiateStreaming` and the `application/wasm` MIME-type TypeError, `wasm-pack build --target web`, `emcc ... -O3 -o hello.js`, `'wasm-unsafe-eval'` in `script-src`, COEP `require-corp`/`credentialless` plus COOP `same-origin` for cross-origin isolation. Removed: emcc modularize flags, AssemblyScript/TinyGo, bundler plugin names, SIMD flags, wasm-opt flags.

Method: documentation only; no commands were run.

## Verify
- [ ] Network: `.wasm` served as `application/wasm`, compressed, cached.
- [ ] Performance panel shows the work in a worker thread, main thread free.

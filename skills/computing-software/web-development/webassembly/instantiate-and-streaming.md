---
id: computing-software.web-development.webassembly.instantiate-and-streaming
name: instantiate-and-streaming
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, instantiatestreaming, webassembly-compile, wasm-fetch, webassembly-instantiate, webassembly-module, wasm-js-api, wasm]
level: practitioner
status: docs-checked
description: "Loading"
sources: ["https://developer.mozilla.org/en-US/docs/WebAssembly/Reference/JavaScript_interface/instantiateStreaming_static", "https://developer.mozilla.org/en-US/docs/WebAssembly/Reference/JavaScript_interface/compileStreaming_static"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loading and instantiating modules

Goal: load Wasm efficiently in the browser.
- `const {instance} = await WebAssembly.instantiateStreaming(fetch('m.wasm'), imports)`; the response must be served as `application/wasm`, otherwise the promise rejects with a `TypeError`.
- `WebAssembly.compileStreaming` compiles a `WebAssembly.Module` from a streamed source when you need the module before instantiating it.
- A `WebAssembly.Module` can be instantiated again or shared via `postMessage()`.
Verify: streaming path used (no fallback to ArrayBuffer).

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: `instantiateStreaming(fetch(...), imports)` returning `{module, instance}`; MIME type TypeError; compileStreaming; module sharing via postMessage.
Removed or reworded as unconfirmed: IndexedDB caching.
Method: documentation only; no commands were run.

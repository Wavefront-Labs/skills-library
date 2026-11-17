---
id: computing-software.web-development.webassembly.js-wasm-boundary-types
name: js-wasm-boundary-types
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasm-js-bigint, wasm-string-passing, typed-array-views, wasm]
level: practitioner
status: docs-checked
description: "Data marshalling"
sources: ["https://developer.mozilla.org/en-US/docs/WebAssembly/Guides/Exported_functions", "https://developer.mozilla.org/en-US/docs/WebAssembly/Reference/JavaScript_interface/Memory"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Passing data across the JS boundary

Goal: move data correctly.
- JS numbers are converted to the Wasm parameter type (for example Int32); strings and arrays go through linear memory as bytes you encode and copy.
- Each crossing costs; batch work inside Wasm.
- Use `WebAssembly.Memory` shared views for bulk data.
Verify: a string round-trips with correct UTF-8.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: exported functions convert arguments to Wasm types; `WebAssembly.Memory` buffers expose memory.
Removed or reworded as unconfirmed: i64-to-BigInt and TextEncoder wording (JS API spec page was empty).
Method: documentation only; no commands were run.

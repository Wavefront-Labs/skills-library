---
id: computing-software.web-development.webassembly.fetch-and-streams-from-wasm
name: fetch-and-streams-from-wasm
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasm-fetch-bridge, asyncify, jspi-fetch, wasm]
level: practitioner
status: docs-checked
description: "Call async JavaScript such as fetch from synchronous-style Wasm using JSPI: WebAssembly.Suspending imports and WebAssembly.promising exports."
sources:
  - https://developer.mozilla.org/en-US/docs/WebAssembly/Reference/JavaScript_interface/Suspending
  - https://developer.mozilla.org/en-US/docs/WebAssembly/Reference/JavaScript_interface/promising_static
  - https://github.com/WebAssembly/proposals/blob/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network access from Wasm

Goal: do async I/O from sync-style code.
- JavaScript Promise Integration (JSPI): wrap a Promise-based JS function in `new WebAssembly.Suspending(fn)` when building the import object. When Wasm calls it, execution is suspended until the Promise resolves, then resumes with the resolved value on the stack. No change is needed inside the Wasm module.
- Wrap the exported Wasm function that relies on a suspending import in `WebAssembly.promising(fn)`; the wrapper takes the same arguments and returns a Promise of the result.
- Status: the proposals list shows JS Promise Integration at phase 5 (not yet merged to the spec) at the time of reading; check the MDN compatibility tables and your target engines before relying on it.
- Otherwise design the boundary explicitly async (callbacks or a promise-returning export).
Verify: an awaited fetch returns to Wasm code correctly.

## Checked
Read the intro and Description of the MDN WebAssembly.Suspending page, the intro, syntax and return value of WebAssembly.promising(), and the proposals README (WebAssembly/proposals) on 2026-11-08; the compatibility tables are rendered from data and were not read. Confirmed the Suspending and promising behaviour and the phase 5 listing. Removed: Asyncify and `-sASYNCIFY` claims about size and speed (no page read for them) and the generic spec, component-model and WASI sources.
Method: docs-only read of cited pages, 2026-11-08

---
id: computing-software.web-development.webassembly.linear-memory-management
name: linear-memory-management
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, memory-grow, wasm-memory-pages, memory-buffer-detach, wasm-linear-memory, wasm-memory64, wasm]
level: practitioner
status: docs-checked
description: "Memory model"
sources: ["https://developer.mozilla.org/en-US/docs/WebAssembly/Reference/JavaScript_interface/Memory/grow", "https://developer.mozilla.org/en-US/docs/WebAssembly/Reference/JavaScript_interface/Memory", "https://webassembly.github.io/spec/core/exec/instructions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linear memory and growth

Goal: manage memory safely.
- Memory is a byte array in 64 KiB pages; the `memory.grow` instruction returns the old size or -1 (JS `Memory.grow()` returns the previous page count); every grow call, even `grow(0)`, detaches views (`Uint8Array`) over the old `memory.buffer`.
- Re-create typed array views after any call that might grow memory.
- Memories can have an `i64` address type; `Memory.grow()` then takes a BigInt.
Verify: views remain valid after growth when re-created.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: 64 KiB pages; grow return value; detachment on every grow; i64 address type.
Removed or reworded as unconfirmed: the Memory64 support hedge.
Method: documentation only; no commands were run.

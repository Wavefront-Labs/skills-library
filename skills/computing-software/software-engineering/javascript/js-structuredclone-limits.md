---
id: computing-software.software-engineering.javascript.js-structuredclone-limits
name: js-structuredclone-limits
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, structuredclone-transfer, js-copying]
level: advanced
status: docs-checked
description: "Use structuredClone for deep copies with circular references, DataCloneError for unserialisable input, and the transfer option to detach buffers."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/Window/structuredClone"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# structuredClone limits and transfer

- `structuredClone(value)` and `structuredClone(value, options)` return a deep copy of the value using the structured clone algorithm. Circular references are supported and preserved (MDN: `clone.itself === clone`).
- It throws a `DataCloneError` DOMException if any part of the input is not serialisable.
- Transfer instead of copy: `structuredClone(obj, { transfer: [buf] })`. Only transferable objects can be transferred. Transferred objects are detached from the original and no longer accessible there; MDN's example shows the original `uInt8Array.byteLength` becoming `0`, and `new Int32Array(object1.buffer)` on the original buffer throwing a `TypeError`.
- You can clone any number of objects and transfer any subset of them, for example transferring `arrayBuffer1` but not `arrayBuffer2` from a nested value.
- Use case from MDN: validate a buffer asynchronously before saving, transferring so attempts to modify the original fail.
- MDN marks `structuredClone()` Baseline widely available (since March 2022). A core-js polyfill exists.

Self-check: clone `{ f() {} }` and confirm the `DataCloneError`.

## Checked

Confirmed against MDN "Window: structuredClone() method" (page last modified 2026-10-26), read 2026-11-08. Removed: the lists of cloned types, dropped getters/symbols/prototypes (those live on the separate Structured clone algorithm page, not read), the claim that postMessage/IndexedDB/history share the algorithm, and the Node v17 claim.
Method: docs-only read of cited pages, 2026-11-08

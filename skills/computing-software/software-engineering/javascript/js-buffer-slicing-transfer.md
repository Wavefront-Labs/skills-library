---
id: computing-software.software-engineering.javascript.js-buffer-slicing-transfer
name: js-buffer-slicing-transfer
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, arraybuffer-transfer, js-typed-arrays]
level: advanced
status: docs-checked
description: "ArrayBuffer slice copies, resizable buffers with maxByteLength and resize, and transfer or postMessage detaching the source buffer."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/ArrayBuffer"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ArrayBuffer views resize and transfer

- An `ArrayBuffer` is raw bytes; you read and write through a typed array or `DataView` over it (`new Int32Array(new ArrayBuffer(8))`).
- `buf.slice(begin, end)` returns a new `ArrayBuffer` holding a copy of the bytes (begin inclusive, end exclusive; negative indexes count from the end).
- Resizable: `new ArrayBuffer(8, { maxByteLength: 64 })`, then `buf.resize(n)`; new bytes are initialised to 0. Inspect with `resizable` and `maxByteLength`. This avoids copying into a new buffer to change size.
- `buf.transfer()` creates a new buffer with the same bytes and detaches the old one; `transferToFixedLength()` does the same but returns a non-resizable buffer.
- `ArrayBuffer` is a transferable object: pass it in the transfer list of `Worker.postMessage()` or `ServiceWorker.postMessage()` to move it between contexts; the original becomes detached.
- A detached buffer has `byteLength` 0 (also through typed array views), `detached` is `true`, and methods such as `resize()` and `slice()` (and the views' methods) throw `TypeError`.

Self-check: after `const b2 = b1.transfer()`, `b1.detached` is `true` and `b1.byteLength` is 0.

## Checked

Confirmed on the MDN ArrayBuffer page: slice copy semantics, resizable buffers, transfer and transferToFixedLength, transferable objects and detached behaviour. Removed: the `subarray` versus typed-array `slice` comparison, offset alignment `RangeError`, `TextDecoder` and base64 conversion notes, the "ES2024" label and the claim that detached views "read as empty" (the page says methods throw `TypeError`), none of which the page supports.

Method: docs-only read of cited pages, 2026-11-08

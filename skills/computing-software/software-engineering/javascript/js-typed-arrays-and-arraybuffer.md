---
id: computing-software.software-engineering.javascript.js-typed-arrays-and-arraybuffer
name: js-typed-arrays-and-arraybuffer
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-typed-arrays, arraybuffer, dataview, endianness, binary-data]
level: advanced
status: docs-checked
description: "Handle binary data with ArrayBuffer, typed arrays and DataView, including endianness and views."
sources: ["https://tc39.es/ecma262/", "https://developer.mozilla.org/en-US/docs/Web/JavaScript", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/ArrayBuffer", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/DataView"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typed arrays, ArrayBuffer, DataView

- An `ArrayBuffer` holds raw bytes; typed arrays (`Uint8Array`, `Int16Array`, `Float32Array`...) and `DataView` read and write it.
- `DataView` accessors give explicit control of byte order (endianness) regardless of the platform; use it for file and network formats. Multi-byte typed arrays use the platform byte order.
- Creating a typed array on a buffer throws a RangeError if `byteOffset` (or the buffer length when no length is given) is not an integral multiple of the element size.
- Integer typed arrays convert out-of-range numbers by truncating the decimal part and taking the lowest bits (they wrap); `Uint8ClampedArray` clamps to 0-255 instead.
- `ArrayBuffer` objects can be made resizable with the `maxByteLength` constructor option, and are transferable objects.

## Checked

2026-11-02. Confirmed: MDN TypedArray (conversion rules, clamping, endianness), TypedArray constructor (RangeError on offset/length multiples), ArrayBuffer (maxByteLength, transferable), DataView (endianness).
Removed: Out-of-range writes ignored, little-endian-on-all-hardware, subarray/slice semantics, TextEncoder/TextDecoder, transfer() and Uint8Array toBase64 availability notes.
Method: documentation only; no commands were run.

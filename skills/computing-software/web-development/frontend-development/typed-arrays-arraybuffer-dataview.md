---
id: computing-software.web-development.frontend-development.typed-arrays-arraybuffer-dataview
name: typed-arrays-arraybuffer-dataview
category: computing-software
field: web-development
product: frontend-development
tags: [iterators-generators, typed-arrays, arraybuffer, dataview, binary-data, javascript]
level: practitioner
status: verified
description: "Handling binary data with ArrayBuffer, typed arrays and DataView: endianness, views vs copies, TextEncoder, Blob conversion, and transferring buffers to workers."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Typed_arrays
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/DataView
  - https://developer.mozilla.org/en-US/docs/Web/API/TextEncoder
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typed arrays, ArrayBuffer and DataView

## 1. Model
- `ArrayBuffer` = raw bytes, no accessors.
- Typed array (`Uint8Array`, `Int16Array`, `Float32Array`, `BigInt64Array`...) = fixed-type view using **platform endianness** (little-endian on all mainstream hardware).
- `DataView` = mixed-type view with explicit endianness - use it for file formats and network protocols.

## 2. Parse a binary header
```js
const buf = await (await fetch("/file.wav")).arrayBuffer();
const v = new DataView(buf);
const tag = new TextDecoder().decode(new Uint8Array(buf, 0, 4)); // "RIFF"
const channels = v.getUint16(22, true);   // true = little-endian
const sampleRate = v.getUint32(24, true);
```
Big-endian network formats: omit the flag (default is big-endian).

## 3. Views vs copies
- `new Uint8Array(buf, offset, length)` and `subarray()` share memory.
- `slice()` copies. `new Uint8Array(otherTypedArray)` copies and converts.
- Multi-byte views need aligned offsets (`new Uint32Array(buf, 3)` throws `RangeError`); use DataView for unaligned reads.
- Writing out-of-range values wraps (`Uint8Array` 256 -> 0; `Uint8ClampedArray` gave 255) unless you use `Uint8ClampedArray` (clamps, used by canvas ImageData).

## 4. Conversions
```js
new TextEncoder().encode("héllo");            // Uint8Array UTF-8
new TextDecoder("utf-8", { fatal: true }).decode(bytes);
const blob = new Blob([bytes], { type: "application/octet-stream" });
const bytes2 = new Uint8Array(await blob.arrayBuffer());
// base64 (Chrome 140, Firefox 133, Safari 18.2 per MDN compat; absent in Node 20): bytes.toBase64(), Uint8Array.fromBase64(s); older: btoa(String.fromCharCode(...bytes)) for small inputs only
```

## 5. Workers and transfers
`worker.postMessage(buf, [buf])` transfers ownership - zero copy, the sender's buffer becomes detached (byteLength 0). `SharedArrayBuffer` needs cross-origin isolation (COOP/COEP).

## 6. Pitfalls
- `String.fromCharCode(...bigArray)` overflows the call stack (`RangeError` at 150 000 elements in Node 20, so well below MB sizes) - chunk it or use TextDecoder.
- Node `Buffer` is a `Uint8Array` subclass but `buffer.buffer` may be a larger shared pool - use `buf.byteOffset`/`byteLength` when creating views.

## Verify
Round-trip tests: encode -> decode equals input; parse a known fixture file and assert fields.

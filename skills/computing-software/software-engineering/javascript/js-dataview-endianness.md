---
id: computing-software.software-engineering.javascript.js-dataview-endianness
name: js-dataview-endianness
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, dataview-endianness, js-typed-arrays]
level: advanced
status: docs-checked
description: "Read and write binary structures with DataView and explicit byte order."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/DataView", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/DataView/DataView", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/DataView/getUint32"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DataView and endianness

- `const dv = new DataView(buf, byteOffset, byteLength); dv.getUint32(0, true)`: the optional last argument `littleEndian`, when true, reads little-endian; false or omitted reads big-endian. The same applies to the setters.
- Typed arrays such as `Int16Array` use the platform's endianness (most platforms are little-endian). Use DataView for network or file formats with a fixed byte order. WebAssembly memory is always little-endian, which is another reason to use DataView there.
- 64-bit integers: `getBigInt64` / `getBigUint64` and the matching setters use BigInt.
- `DataView` must be called with `new`. A `RangeError` is thrown if `byteOffset` and `byteLength` extend past the buffer, and by the getters when the read would pass the end of the view.
- There is no alignment constraint: multi-byte values can be read from any offset in bounds. Parse a protocol header from an explicit table of offsets.
- Detect platform order by writing with DataView and reading with a typed array:
  `new DataView(buf).setInt16(0, 256, true)` on a 2-byte `ArrayBuffer`, then `new Int16Array(buf)[0] === 256` means the platform is little-endian.

Self-check: write `0x01020304` with `setUint32(0, 0x01020304)` (big-endian default) and read bytes `[1,2,3,4]` through a `Uint8Array`.

## Checked

Confirmed on the cited MDN pages (DataView, DataView() constructor, getUint32): default big-endian, the littleEndian parameter, typed arrays using platform endianness, WebAssembly note, BigInt accessors, RangeError conditions, no alignment constraint, the platform-detection pattern. Removed: the Uint16Array-based detection one-liner (replaced by the page's pattern) and the "struct padding" wording.

Method: docs-only read of cited pages, 2026-11-08

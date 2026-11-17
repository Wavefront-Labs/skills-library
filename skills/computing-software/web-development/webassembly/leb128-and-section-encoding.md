---
id: computing-software.web-development.webassembly.leb128-and-section-encoding
name: leb128-and-section-encoding
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, leb128-encoding, wasm-magic-number, section-size, wasm-binary-format, leb128, wasm-section-ids, wasm]
level: practitioner
status: docs-checked
description: "Reading raw bytes"
sources: ["https://webassembly.github.io/spec/core/binary/modules.html", "https://webassembly.github.io/spec/core/binary/values.html", "https://github.com/WebAssembly/wabt"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LEB128 and section encoding

Goal: read a .wasm file by hand.
- Header `00 61 73 6d 01 00 00 00` (magic then version 1); then sections: id byte, `u32` size, contents.
- LEB128 variable-length integers (unsigned and signed) encode indices and sizes.
- `xxd` plus `wasm-objdump` (WABT prints information about a wasm binary) helps check offsets.
Verify: manual decode of a tiny module matches `wasm-objdump` output.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: magic and version bytes; sections with an id and size; unsigned and signed LEB128 with a byte-count limit of ceil(N/7); `wasm-objdump` prints binary information.
Removed or reworded as unconfirmed: the `-s` flag of `wasm-objdump`.
Method: documentation only; no commands were run.

---
id: computing-software.web-development.webassembly.strings-and-lists-across-boundary
name: strings-and-lists-across-boundary
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, utf8-utf16-latin1, lift-lower, realloc-export, canonical-abi, string-encoding, wasm-lifting-lowering, wasm]
level: practitioner
status: docs-checked
description: "Data layout"
sources: ["https://raw.githubusercontent.com/WebAssembly/component-model/main/design/mvp/Explainer.md", "https://raw.githubusercontent.com/WebAssembly/component-model/main/design/mvp/CanonicalABI.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Strings, lists and records across components

Goal: understand data passing.
- The Canonical ABI options on `canon lift` and `canon lower` include `string-encoding=utf8`, `string-encoding=utf16` or `string-encoding=latin1+utf16`, `(memory ...)`, `(realloc ...)` and `(post-return ...)`.
- If no `string-encoding` is given the default is `utf8`; more than one is a validation error. `latin1+utf16` picks Latin-1 or UTF-16 dynamically per string.
- `(memory ...)` is required whenever the ABI must load or store; `(realloc ...)` is a core function taking original pointer, original size, alignment and new size and returning a pointer. The ABI calls it to allocate (passing 0 for the first two arguments) and to reallocate.
- `(post-return ...)` lets the callee free memory after the caller has read the results.
- Bindings generators hide this; know it when debugging corruption.
Verify: round trip of non-ASCII strings is correct.

## Checked

2026-11-08. Confirmed in the Component Model Explainer, canonical ABI options section (read lines 1400-1460). The CanonicalABI.md was only searched for `realloc` (not read in full), and no claim here depends on it beyond the use of `realloc`.
Removed as unconfirmed: the export name `cabi_realloc` (a toolchain convention not stated in these pages) and the copying-cost remark.
Method: documentation only; no commands were run.

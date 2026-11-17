---
id: computing-software.web-development.webassembly.imports-exports-start
name: imports-exports-start
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasm-import, wasm-export, start-section, wasm]
level: practitioner
status: docs-checked
description: "Linking"
sources: ["https://webassembly.github.io/spec/core/syntax/modules.html", "https://developer.mozilla.org/en-US/docs/WebAssembly/Reference/JavaScript_interface/LinkError", "https://developer.mozilla.org/en-US/docs/WebAssembly/Reference/JavaScript_interface/instantiateStreaming_static"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Imports, exports and start function

Goal: wire a module to its host.
- Imports are satisfied at instantiation; exports expose functions, tables, memories and globals.
- The start function runs automatically at instantiation, after tables and memories are initialised; it is meant for initialising module state, so keep it light.
- In the JS API a missing import makes instantiation reject with `WebAssembly.LinkError`.
Verify: instantiation succeeds with the supplied import object.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: start function timing and purpose; LinkError on instantiation errors and missing import properties.
Removed or reworded as unconfirmed: the (module, name, type) triple wording.
Method: documentation only; no commands were run.

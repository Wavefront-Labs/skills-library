---
id: computing-software.web-development.webassembly.exceptions-tailcalls-stack-switching
name: exceptions-tailcalls-stack-switching
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasm-exceptions, return-call, jspi, wasm]
level: practitioner
status: docs-checked
description: "Control proposals"
sources: ["https://raw.githubusercontent.com/WebAssembly/exception-handling/main/proposals/exception-handling/Exceptions.md", "https://raw.githubusercontent.com/WebAssembly/tail-call/main/proposals/tail-call/Overview.md", "https://raw.githubusercontent.com/WebAssembly/js-promise-integration/main/proposals/js-promise-integration/Overview.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exception handling, tail calls, JSPI

Goal: use modern control features.
- Exceptions: tags are declared in a `tag` section; `throw` takes a tag index; a `try_table` block holds catch clauses (`catch`, `catch_ref`, `catch_all`, `catch_all_ref`); a caught exception can be reified as an `exnref` and rethrown. The earlier (legacy) proposal is still supported in several browsers, so toolchains may emit either form.
- Tail calls: `return_call <funcidx>` (opcode 0x12) and `return_call_indirect <tableidx> <typeidx>` (0x13) unwind the current frame before the call. Tail behaviour is guaranteed across Wasm module boundaries but not for calls to host functions.
- JSPI (JavaScript Promise Integration): `WebAssembly.Suspending` marks a Promise-returning import so Wasm suspends until it resolves; `WebAssembly.promising` wraps an export so it returns a Promise. A suspending import reached through an unmarked export traps. Only Wasm frames may sit between the promising call and the suspending import.
- Detect features before relying on them; this document does not state per-engine support.
Verify: feature-detection logic selects the correct build.

## Checked

2026-11-08. Confirmed in the exception-handling Exceptions.md (read lines 1-150: overview, tags, try_table, catch forms, throw, exnref), the tail-call Overview (read in full) and the JSPI Overview (read lines 1-140: summary, core concepts, restriction, examples).
Removed as unconfirmed: the `try`/`catch` instruction names (current text uses `try_table`) and the JSPI "confirm status" note.
Method: documentation only; no commands were run.

---
id: computing-software.web-development.webassembly.traps-and-determinism
name: traps-and-determinism
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasm-trap, unreachable-trap, nondeterminism-sources, wasm]
level: practitioner
status: docs-checked
description: "Runtime errors"
sources: ["https://webassembly.github.io/spec/core/exec/instructions.html", "https://webassembly.github.io/spec/core/exec/numerics.html", "https://webassembly.github.io/spec/core/exec/runtime.html", "https://developer.mozilla.org/en-US/docs/WebAssembly/Reference/JavaScript_interface/RuntimeError"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Traps and determinism

Goal: handle traps.
- Traps: `unreachable`, out-of-bounds memory/table access, integer divide by zero or signed overflow, NaN or out-of-range float-to-integer truncation, indirect call type mismatch.
- In the JS API a trap is thrown as `WebAssembly.RuntimeError`.
- Nondeterminism sources in the spec: NaN bit patterns, `memory.grow` failure, host calls.
Verify: each trap type reproduced in a test.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: trap conditions; RuntimeError on traps; non-deterministic NaN results, `memory.grow` and `table.grow` failure, host function calls.
Removed or reworded as unconfirmed: stack exhaustion, partial state changes and threads (not on a page read).
Method: documentation only; no commands were run.

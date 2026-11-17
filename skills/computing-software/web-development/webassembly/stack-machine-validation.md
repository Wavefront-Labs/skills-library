---
id: computing-software.web-development.webassembly.stack-machine-validation
name: stack-machine-validation
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasm-validation-algorithm, operand-stack, type-checking, wasm-validation, wasm-traps, wasm-stack-machine, wasm]
level: practitioner
status: docs-checked
description: "Why modules are safe"
sources: ["https://webassembly.github.io/spec/core/valid/instructions.html", "https://developer.mozilla.org/en-US/docs/WebAssembly/Guides/Concepts", "https://developer.mozilla.org/en-US/docs/WebAssembly/Reference/JavaScript_interface/validate_static", "https://github.com/WebAssembly/wabt", "https://webassembly.github.io/spec/core/exec/instructions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stack machine and validation

Goal: understand safety guarantees.
- Validation type-checks the operand stack at every instruction; unreachable code is polymorphic.
- WebAssembly is specified to run in a safe, sandboxed environment; indirect calls are type-checked at runtime.
- Validate with `wasm-validate` or `WebAssembly.validate(bytes)`.
Verify: an ill-typed module is rejected by validation.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: polymorphic stack after unconditional branches; sandboxed execution; `call_indirect` casts to the expected type; `wasm-validate` and `WebAssembly.validate`.
Removed or reworded as unconfirmed: 'no raw stack access' and 'no access outside linear memory' wording.
Method: documentation only; no commands were run.

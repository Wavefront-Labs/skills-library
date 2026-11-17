---
id: computing-software.web-development.webassembly.fuzzing-wasm-modules
name: fuzzing-wasm-modules
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasm-smith-fuzz, cargo-fuzz-wasm, differential-testing, wasm-smith, wasm-fuzzing, wasm-validation-fuzz, wasm]
level: practitioner
status: docs-checked
description: "Quality"
sources: ["https://raw.githubusercontent.com/bytecodealliance/wasm-tools/main/crates/wasm-smith/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fuzzing runtimes and modules

Goal: find bugs in hosts and modules.
- `wasm-smith` is a WebAssembly test case generator: every generated module passes validation, it covers the full language, it is deterministic for a given input seed, and it implements `Arbitrary` for use with `cargo fuzz` and `libfuzzer-sys`.
- Fuzz target shape: take a `wasm_smith::Module`, call `to_bytes()`, feed the bytes to your tool. Setup: `cargo fuzz add <target>`, `cargo add wasm-smith`, `cargo fuzz run <target>`.
- Command line: `cargo install wasm-tools`, then `wasm-tools smith -o test.wasm` with random bytes on stdin turns arbitrary input into a valid module.
- The repository's `validate` fuzz target checks that every generated module validates with `wasmparser`.
- Also fuzz host functions that take pointers and lengths (your own judgement, not a documented procedure).
Verify: the fuzz corpus runs clean for a set time.

## Checked

2026-11-08. Confirmed in the wasm-smith README (read in full).
Removed as unconfirmed: cross-engine differential testing and sanitizer advice as documented practice.
Method: documentation only; no commands were run.

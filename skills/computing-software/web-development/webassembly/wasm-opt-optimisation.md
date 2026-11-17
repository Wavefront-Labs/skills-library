---
id: computing-software.web-development.webassembly.wasm-opt-optimisation
name: wasm-opt-optimisation
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasm-opt-o3, binaryen-passes, wasm-strip, binaryen, wasm-opt, wabt, wasm]
level: practitioner
status: docs-checked
description: "Optimising binaries"
sources: ["https://raw.githubusercontent.com/WebAssembly/binaryen/main/README.md", "https://raw.githubusercontent.com/rustwasm/book/master/src/reference/code-size.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# wasm-opt

Goal: optimise compiled Wasm.
- `wasm-opt -O3 -o output.wasm input.wasm`; `-Os` or `-Oz` for size.
- By default `wasm-opt` removes the `names` section unless `-g` is also specified.
- Run it on the `.wasm` produced by the compiler (it post-processes LLVM output).
- Always retest after optimisation.
Verify: size and speed measured before and after.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: `-O3`, `-Os`, `-Oz`, the names-section default and `-g`.
Removed or reworded as unconfirmed: `--strip-debug` and `--enable-simd`.
Method: documentation only; no commands were run.

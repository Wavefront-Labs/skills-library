---
id: computing-software.web-development.webassembly.wasm-build-reproducibility
name: wasm-build-reproducibility
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, reproducible-wasm, size-budget-ci, wasm-binary-diff, wasm]
level: practitioner
status: docs-checked
description: "Release pipelines"
sources: ["https://raw.githubusercontent.com/rustwasm/twiggy/master/README.md", "https://raw.githubusercontent.com/emscripten-core/emscripten/main/site/source/docs/porting/Debugging.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Build reproducibility and size budgets in CI

Goal: keep builds stable.
- Pin the toolchain versions your build uses and compare a checksum of the output across CI runs; two clean builds from the same inputs should give identical hashes (a practice recommendation, not a documented guarantee).
- Twiggy is a code size profiler for Wasm: it analyses the call graph to show why a function is in the binary and its retained size, meaning how much would be saved by removing it and what becomes dead code. Install with `cargo install twiggy`. Use its reports to set a size budget, and read the Twiggy guide for the exact subcommands.
- Emscripten can keep debug information out of the shipped binary with `-gseparate-dwarf`, and writes source maps with `-gsource-map`; publish those separately from the release binary.
Verify: two builds yield identical hashes.

## Checked

2026-11-08. Confirmed in the Twiggy README (read in full) and the Emscripten Debugging page (searched for the DWARF and source-map passages, not read end to end).
Removed as unconfirmed: the `twiggy diff` subcommand (its guide page was not reachable), `rust-toolchain.toml` and emsdk pinning specifics.
Method: documentation only; no commands were run.

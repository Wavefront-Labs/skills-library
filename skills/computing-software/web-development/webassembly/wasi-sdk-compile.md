---
id: computing-software.web-development.webassembly.wasi-sdk-compile
name: wasi-sdk-compile
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, clang-wasi, wasi-sysroot, wasm32-wasip1, wasi-sdk, wasm32-wasi, wasi-libc, wasm]
level: practitioner
status: docs-checked
description: "Standalone Wasm"
sources: ["https://raw.githubusercontent.com/WebAssembly/wasi-sdk/main/README.md", "https://docs.wasmtime.dev/cli-options.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compiling with wasi-sdk

Goal: build command-line Wasm programs.
- `$WASI_SDK/bin/clang --sysroot=$WASI_SDK/share/wasi-sysroot -O2 hello.c -o hello.wasm`; run it with a WASI runtime such as `wasmtime`.
- Targets: `wasm32-wasip1` (default), `wasm32-wasip2`, `wasm32-wasip3` and `wasm32-wasip1-threads` (preview 1 with experimental thread spawning via wasi-threads).
- Use `--dir` for file access.
Verify: output printed under wasmtime.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: `--sysroot=.../share/wasi-sysroot`, the wasip1/wasip2/wasip3/wasip1-threads targets, `--dir` in the Wasmtime CLI.
Removed or reworded as unconfirmed: the claim that preview1 has no threads (the `wasm32-wasip1-threads` target exists) and the sockets claim.
Method: documentation only; no commands were run.

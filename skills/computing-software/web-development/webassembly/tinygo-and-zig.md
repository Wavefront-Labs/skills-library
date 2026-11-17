---
id: computing-software.web-development.webassembly.tinygo-and-zig
name: tinygo-and-zig
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, tinygo-wasm, zig-wasm32, go-wasm-exec, wasm]
level: practitioner
status: docs-checked
description: "Go and Zig"
sources: ["https://tinygo.org/docs/guides/webassembly/wasm/", "https://tinygo.org/docs/guides/webassembly/wasi/", "https://go.dev/wiki/WebAssembly"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TinyGo and Zig

Goal: compile Go and Zig.
- TinyGo for the browser: `GOOS=js GOARCH=wasm tinygo build -o wasm.wasm ./main.go` with the TinyGo `wasm_exec.js` (use the same version as the compiler); for WASI: `GOOS=wasip1 GOARCH=wasm tinygo build -o main.wasm main.go` (wasip1 and wasip2 are supported).
- Standard Go: `GOOS=js GOARCH=wasm go build` with `wasm_exec.js`, and `GOOS=wasip1 GOARCH=wasm go build`.
- Goroutine/GC overhead differs; check sizes.
Verify: module loads in the browser or runtime.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: TinyGo and Go build commands with `GOOS`/`GOARCH`, `wasm_exec.js`, wasip1 and wasip2 support.
Removed or reworded as unconfirmed: the `-target wasm` and `-target wasi` TinyGo flags (the documented form uses `GOOS`/`GOARCH`) and the Zig command line (not covered by a page read).
Method: documentation only; no commands were run.

---
id: computing-software.web-development.webassembly.assemblyscript-basics
name: assemblyscript-basics
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, assemblyscript-asc, asc-compile, typed-typescript, assemblyscript, tinygo, zig-wasm, wasm]
level: practitioner
status: docs-checked
description: "TypeScript-like to Wasm"
sources: ["https://raw.githubusercontent.com/AssemblyScript/website/main/src/getting-started.md", "https://raw.githubusercontent.com/AssemblyScript/website/main/src/status.md", "https://raw.githubusercontent.com/AssemblyScript/assemblyscript/main/lib/loader/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AssemblyScript

Goal: write Wasm with TS-like syntax.
- `asc --config asconfig.json --target release` (the config defines `debug` and `release` targets; output goes to `build/`); types like `i32`, `f64`.
- Loader utilities from `@assemblyscript/loader`.
- Closures that capture local variables are not yet supported; see the status page.
Verify: exported function runs in Node.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: `asc --config asconfig.json --target release`, the `build/` output, `@assemblyscript/loader`, the closure limitation.
Removed or reworded as unconfirmed: the `npx asc ... -o` command line and the manual-memory line.
Method: documentation only; no commands were run.

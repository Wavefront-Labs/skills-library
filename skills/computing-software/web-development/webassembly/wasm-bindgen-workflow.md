---
id: computing-software.web-development.webassembly.wasm-bindgen-workflow
name: wasm-bindgen-workflow
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasm-pack-build, js-sys, web-sys, wasm-bindgen, wasm-pack, wasm32-unknown-unknown, wasm]
level: practitioner
status: docs-checked
description: "Rust bindings"
sources: ["https://raw.githubusercontent.com/rustwasm/wasm-bindgen/main/guide/src/examples/hello-world.md", "https://raw.githubusercontent.com/rustwasm/wasm-pack/master/docs/src/commands/build.md", "https://raw.githubusercontent.com/rustwasm/book/master/src/reference/code-size.md", "https://raw.githubusercontent.com/rustwasm/book/master/src/reference/debugging.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# wasm-bindgen and wasm-pack

Goal: ship Rust to the web.
- Annotate exported Rust items with `#[wasm_bindgen]`; build for the `wasm32-unknown-unknown` target with `wasm-pack build --target web`.
- `web-sys` and `js-sys` expose browser APIs; `console_error_panic_hook` aids debugging.
- Bundle size: `opt-level="s"`, `lto=true`, `wasm-opt`.
Verify: the generated package imports and runs in a page.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: `wasm-pack build --target web`, `web-sys`/`js-sys`, `console_error_panic_hook`, `opt-level`, `lto = true`, `wasm-opt`.
Removed or reworded as unconfirmed: the `rustup target add` line and the example signature.
Method: documentation only; no commands were run.

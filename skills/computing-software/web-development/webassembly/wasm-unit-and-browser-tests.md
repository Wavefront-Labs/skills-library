---
id: computing-software.web-development.webassembly.wasm-unit-and-browser-tests
name: wasm-unit-and-browser-tests
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasm-bindgen-test, headless-browser-tests, wasm-test-runner, wasm-testing, wasm-pack-test, wasm-ci, wasm]
level: practitioner
status: docs-checked
description: "Automated tests"
sources: ["https://raw.githubusercontent.com/rustwasm/wasm-bindgen/main/guide/src/wasm-bindgen-test/usage.md", "https://raw.githubusercontent.com/rustwasm/wasm-bindgen/main/guide/src/wasm-bindgen-test/browsers.md", "https://raw.githubusercontent.com/rustwasm/wasm-pack/master/docs/src/commands/test.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unit and browser tests

Goal: test Wasm modules.
- `wasm-pack test --headless --chrome` runs `#[wasm_bindgen_test]` tests (the default target is Node.js; `--node` selects it explicitly); run native tests for logic and Wasm tests for bindings.
- Node can run Wasm for JS-level tests.
- Pin browser versions in CI.
Verify: CI runs both native and Wasm targets.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: `wasm-pack test`, `--headless`, `--chrome`, `#[wasm_bindgen_test]`, Node default.
Removed or reworded as unconfirmed: nothing.
Method: documentation only; no commands were run.

---
id: computing-software.web-development.vite.webassembly
name: webassembly
category: computing-software
field: web-development
product: vite
tags: [wasm-import, wasm-init, wasm-esm-integration, wasm-url]
level: advanced
status: docs-checked
description: "Import WebAssembly in Vite: direct ES module import, ?init for manual instantiation with importObject, ?url for the Module, and the SSR Node-only limit."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/features.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Direct import follows the WebAssembly/ES Module Integration proposal. Exports become named ES exports and the module's own imports resolve from JavaScript modules. It behaves as an async module, so top-level `await` support is required.

```js
import { add } from './add.wasm'
```

For TypeScript, enable `allowArbitraryExtensions` and add a declaration `add.d.wasm.ts` next to the file.

Manual control with `?init` (default export is an init function returning a Promise of `WebAssembly.Instance`; it can take an importObject):

```js
import init from './example.wasm?init'
init({ imports: { someFunc: () => {} } }).then((instance) => instance.exports.test())
```

For the `Module` object (to instantiate repeatedly), import the URL and use `WebAssembly.instantiateStreaming(fetch(wasmUrl))` with `foo.wasm?url`.

Build: files smaller than `assetsInlineLimit` are inlined as base64, otherwise treated as static assets.

SSR builds: both forms use `node:fs`, so only Node.js-compatible runtimes work.

## Checked

2026-11-07. Re-read the Features guide (docs/guide/features.md) in full, WebAssembly section. Confirmed direct ESM integration (named exports, top-level await), the allowArbitraryExtensions and .d.wasm.ts note, ?init with an importObject, the ?url plus WebAssembly.instantiateStreaming route to the Module, the assetsInlineLimit inlining rule and the node:fs SSR limitation. Nothing removed.

Method: documentation only; no commands were run.

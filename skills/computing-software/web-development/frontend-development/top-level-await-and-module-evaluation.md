---
id: computing-software.web-development.frontend-development.top-level-await-and-module-evaluation
name: top-level-await-and-module-evaluation
category: computing-software
field: web-development
product: frontend-development
tags: [es-modules, javascript-modules, top-level-await, module-evaluation-order, async-module-init, tla]
level: practitioner
status: docs-checked
description: "Using top-level await in modules: how it delays dependents, evaluation order, good uses (config, wasm, conditional imports) and the waterfalls it causes."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/await
  - https://nodejs.org/api/errors.html#err_require_async_module
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Top-level await and module evaluation

**Goal:** use top-level await (TLA) where it simplifies async initialisation without stalling the whole app.

## 1. Semantics
In ES modules (not classic scripts or CommonJS), `await` at module top level pauses that module's evaluation. **Every module that imports it (directly or transitively) waits** before running. Sibling branches without the dependency continue.

## 2. Good uses
```js
// config.js
const res = await fetch('/config.json');
export const config = await res.json();

// wasm.js
export const { instance } = await WebAssembly.instantiateStreaming(fetch('/codec.wasm'));

// conditional dependency
export const crypto = globalThis.crypto ?? (await import('node:crypto')).webcrypto;
```

## 3. Hazards
- **Waterfalls**: a fetch in a deep leaf module blocks everything above it, delaying first render. Keep TLA in modules that genuinely gate the app, and start fetches as early as possible.
- **Hard to see failures**: a rejected TLA makes importing modules fail to evaluate; error appears as a module load error. Wrap with try/catch and export a fallback where possible.
- **Cycles + TLA**: avoid top-level await in modules that sit in an import cycle.
- Bundlers: check that your build target and output format support top-level await; this is a bundler setting, so confirm it in the bundler's documentation.
- Node: works in ES modules; `require()` of an ES module that contains top-level await throws `ERR_REQUIRE_ASYNC_MODULE`.

## 4. Alternative
Export a promise or an `init()` function when consumers should decide when to wait:
```js
export const ready = loadConfig();   // consumers: const cfg = await ready;
```

## Verify
- [ ] Performance panel: TLA fetches start at module load, not after unrelated work.
- [ ] Build target supports TLA (no build error, works in target browsers).
- [ ] Failure path (config 500) shows a handled error state.

## Checked

2026-10-26. MDN `await` (top level of a module; modules that import a module using await wait for it) and the Node errors page (ERR_REQUIRE_ASYNC_MODULE when require() reaches a module with top-level await). Removed the unconfirmed bundler error text and the deadlock claim.

Method: documentation only; no commands were run.

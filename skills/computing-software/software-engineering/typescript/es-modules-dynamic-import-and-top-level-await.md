---
id: computing-software.software-engineering.typescript.es-modules-dynamic-import-and-top-level-await
name: es-modules-dynamic-import-and-top-level-await
category: computing-software
field: software-engineering
product: typescript
tags: [javascript, es-modules, dynamic-import, top-level-await, live-bindings, import-attributes, circular-modules]
level: practitioner
status: gated
description: "Use ES modules correctly: static vs dynamic import, live bindings, module evaluation order and cycles, top-level await trade-offs, import.meta and JSON import attributes."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/import", "https://nodejs.org/api/esm.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ES modules, dynamic import and top-level await

**Goal:** module structure that loads fast, code-splits cleanly and avoids
initialisation-order bugs.

## Static imports
```js
import { parse } from "./parser.js";         // hoisted, resolved before any code runs
import * as fs from "node:fs/promises";
import config from "./config.json" with { type: "json" };   // import attributes (ran on Node 20.20.2 and 24.22.0; browser support not confirmed (gated: unconfirmed, source is paywalled or blocked))
export { parse as parseConfig };
export * from "./types.js";
```
- Module code runs once, in strict mode, and is cached per resolved URL.
- In Node ESM and browsers, relative specifiers need the file extension.
- Bindings are **live**: importers see later reassignments of an exported `let`; they cannot
  assign to it (tested: `inc()` made the importer's `n` read 2; `n = 5` threw `TypeError: Assignment to constant variable.`).
- A bare `./x` specifier fails in Node ESM with `ERR_MODULE_NOT_FOUND` (tested).

## Dynamic import
```js
const { renderChart } = await import("./chart.js");       // returns a promise of the namespace
button.onclick = async () => (await import("./editor.js")).open();   // load on demand
const mod = await import(`./locales/${lang}.js`);         // bundlers split per matching file
```
Use for code splitting, optional dependencies (`try { await import("sharp") } catch {}` (a missing module rejects with `ERR_MODULE_NOT_FOUND`, tested)), and
loading ESM from CommonJS (`await import()` works in CJS).

## Top-level await
```js
// db.js
export const pool = await createPool(process.env.DATABASE_URL);
```
Every importer waits until it resolves - one slow top-level await delays the whole module graph
(and app startup). Fine for entry points and scripts; avoid in widely imported library modules.
A module with TLA cannot be loaded with Node's `require(esm)` (tested on 20.20 and 24.22: `ERR_REQUIRE_ASYNC_MODULE`).

## Evaluation order and cycles
Modules evaluate depth-first in import order. In a cycle, one module sees the other's exports
before they are initialised: accessing a `const`/`class` export throws
`ReferenceError: Cannot access 'X' before initialization` (TDZ). Fixes: break the cycle (shared
module), or defer access into functions that run after load. `madge --circular src` finds cycles (madge 8.0.0 reported `a.js > b.js` on a two-file cycle). Tested the cycle itself: `ReferenceError: Cannot access 'a' before initialization`.

## import.meta
`import.meta.url` (file URL of the module), `import.meta.dirname` / `filename` (Node 20.11+),
`import.meta.resolve("pkg")`, `import.meta.env` (Vite) (gated: unconfirmed, source is paywalled or blocked). `dirname`, `filename` and `resolve` returned a string, a string and a `file:///` URL on Node 20.20 and 24.22.

## Side-effect imports and tree shaking
`import "./polyfills.js"` runs code for its effects. Bundlers can drop unused exports only when
modules are side-effect-free (`"sideEffects": false`); avoid top-level work in library modules.

## Verify
- [ ] `madge --circular` reports no cycles in core packages.
- [ ] Heavy, rarely used features load via dynamic import (check bundle analyzer).

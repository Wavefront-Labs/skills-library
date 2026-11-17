---
id: computing-software.web-development.frontend-development.es-module-exports-and-imports
name: es-module-exports-and-imports
category: computing-software
field: web-development
product: frontend-development
tags: [es-modules, javascript-modules, named-exports, re-exports, default-export, barrel-files, circular-imports, live-bindings]
level: practitioner
status: docs-checked
description: "Structuring ES modules: named vs default exports, re-exports and barrel files, live bindings, circular imports and their effect on tree shaking."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/export
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules
  - https://nodejs.org/api/esm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ES module exports and imports

**Goal:** modules with clear public APIs that tree-shake well and don't break on import order.

## 1. Prefer named exports
```js
export function formatPrice(n, cur) {}
export const TAX_RATE = 0.2;
import { formatPrice } from './money.js';
```
Named exports are greppable, refactor-safe, and auto-importable. Default exports allow any import name (`import x from`), which drifts across a codebase. Use default only where a tool requires it (some framework route/page files, `React.lazy` targets).

## 2. Re-exports
```js
export { formatPrice } from './money.js';
export * from './dates.js';            // does NOT re-export the default
export * as money from './money.js';   // namespace re-export
export { default as Chart } from './Chart.js';
```
**Barrel files** (`index.js` re-exporting everything) pull every re-exported module into the graph of anything that imports the barrel. In apps, import from the specific file; reserve barrels for a package's public entry.

## 3. Live bindings
Imports are live read-only views: if the exporter reassigns `export let count`, importers see the new value. Importers can't assign to them (TypeError). Export functions/getters to mutate state.

## 4. Circular imports
Allowed, but during evaluation one side sees uninitialised bindings: `ReferenceError: Cannot access 'X' before initialization` (TDZ) for `const`/`class`. Fixes: move the shared piece into a third module, import lazily inside functions, or invert the dependency.

## 5. Browser specifics
`<script type="module">` is deferred automatically and needs CORS-compatible loading (a `file://` page hits CORS errors). Module specifiers in the browser must be URLs or mapped via import maps (a bare `lodash` fails without one). Node ESM requires file extensions in relative imports.

## Verify
- [ ] Any circular import is understood and no module reads another's binding during evaluation.
- [ ] No module imports from another feature's internals instead of its public entry.

## Checked

2026-10-26. MDN export (`export *` does not re-export the default), import (live read-only bindings), Modules guide (modules deferred automatically, CORS errors on file://, import maps for bare names) and the Node ESM page (mandatory file extensions). Removed the unconfirmed Vite, sideEffects and madge statements.

Method: documentation only; no commands were run.

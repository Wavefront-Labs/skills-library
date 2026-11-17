---
id: computing-software.web-development.vite.performance-resolve-barrels
name: performance-resolve-barrels
category: computing-software
field: web-development
product: vite
tags: [resolve-extensions, explicit-import-paths, barrel-files, bundler-resolution]
level: practitioner
status: docs-checked
description: "Cut Vite resolve work: use explicit file extensions, narrow resolve.extensions, set TypeScript moduleResolution bundler, and avoid barrel files."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/performance.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Resolve cost: `resolve.extensions` defaults to `['.mjs', '.js', '.mts', '.ts', '.jsx', '.tsx', '.json']`. Importing `./Component` that is really `./Component.jsx` takes 6 filesystem checks (bare name, then each extension until `.jsx`). Be explicit instead: `import './Component.jsx'`. You can also narrow `resolve.extensions`, but verify it still works for files in `node_modules`. Plugin authors should call `this.resolve` only when needed.

TypeScript: enable `"moduleResolution": "bundler"` and `"allowImportingTsExtensions": true` to use `.ts` and `.tsx` extensions directly.

Barrel files re-export siblings:

```js
export * from './color.js'
export * from './dom.js'
export * from './slash.js'
```

Importing `{ slash } from './utils'` forces all files in the barrel to be fetched and transformed, since any may hold the API or have initialization side effects. Prefer the direct path:

```js
import { slash } from './utils/slash.js'
```

## Checked

Date: 2026-11-07

Read performance.md in full. Confirmed the resolve.extensions default list, the six-check example, explicit extensions, narrowing extensions with the node_modules caveat, this.resolve, the moduleResolution bundler and allowImportingTsExtensions tip, and the barrel file section. Nothing removed.

Method: documentation only; no commands were run.

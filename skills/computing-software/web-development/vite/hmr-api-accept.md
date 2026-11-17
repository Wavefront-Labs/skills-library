---
id: computing-software.web-development.vite.hmr-api-accept
name: hmr-api-accept
category: computing-software
field: web-development
product: vite
tags: [import-meta-hot, hot-accept, hmr-boundary, hmr-conditional-guard, hmr-typescript-types]
level: advanced
status: docs-checked
description: "Manual HMR API with import.meta.hot: guard for tree-shaking, vite/client types, hot.accept self-accept and dependency forms, and HMR boundary rules."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/api-hmr.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The client HMR API is mainly for framework and tooling authors. Plugin-side handling is `handleHotUpdate`.

Always guard use so it is tree-shaken in production:

```js
if (import.meta.hot) { /* HMR code */ }
```

For types, add `"types": ["vite/client"]` to `tsconfig.json` `compilerOptions`.

Self-accept: the callback gets the new module, which is `undefined` on a SyntaxError.

```js
export const count = 1
if (import.meta.hot) {
  import.meta.hot.accept((newModule) => {
    if (newModule) console.log('updated: count is now ', newModule.count)
  })
}
```

An accepting module is an HMR boundary. Vite does not swap the originally imported module: a boundary that re-exports a dep must update those re-exports itself (exports must use `let`), and importers above the boundary are not notified.

The call must literally appear as `import.meta.hot.accept(` (whitespace-sensitive) for static analysis.

Accept dependencies without reloading yourself:

```js
import.meta.hot.accept('./foo.js', (newFoo) => newFoo?.foo())
import.meta.hot.accept(['./foo.js', './bar.js'], ([newFoo, newBar]) => {})
```

With an array, only the updated module is non-null; after a failed update the array is empty.

## Checked

2026-11-07. Confirmed against guide/api-hmr.md, read in full: the plugin-side `handleHotUpdate` pointer, the `import.meta.hot` guard, the `vite/client` types entry, the self-accept example and `undefined` on SyntaxError, HMR boundary rules (re-exports with `let`, importers not notified), the whitespace-sensitive `import.meta.hot.accept(` requirement, and the dependency and array forms. Nothing removed.

Method: documentation only; no commands were run.

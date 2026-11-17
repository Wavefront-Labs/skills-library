---
id: computing-software.web-development.vite.optimize-deps-entries-include
name: optimize-deps-entries-include
category: computing-software
field: web-development
product: vite
tags: [optimize-deps-entries, optimize-deps-exclude, optimize-deps-include, nested-cjs-include]
level: advanced
status: docs-checked
description: "Control dep scanning with optimizeDeps.entries globs and ! ignores, exclude (CommonJS caveat), and include for linked packages or experimental deep-import globs."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/dep-optimization-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
These options only apply to the dependency optimizer, which is used only in dev.

- `optimizeDeps.entries` (`string | string[]`): by default Vite crawls `.html` files (ignoring `node_modules`, `build.outDir`, `__tests__`, `coverage`), or the top-level `input` / `build.rolldownOptions.input` if set. Custom `tinyglobby` patterns relative to root replace that inference; then only `node_modules` and `outDir` are ignored. Add `!` patterns to ignore more.
- `optimizeDeps.exclude`: skip pre-bundling. Do not exclude CommonJS deps. If an excluded ESM dep has a nested CommonJS dependency, include it with the `>` syntax:

```js
optimizeDeps: { include: ['esm-dep > cjs-dep'] }
```

- `optimizeDeps.include`: linked packages outside `node_modules` are not pre-bundled by default; list one to force it. Experimental: a trailing glob pre-bundles many deep imports at once, avoiding repeated re-bundling:

```js
optimizeDeps: { include: ['my-lib/components/**/*.vue'] }
```

## Checked

Date: 2026-11-07

Read dep-optimization-options.md in full. Confirmed entries inference and ignores, tinyglobby patterns, ! ignores, exclude CommonJS warning with the esm-dep > cjs-dep example, include for linked packages and the experimental trailing glob. Removed the claim that the options are "not inherited by environments": the page only shows a non-inherit badge and says the options apply to the dev-only optimizer.

Method: documentation only; no commands were run.

---
id: computing-software.web-development.vite.migration-v8-removals
name: migration-v8-removals
category: computing-software
field: web-development
product: vite
tags: [bundle-error, rollup-options-renamed, removed-hooks, v8-advanced-breaking]
level: advanced
status: docs-checked
description: "Vite 8 removals and deprecations: BundleError from build(), rollupOptions renamed to rolldownOptions, unsupported formats and hooks, and the advanced breaking changes."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/migration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
JS API: `build()` throws a `BundleError` (`Error & { errors?: RolldownError[] }`); read individual errors from `.errors`.

Deprecated (to be removed): `build.rollupOptions` (now `build.rolldownOptions`), `worker.rollupOptions` (now `worker.rolldownOptions`), `build.commonjsOptions` (no-op), `build.dynamicImportVarsOptions.warnOnError` (no-op), `resolve.alias[].customResolver` (use a plugin with `resolveId` and `enforce: 'pre'`). Passing a URL to `import.meta.hot.accept` was removed; pass an id.

Advanced breaking changes:
- Extglobs are not supported yet.
- TypeScript legacy namespace is only partially supported.
- `define` does not share object references between variables.
- `bundle` object: assigning `bundle[foo]` is unsupported (use `this.emitFile()`), the reference is not shared across hooks, and `structuredClone(bundle)` fails (clone `{ ...bundle }`).
- All parallel Rollup hooks run sequentially; `"use strict";` is sometimes not injected.
- Transforming to ES5 or below with plugin-legacy is unsupported; the same browser with several versions in `build.target` now errors.
- Unsupported by Rolldown: `output.format` `system` and `amd`, and the hooks `shouldTransformCachedModule`, `resolveImportMeta`, `renderDynamicImport`, `resolveFileUrl`.
- `parseAst` / `parseAstAsync` are deprecated for `parseSync` / `parse`.

## Checked

Date: 2026-11-07

Read migration.md in full. Confirmed: BundleError type and .errors, the five "Other Related Deprecations", the removed URL argument to import.meta.hot.accept, and every bullet under Advanced (extglobs, namespace, define, bundle object, sequential hooks, plugin-legacy ES5, build.target duplicates, unsupported system/amd formats and hooks, parseAst). Nothing removed.

Method: documentation only; no commands were run.

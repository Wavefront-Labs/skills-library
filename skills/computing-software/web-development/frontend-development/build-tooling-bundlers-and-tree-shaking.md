---
id: computing-software.web-development.frontend-development.build-tooling-bundlers-and-tree-shaking
name: build-tooling-bundlers-and-tree-shaking
category: computing-software
field: web-development
product: frontend-development
tags: [vite, webpack, esbuild, rollup, tree-shaking, code-splitting, bundler, source-maps, esm, commonjs, web-development]
level: advanced
status: docs-checked
description: "Modern frontend build tooling: why Vite's dev server is fast, tree-shaking requirements, manual code-splitting, and reading a bundle analyzer."
sources:
  - https://vitejs.dev/guide/why.html
  - https://webpack.js.org/guides/tree-shaking/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Build tooling — bundlers, tree-shaking, and why the bundle is big

**Goal:** understand what the bundler is actually doing so you can fix a slow dev
server or a bloated production bundle instead of guessing at config flags.

## 1. Why Vite's dev server is fast and webpack's isn't (by default)
Vite serves source files over native ESM in dev — the browser requests each
module directly, so Vite only transforms the file you're currently touching
(the Vite guide describes pre-bundling dependencies for dev). Webpack-based dev
servers bundle the app graph up front, so startup time scales with app
size. Check the current Vite docs for which bundler its production build uses,
as this has changed between versions.

## 2. Tree-shaking has hard requirements it silently fails
Tree-shaking (dropping unused exports from the final bundle) depends on static,
analyzable ESM `import`/`export` — not CommonJS (`require`/`module.exports`),
which the bundler can't safely analyze because `require` calls can be
conditional/dynamic. Importing one function from a library that is distributed
as CommonJS, or that has side effects at module scope, pulls in the whole
module even if you wrote a named import — prefer a package's ESM build
or a per-function subpath import. Check a library's
`package.json` for `"sideEffects": false` (or an explicit list) — without it,
bundlers must assume every module has side effects and keep it in regardless of
usage, which is the single most common reason tree-shaking "doesn't work."

## 3. Code splitting — automatic vs manual
Dynamic `import()` creates a natural split point the bundler turns into a
separate chunk, loaded on demand:
```js
const Chart = lazy(() => import('./Chart')); // React; separate chunk, loaded when rendered
```
Route-based splitting (one chunk per page) is the highest-value default for any
multi-page app. Beyond that, manual chunk configuration in your bundler groups rarely-changing vendor code into its
own cacheable chunk, so a deploy that only changes app code doesn't invalidate
the browser's cached copy of React/lodash/etc.

## 4. Reading a bundle analyzer, not just eyeballing dist size
Bundle analyzer plugins render a treemap by
module size *after* minification. Look for: one huge dependency pulled in for a
tiny usage (a date library imported for one format call — check for a
lighter alternative or named-import-only path), duplicate versions of the same
package (two major versions of a lib both bundled — usually a transitive
dependency mismatch, fixable with a package-manager override/resolution), and
polyfills included for browsers you don't actually need to support (check
`.browserslistrc`/`target` — a too-conservative target ships unnecessary
transpiled code and polyfills to everyone).

## 5. Source maps — dev speed vs production debuggability tradeoff
A cheap source-map setting gives fast rebuilds with good-enough mapping in dev. In production, generate full source
maps but **don't serve them publicly** — upload them to your error-tracking
tool (Sentry) and keep them off the CDN, or anyone can reconstruct readable
source from a public bundle.

## 6. ESM/CJS interop headaches
A package that's ESM-only (`"type": "module"`, no `main` field) can't be
`require()`'d from CommonJS code without dynamic `import()`. Mixed-module
monorepos hit this most; check a dependency's `exports` map in `package.json`
before assuming a straightforward `require` will work after an upgrade.

## Verify
- [ ] Bundle analyzer run at least once per major dependency change; no duplicate major versions of the same package.
- [ ] Imports from large libraries use ESM-friendly paths, not full-module CJS imports.
- [ ] Route-level code splitting exists for any app with more than a couple of pages/views.
- [ ] Vendor chunk is split from app code so routine deploys don't invalidate the whole cache.
- [ ] Production source maps exist for error tracking but are not publicly served from the CDN.

## Checked
2026-10-28. Confirmed on the webpack tree-shaking guide: `sideEffects` in package.json (false or a list), ESM requirement, `/*#__PURE__*/`. Vite guide: dev serving via native ESM; it notes Vite originally used esbuild and Rollup and has since changed. Removed: lodash-es names, `manualChunks`/`splitChunks` option paths, named analyzer plugins and the source-map preset (not on the fetched pages).
Method: documentation only; no commands were run.

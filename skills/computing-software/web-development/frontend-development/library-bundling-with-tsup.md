---
id: computing-software.web-development.frontend-development.library-bundling-with-tsup
name: library-bundling-with-tsup
category: computing-software
field: web-development
product: frontend-development
tags: [tsup, library-bundling, esbuild, rollup, publint, are-the-types-wrong, npm-package]
level: practitioner
status: verified
description: "Building and publishing a TypeScript library with tsup (or Rollup): ESM+CJS outputs, d.ts generation, exports map, externals, sideEffects, and publint/attw checks."
sources:
  - https://tsup.egoist.dev/
  - https://publint.dev/docs/
  - https://github.com/arethetypeswrong/arethetypeswrong.github.io
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Library bundling with tsup

App bundlers (Vite) optimise for browsers; libraries need clean, tree-shakable modules with types and correct `exports`.

## 1. Build
```bash
npm i -D tsup typescript
npx tsup src/index.ts --format esm,cjs --dts --sourcemap --clean --target es2020
```
```ts
// tsup.config.ts
import { defineConfig } from "tsup";
export default defineConfig({
  entry: { index: "src/index.ts", react: "src/react.tsx" },
  format: ["esm", "cjs"], dts: true, sourcemap: true, clean: true, treeshake: true,
  external: ["react", "react-dom"],          // peer deps never bundled
});
```
tsup uses esbuild (fast, **no type checking**: run `tsc --noEmit` separately). With TypeScript 6 the `--dts` step failed with `TS5101: Option 'baseUrl' is deprecated` until `"ignoreDeprecations": "6.0"` was added to tsconfig (tsup injects `baseUrl` itself); check your tsup/TS pairing. Alternatives: `tsdown` (Rolldown-based), `unbuild`, or Rollup + `rollup-plugin-dts` for fine control.

## 2. package.json
```json
{
  "name": "@acme/ui", "type": "module", "sideEffects": false,
  "exports": {
    ".":       { "import": { "types": "./dist/index.d.ts", "default": "./dist/index.js" },
                 "require": { "types": "./dist/index.d.cts", "default": "./dist/index.cjs" } },
    "./react": { "import": "./dist/react.js", "require": "./dist/react.cjs" },
    "./package.json": "./package.json"
  },
  "files": ["dist"],
  "peerDependencies": { "react": "^18 || ^19" }
}
```
- `types` first inside each condition; separate `.d.ts`/`.d.cts` so CJS consumers get CJS types.
- `sideEffects: false` lets consumers tree-shake; list CSS files if you import them (`["**/*.css"]`).
- Consider ESM-only for new packages (`require()` of ESM is unflagged from Node 22.12 and 20.19; the module must have no top-level await).

## 3. Check before publishing
```bash
npx publint                         # exports/files/package.json mistakes
npx @arethetypeswrong/cli --pack    # types resolution under node16, bundler, CJS/ESM
npm pack --dry-run                  # what actually ships
```

## Gotchas
- Bundling a dependency duplicates it in consumers (two Reacts = invalid hook call); externalise deps and peer deps.
- `"use client"` in a source file is dropped (warning: "Module level directives cause errors when bundled"). Re-add it with `banner: { js: '"use client";' }` - but with `treeshake: true` (Rollup pass) even the banner was stripped in a test; omit `treeshake` for those builds and check `dist/*.js` line 1.
- A module with named and default exports builds to CJS `exports.default`/`exports.hi`; consumers must use `.default` (Rollup warns about it). Prefer named exports only.
- `publint` also suggests an `engines.node` field; `attw` flags `node10` resolution as failed for exports-only packages (expected unless you add `main`/`types` fallbacks).

## Verify
- [ ] publint and attw report no errors; a fresh Vite app and a Node CJS script both import the package.

---
id: computing-software.software-engineering.typescript.bundling-libraries-with-tsup-and-esbuild
name: bundling-libraries-with-tsup-and-esbuild
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, tsup, esbuild, dual-package, library-bundling, rollup, declaration-files]
level: practitioner
status: verified
description: "Build TypeScript libraries for npm with tsup/esbuild: ESM plus CJS outputs, .d.ts generation, externals, exports map alignment, and validating with publint and attw."
sources: ["https://tsup.egoist.dev/", "https://esbuild.github.io/api/", "https://publint.dev/", "https://arethetypeswrong.github.io/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bundling libraries with tsup and esbuild

**Goal:** a published package that imports correctly from ESM, CJS, bundlers and
TypeScript, with accurate types.

> Status check: the tsup README now says the project is not actively maintained and points to
> tsdown (migration guide at tsdown.dev). The config below ran on tsup 9.0.0 with TypeScript 5.9.3.
> With TypeScript 7.0.2 installed, `dts: true` failed ("rollup-plugin-dts requires the TypeScript
> compiler API"); adding `@typescript/typescript6` then failed with
> `parseJsonConfigFileContent is not a function`, so keep `typescript@5.x` for tsup dts builds.

## Do you need a bundler?
For Node-only ESM libraries, plain `tsc` output (one `.js` + `.d.ts` per source file) is
simplest and tree-shakes best. Use tsup/esbuild when you need CJS + ESM dual output, browser
bundles, or to inline small internal modules.

## tsup config
```ts
// tsup.config.ts
import { defineConfig } from "tsup";
export default defineConfig({
  entry: ["src/index.ts", "src/cli.ts"],
  format: ["esm", "cjs"],
  dts: true,                 // rollup-based .d.ts (and .d.cts for cjs)
  sourcemap: true,
  clean: true,
  target: "node20",
  splitting: false,
  treeshake: true,
});
```
Dependencies and peerDependencies are external by default (not bundled); devDependencies
imported at runtime get inlined - check what ends up in `dist/` (tested: `is-odd` as a dependency stayed an `import`, `is-even` as a devDependency was inlined).
Output names depend on `"type"`: with `"type": "module"` tsup wrote `index.js` (esm) and `index.cjs`; without it, `index.js` is CJS and ESM is `index.mjs`.

## Matching package.json
```json
{
  "type": "module",
  "exports": {
    ".": {
      "import": { "types": "./dist/index.d.ts", "default": "./dist/index.js" },
      "require": { "types": "./dist/index.d.cts", "default": "./dist/index.cjs" }
    }
  },
  "main": "./dist/index.cjs",
  "types": "./dist/index.d.ts",
  "files": ["dist"],
  "sideEffects": false
}
```
CJS consumers must get `.d.cts` types, or TS reports "masquerading as ESM" problems.

## Validate before publishing
```bash
npx publint                         # exports/files/main consistency
npx @arethetypeswrong/cli --pack .  # types resolve correctly under node10/node16/bundler
npm pack --dry-run
```
With the package.json above, publint reported no problems and attw showed green for node10, node16 (CJS and ESM) and bundler.

## Dual package hazard
Shipping both formats means a process can load two copies (one ESM, one CJS) - module-level
state and `instanceof` break. Keep libraries stateless, or ship ESM only (Node 20.19+/22.12+ can
`require()` ESM synchronously (tested on 20.20.2), which reduces the need for CJS builds).

## esbuild directly
```bash
esbuild src/index.ts --bundle --platform=node --format=esm --packages=external --outfile=dist/index.js
```
esbuild does not type-check or emit declarations: run `tsc --emitDeclarationOnly` (or
`isolatedDeclarations` tooling) alongside. Alternatives: Rollup (fine-grained control),
tsdown/unbuild/pkgroll.

## Verify
- [ ] publint and attw clean; an ESM and a CJS smoke test import the packed tarball.
- [ ] `dist/` contains no inlined copies of runtime dependencies.

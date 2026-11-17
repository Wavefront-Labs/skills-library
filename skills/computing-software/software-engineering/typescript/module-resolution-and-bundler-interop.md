---
id: computing-software.software-engineering.typescript.module-resolution-and-bundler-interop
name: module-resolution-and-bundler-interop
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, module-resolution, esm, cjs, commonjs, tsconfig, package-json, exports-field, bundler, vite, webpack, node16, moduleresolution, interop, dual-package]
level: advanced
status: docs-checked
description: "Diagnose ESM/CJS interop failures and tsconfig moduleResolution mismatches across tsc, bundlers, and Node's package.json exports field."
sources:
  - https://www.typescriptlang.org/docs/handbook/modules/reference.html
  - https://www.typescriptlang.org/tsconfig/#moduleResolution
  - https://www.typescriptlang.org/tsconfig/#paths
  - https://www.typescriptlang.org/tsconfig/#esModuleInterop
  - https://www.typescriptlang.org/docs/handbook/release-notes/typescript-6-0.html
  - https://nodejs.org/api/packages.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Module resolution and bundler interop — why the import works in dev but not in the build

**Goal:** stop "Cannot find module" and "require() of ES Module not supported" errors
that only show up in CI, production builds, or a specific bundler.

## 1. `moduleResolution` must match what actually runs the code
- `"node16"`/`"nodenext"` — mirrors real Node ESM/CJS resolution exactly (needs
  explicit file extensions in relative imports under ESM: `import "./x.js"`, even in
  `.ts` source — this trips up everyone coming from `"node"` resolution).
- `"bundler"` (TS 5.0+) — for code that a bundler (Vite, esbuild, webpack) will process,
  not run directly by Node. Allows extensionless imports and `exports`-field lookups
  without demanding Node's stricter runtime rules.
- `"node10"` (formerly `"node"`) — models Node.js before v10 and is deprecated in TypeScript 6.0; migrate to `nodenext` or `bundler`.

## 2. package.json `exports` overrides `main`/`module`/`types`
Modern packages gate what's importable via `exports`:
```json
"exports": {
  ".": { "types": "./dist/index.d.ts", "import": "./dist/index.mjs", "require": "./dist/index.cjs" },
  "./subpath": "./dist/subpath.js"
}
```
If `exports` is present, **anything not listed is unreachable** — `import x from
"pkg/dist/internal.js"` fails even though the file exists on disk, because `exports`
is an allowlist, not documentation. Fix: use the package's documented subpath.

## 3. The "default import" trap (CJS interop)
```ts
import express from "express";       // works with esModuleInterop
```
`esModuleInterop: true` emits helper code to ease importing CommonJS modules and enables `allowSyntheticDefaultImports` for type compatibility. TypeScript 6.0 deprecates setting `esModuleInterop` to `false`.

## 4. Dual-package hazard
A library that defines both `import` and `require` conditions can be loaded once per format; the Node.js docs describe the hazards of these conditions in their dual CommonJS/ES module packages section. Trace which `exports` condition each importer hit.

## 5. Path aliases need resolving twice
`tsconfig.json` `paths` (`"@/*": ["./src/*"]`) only affects **type-checking** — `tsc`
does not rewrite the emitted JS. Node/the bundler needs its own alias config
(for example Vite's `resolve.alias`, or Node's package.json `imports`) or imports resolve for the type-checker and then explode at
runtime with "Cannot find module '@/utils'".

## Gotchas
- `.ts` files importing `.js` extensions under `nodenext` looks wrong but is correct —
  it refers to the *emitted* file's extension, not the source's.

## Verify
- [ ] `moduleResolution` matches the actual runtime (node16/nodenext for Node ESM,
      bundler for bundler-processed code).
- [ ] A clean `tsc --build` + the actual bundler build both succeed, not just the dev server.
- [ ] Path aliases are configured in both tsconfig and the runtime/bundler, verified by
      a build (not just dev-server HMR, which is more forgiving).

Related: computing-software.software-engineering.typescript.strict-typescript-setup

## Checked
Checked 2026-10-25 against the TypeScript-Website modules reference, tsconfig reference and 6.0 release notes, and the Node.js packages docs. Confirmed: node16/nodenext, bundler and node10 (formerly node) module resolution modes, node10 deprecated in 6.0; `exports` encapsulation and significant key order; `.ts` source importing `.js` through extension substitution; `paths` does not change emitted import paths; esModuleInterop behaviour and its `false` setting deprecated in 6.0; Node documents hazards of the import/require conditions. Replaced the prose source titles with URLs and removed the unconfirmed claims about Jest resolution, circular imports, patching tools, alias tools and a duplicate-copy symptom.
Method: documentation only; no commands were run.

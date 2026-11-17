---
id: computing-software.software-engineering.typescript.tsconfig-target-and-lib
name: tsconfig-target-and-lib
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, tsconfig-target, tsconfig-lib, downlevel-emit, tsconfig-bases, types-option, tsconfig]
level: practitioner
status: docs-checked
description: "Set target, lib, module and types in tsconfig to match the runtime: what target downlevels vs what lib declares, tsconfig/bases presets, DOM vs Node globals and @types leakage."
sources:
  - https://www.typescriptlang.org/tsconfig/#target
  - https://www.typescriptlang.org/tsconfig/#lib
  - https://www.typescriptlang.org/tsconfig/#types
  - https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-0.html
  - https://www.typescriptlang.org/docs/handbook/release-notes/typescript-6-0.html
  - https://github.com/tsconfig/bases
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tsconfig target and lib

**Goal:** the compiler allows exactly the language features and globals your runtime
has - no more (runtime crashes), no less (needless downlevelling).

## target: syntax output
`target` decides which syntax TS rewrites; changing it also changes the default of `lib`. TypeScript 6.0 defaults `target` to the newest supported ECMAScript version (`es2025` at the time of that release) and deprecates `target: es5`. The `@tsconfig/node22` base uses `target: es2022` with `lib: ["es2024", "ESNext.Array", "ESNext.Collection", "ESNext.Iterator"]`; pick the base that matches your Node major.

## lib: which built-in APIs type-check
Defaults to match `target` (+ DOM). Set explicitly:
```json
{ "compilerOptions": { "target": "ES2022", "lib": ["ES2023"], "types": ["node"] } }   // Node service: no DOM
{ "compilerOptions": { "lib": ["ES2022", "DOM", "DOM.Iterable"] } }                    // browser app
```
`lib` newer than the runtime type-checks APIs the runtime may lack - lib is a promise about the runtime. Including `DOM` in a Node project lets
`window`/`document` references compile.

## types: stop @types leakage
Before TypeScript 6.0, every visible `node_modules/@types/*` package was included globally by default; since 6.0 `types` defaults to `[]`, so list the global typings you need (`"types": ["node"]`). Naming only what you need also cuts build time (the 6.0 notes report 20-50% for many projects). Restrict:
```json
"types": ["vite/client"]           // only these global type packages
```
Test files can use a separate tsconfig with its own `types`.

## Presets
```bash
npm i -D @tsconfig/node22 @tsconfig/strictest
```
```json
{ "extends": ["@tsconfig/node22/tsconfig.json", "@tsconfig/strictest/tsconfig.json"] }
```
Arrays in `extends` (TS 5.0+) combine several base configs.

## module / moduleResolution pairing
- Node ESM/CJS packages: `"module": "NodeNext"` (implies `moduleResolution: NodeNext`).
- Bundled apps (Vite, webpack): `"module": "ESNext", "moduleResolution": "Bundler"`.
- `"node10"` (formerly `"node"`) is deprecated in TypeScript 6.0.

## Verify
- [ ] `tsc --showConfig` output reviewed: target/lib/types match the deployed runtime.
- [ ] A Node-only project fails to compile `document.title` (no DOM lib).

## Checked
Checked 2026-10-25 against the TypeScript-Website tsconfig reference and 5.0 and 6.0 release notes and the tsconfig/bases repository (node22.json). Confirmed: changing `target` changes the default `lib`; `lib` can drop DOM for non-browser programs; `types` defaults to `[]` from 6.0 (all visible @types before); 6.0 target default and `es2025` option; `target: es5` and `moduleResolution node10` deprecated in 6.0; `extends` accepts an array (5.0); the node22 base values; `tsc --showConfig`. Removed the unconfirmed syntax-per-target examples, the runtime-to-target table, the `@types/node` browser example and the vitest globals example.
Method: documentation only; no commands were run.

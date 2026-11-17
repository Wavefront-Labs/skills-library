---
id: computing-software.web-development.node-express.running-typescript-in-node
name: running-typescript-in-node
category: computing-software
field: web-development
product: node-express
tags: [node, node-typescript, type-stripping, tsx, erasable-syntax, typescript, esm, web-development]
level: practitioner
status: verified
description: "Running TypeScript in Node: native type stripping (22.18+/23.6+), erasable-only syntax and tsconfig flags, tsx for full TS, type-checking with tsc and production builds."
sources:
  - https://nodejs.org/api/typescript.html
  - https://www.typescriptlang.org/tsconfig/#erasableSyntaxOnly
  - https://tsx.is/
  - https://nodejs.org/en/learn/typescript/run-natively
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running TypeScript in Node

**Goal:** run `.ts` directly in dev and production with predictable behaviour, and still type-check.

## 1. Native type stripping
Node 23.6+ and 22.18+ run `.ts` files without flags (22.6-22.17: `--experimental-strip-types`; confirmed: 22.6 and 22.17 fail with `ERR_UNKNOWN_FILE_EXTENSION` without it, 22.18 and 24 run the file). Type stripping is stable from Node 24.12 / 25.2. Node replaces type annotations with whitespace - **no type checking, no downlevelling**.
```bash
node src/server.ts
node --watch src/server.ts
```

## 2. Only erasable syntax
Rejected by native type stripping (`ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX`, checked on Node 22.18 and 24): `enum`, `namespace` with runtime code, parameter properties (`constructor(private x)`) and `import x = require()`. `--experimental-transform-types` (Node 22.7+) made enum, namespace and parameter properties work in Node 22.18, but not `import x = require()`, and the Node docs say the flag was removed in v26.0.0. Decorators are a parse error (`SyntaxError`) either way. Use unions/`as const` objects instead of enums.

Also required:
- `import type { User } from "./user.ts"` for type-only imports (otherwise the import stays and fails at runtime).
- Explicit `.ts` extensions in relative imports.
- `tsconfig` paths aliases are **not** resolved (`ERR_MODULE_NOT_FOUND`) - use package.json `"imports"` (`#lib/*`). With `rewriteRelativeImportExtensions`, `tsc` 7.0 reports TS2877 for a `#lib/a.ts` specifier because it is not relative, so write the target extension the compiled output will have (or drop the option for run-only code).
- Files under `node_modules` are not stripped (publish JS); `--experimental-strip-private-modules` relaxes this only for packages with `"private": true`.

## 3. tsconfig for native TS
```json
{
  "compilerOptions": {
    "target": "esnext", "module": "nodenext",
    "noEmit": true,
    "erasableSyntaxOnly": true,
    "verbatimModuleSyntax": true,
    "allowImportingTsExtensions": true,
    "rewriteRelativeImportExtensions": true,
    "strict": true
  }
}
```
`erasableSyntaxOnly` (Node docs recommend TS 5.8 or newer) makes tsc reject `enum`, runtime `namespace`, parameter properties and `import =` (TS1294; run with tsc 7.0.2).

## 4. Type-check separately
`tsc --noEmit` in CI and a pre-commit/editor step. Running code proves nothing about types.

## 5. tsx when you need full TypeScript
`npx tsx src/server.ts`, `tsx watch`, `node --import tsx` - esbuild-based, supports enums, parameter properties, decorators, path aliases (via tsconfig; each run on tsx 4.23), CJS/ESM interop. Also no type checking.

## 6. Production
Options: run `.ts` natively (simple, startup cost small), or compile with `tsc`/`tsup`/`esbuild` to `dist/` and run JS (needed for libraries, older Node, non-erasable syntax). Source maps: `node --enable-source-maps dist/server.js`.

## Verify
- [ ] `node --version` meets the minimum in `engines` and the Dockerfile base image.
- [ ] `tsc --noEmit` runs in CI.
- [ ] No `enum`/parameter properties when using native stripping (`erasableSyntaxOnly` enforces).

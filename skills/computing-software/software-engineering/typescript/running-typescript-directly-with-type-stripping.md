---
id: computing-software.software-engineering.typescript.running-typescript-directly-with-type-stripping
name: running-typescript-directly-with-type-stripping
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, type-stripping, erasablesyntaxonly, tsx-runner, node-strip-types, verbatimmodulesyntax, nodejs]
level: practitioner
status: gated
description: "Run .ts files without a build step: Node's built-in type stripping, erasableSyntaxOnly and verbatimModuleSyntax constraints, tsx for full syntax, and keeping tsc for type checks."
sources: ["https://nodejs.org/api/typescript.html", "https://www.typescriptlang.org/tsconfig/#erasableSyntaxOnly", "https://www.typescriptlang.org/tsconfig/#verbatimModuleSyntax", "https://tsx.is/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running TypeScript directly with type stripping

**Goal:** scripts and services that run `.ts` source directly, with type checking done
separately - no `dist/` for dev tooling.

## Node's built-in support
Node 22.6 added type stripping behind `--experimental-strip-types`; Node 23.6+/22.18+ strip types by default (no experimental warning from 24.3/22.18; stable from 24.12/25.2):
```bash
node src/server.ts
```
Node replaces type annotations with whitespace (source positions stay correct, no source maps
needed) (gated: unconfirmed, source is paywalled or blocked). It does **not** type-check and does **not** read tsconfig.

### What is not supported (non-erasable syntax)
- `enum`, `namespace` with values, parameter properties (`constructor(private x)`), legacy
  `import x = require()`; these need code generation and fail with `ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX` (checked on Node 24.22). `--experimental-transform-types` (added 22.7, removed in Node 26) handles them.
- Path aliases from tsconfig `paths`; use package.json `imports` (`#lib/*`) instead.
- Import specifiers must include the extension: `import { x } from "./util.ts"`.
- Files in `node_modules` are not stripped (publish JS).

### tsconfig to match
`verbatimModuleSyntax` with `module: NodeNext` also needs `"type": "module"` in package.json, otherwise tsc reports TS1295/TS1287 on every `import`/`export` (checked with TypeScript 7.0.2).
```json
{
  "compilerOptions": {
    "noEmit": true,
    "module": "NodeNext",
    "allowImportingTsExtensions": true,
    "rewriteRelativeImportExtensions": true,     // TS 5.7: emit .js if you also build
    "erasableSyntaxOnly": true,                  // TS 5.8: error on enums/param props/namespaces
    "verbatimModuleSyntax": true                 // type-only imports must use `import type`
  }
}
```
`verbatimModuleSyntax` matters because a stripper cannot know whether `import { User }` is a
type; write `import type { User }` so it is removed entirely.

## tsx (esbuild-based runner)
```bash
npx tsx watch src/server.ts
```
Supports full TS syntax incl. enums (checked: `enum` runs under tsx) and tsconfig paths, ESM and CJS. Also no type checking. (`tsx watch` subcommand exists.)

## Keep type checking
```json
"scripts": { "dev": "node --watch src/server.ts", "typecheck": "tsc --noEmit", "test": "node --test" }
```
Run `typecheck` in CI and pre-push; the runtime will happily execute type-incorrect code.

## When to still build
Publishing libraries (ship JS + `.d.ts`), targeting older runtimes, bundling for browsers,
or startup-critical services (stripping costs a little at load (gated: unconfirmed, source is paywalled or blocked)).

## Verify
- [ ] `tsc --noEmit` with `erasableSyntaxOnly` passes, guaranteeing Node can strip every file.
- [ ] CI runs the same Node version used in production.

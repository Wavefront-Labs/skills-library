---
id: computing-software.software-engineering.typescript.typescript-compiler-performance
name: typescript-compiler-performance
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, incremental-build, extendeddiagnostics, skiplibcheck, generatetrace, tsbuildinfo, typescript-build]
level: advanced
status: docs-checked
description: "Speed up slow tsc and editor type checking: incremental and tsbuildinfo, skipLibCheck, --extendedDiagnostics and --generateTrace, include scoping and expensive type patterns."
sources:
  - https://github.com/microsoft/TypeScript/wiki/Performance
  - https://www.typescriptlang.org/tsconfig/#incremental
  - https://www.typescriptlang.org/tsconfig/#skipLibCheck
  - https://www.typescriptlang.org/tsconfig/#composite
  - https://www.typescriptlang.org/tsconfig/#disableSourceOfProjectReferenceRedirect
  - https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-5.html#isolated-declarations
  - https://www.typescriptlang.org/docs/handbook/release-notes/typescript-6-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TypeScript compiler performance

**Goal:** CI type checks in seconds and a responsive editor on large codebases.

## Measure first
```bash
npx tsc --noEmit --extendedDiagnostics
npx tsc --noEmit --listFilesOnly | wc -l          # are you checking node_modules or dist by accident?
npx tsc --noEmit --generateTrace trace/            # then: npx @typescript/analyze-trace trace/
```
A high file count points at `include`/`types` scoping; use the trace to find expensive types.

## Cheap wins
```json
{
  "compilerOptions": {
    "incremental": true,                 // writes .tsbuildinfo; re-checks only affected files
    "skipLibCheck": true,                // don't type-check every .d.ts in node_modules
    "types": ["node"]                    // don't load every @types package
  },
  "include": ["src"],                    // not "**/*" (pulls in dist, coverage, scripts)
  "exclude": ["**/*.test.ts"]            // if tests are checked by a separate config
}
```
Cache `.tsbuildinfo` between CI runs. `skipLibCheck` hides conflicts between library typings;
accepted trade-off almost everywhere.

## Split large repos
Project references (`composite: true`, `tsc -b`) check packages independently and in parallel
order, reusing `.d.ts` outputs of dependencies instead of re-checking their sources.
`isolatedDeclarations` (TS 5.5) lets tools generate declarations without type checking.

## Expensive type patterns
- Large unions: the wiki recommends preferring base types over unions.
- Intersections of many object types: prefer `interface X extends A, B` (cached).
- Missing return type annotations on exported functions force inference through complex bodies;
  annotations act as checkpoints.
- Large inferred types re-printed into declaration files - name them with an alias/interface.

## Editor (tsserver)
- Exclude generated folders; `disableSourceOfProjectReferenceRedirect` makes the editor use `.d.ts` outputs instead of sources at project-reference boundaries.

## Native compiler
TypeScript 7.0 is the native (Go) port of the compiler; options deprecated in TypeScript 6.0 are removed there, so clear the 6.0 deprecation warnings first (6.0 release notes).

## Verify
- [ ] `--extendedDiagnostics` numbers recorded before/after changes.
- [ ] CI caches tsbuildinfo; `--listFilesOnly` shows only intended sources.

## Checked
Checked 2026-10-25 against the TypeScript performance wiki, the tsconfig reference and the 5.5 and 6.0 release notes. Confirmed: `--extendedDiagnostics`, `--listFilesOnly`, `--generateTrace` with `@typescript/analyze-trace`; `incremental` and `.tsbuildinfo`; `skipLibCheck` skips all .d.ts files; `composite` makes incremental the default for project references; extending interfaces over intersections; return type annotations save work; naming complex types; base types over unions; `disableSourceOfProjectReferenceRedirect`; `isolatedDeclarations` (5.5); TypeScript 7.0 is the native port and removes options deprecated in 6.0. Removed the unconfirmed speed multiplier, tsserver memory setting, cache path, recursion-explosion claim and `Instantiations` remark.
Method: documentation only; no commands were run.

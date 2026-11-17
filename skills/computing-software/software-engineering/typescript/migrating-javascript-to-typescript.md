---
id: computing-software.software-engineering.typescript.migrating-javascript-to-typescript
name: migrating-javascript-to-typescript
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, js-to-ts-migration, allowjs, checkjs, jsdoc-types, incremental-adoption, ts-expect-error]
level: practitioner
status: docs-checked
description: "Migrate a JavaScript codebase to TypeScript incrementally: allowJs and checkJs, JSDoc types, file-by-file conversion order, temporary escape hatches and ratcheting strictness."
sources:
  - https://www.typescriptlang.org/docs/handbook/migrating-from-javascript.html
  - https://www.typescriptlang.org/docs/handbook/intro-to-js-ts.html
  - https://www.typescriptlang.org/docs/handbook/jsdoc-supported-types.html
  - https://www.typescriptlang.org/tsconfig/#checkJs
  - https://nodejs.org/api/typescript.html
  - https://github.com/pahen/madge#readme
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating JavaScript to TypeScript

**Goal:** move a live JS codebase to TS without a big-bang rewrite or a frozen
feature pipeline.

## Phase 0: TypeScript compiles your JS
```json
{
  "compilerOptions": {
    "allowJs": true, "checkJs": false, "noEmit": true,
    "target": "ES2022", "module": "NodeNext", "strict": false,
    "skipLibCheck": true, "esModuleInterop": true
  },
  "include": ["src"]
}
```
Add `tsc --noEmit` to CI immediately; it should pass with zero errors.

## Phase 1: type-check JS with JSDoc
Enable per file with `// @ts-check` at the top, or `checkJs: true` globally. Add types without renaming:
```js
/** @typedef {{ id: string, total: number }} Order */
/** @param {Order[]} orders @returns {number} */
export function sum(orders) { return orders.reduce((a, o) => a + o.total, 0); }
/** @type {import("./config.js").Config} */
```
Install `@types/*` packages for dependencies.

## Phase 2: rename files, leaves first
1. Convert modules with no internal imports (utils, types, constants) first, then work up the
   dependency graph (`madge --leaves src` lists them). Converting high-level files first
   means typing against untyped dependencies.
2. Rename `.js` -> `.ts` in a commit with **no other changes** (git keeps rename history), fix
   errors in the next commit.
3. Write types for shared domain objects early; they pay off everywhere.

## Escape hatches (temporary, tracked)
- `// @ts-expect-error: reason` over `// @ts-ignore` - it errors when no longer needed.
- `unknown` + narrowing instead of `any` for untyped input; `any` only with an eslint-disable
  comment explaining why.
- Track counts in CI (grep `@ts-expect-error`, `: any`) and drive them down.

## Phase 3: ratchet strictness
Turn on one flag at a time, fix, commit: `noImplicitAny` -> `strictNullChecks` -> remaining `strict` family -> `noUncheckedIndexedAccess`. For huge codebases, a second, stricter tsconfig that includes only converted directories lets you enforce strict mode on new files first.

## Build and runtime
Keep the existing bundler; most (Vite, esbuild, webpack + ts-loader/babel) handle `.ts`.
Node: `tsc` to `dist/`, or run TS directly with type stripping during migration.

## Verify
- [ ] CI runs `tsc --noEmit` from day one; error count only decreases.
- [ ] Percentage of `.ts` files and count of `any`/`@ts-expect-error` reported per sprint.

## Checked
Checked 2026-10-25 against the TypeScript-Website handbook and tsconfig reference, the Node.js TypeScript docs and the madge README. Confirmed: allowJs, checkJs and noEmit options; `checkJs` equals adding `// @ts-check` to every JS file; `@ts-expect-error` (3.9); noImplicitAny and strictNullChecks as separate flags; noUncheckedIndexedAccess is not part of strict; `madge --leaves`; Node can run erasable TypeScript by type stripping (enabled by default in current releases). Removed the unconfirmed `@ts-nocheck` note, the typescript-strict-plugin recommendation and a payoff claim.
Method: documentation only; no commands were run.

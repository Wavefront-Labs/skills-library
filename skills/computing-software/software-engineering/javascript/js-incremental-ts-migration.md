---
id: computing-software.software-engineering.javascript.js-incremental-ts-migration
name: js-incremental-ts-migration
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, allowjs-migration, js-ts-interop]
level: practitioner
status: docs-checked
description: "Migrate a JS codebase to TypeScript file by file with allowJs, then raise strictness with noImplicitAny and strictNullChecks."
sources: ["https://www.typescriptlang.org/docs/handbook/migrating-from-javascript.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Incremental TypeScript migration steps

- Separate inputs from outputs so TypeScript does not overwrite your sources. Bare-bones `tsconfig.json`: `{ "compilerOptions": { "outDir": "./built", "allowJs": true, "target": "es5" }, "include": ["./src/**/*"] }`. Running `tsc` then emits into `built` mirroring `src`.
- Early benefits with no renames: editor completion, and checks such as `noImplicitReturns` and `noFallthroughCasesInSwitch`. TypeScript also warns about unreachable code and labels (`allowUnreachableCode`, `allowUnusedLabels` disable that).
- Move file by file: rename one `.js` file to `.ts` (`.tsx` if it uses JSX). Errors do not block output by default; `noEmitOnError` stops emitting on errors. TypeScript has a strictness dial.
- If you plan to use strict settings, turn them on before editing files, for example `noImplicitAny`.
- Replace `require`/`define` calls with TypeScript imports; set the `module` option first (valid values include `commonjs`, `amd`, `system`, `umd`). A fallback is `declare function require(path: string): any;`, but converting is better. `module.exports = foo` becomes `export = foo`; named exports become `export function ...`.
- "Cannot find module" errors usually mean missing declaration files: install them, for example `npm install -S @types/lodash`. With a module option other than `commonjs`, set `moduleResolution` to `node`.
- Calls with varying argument counts need function overloads; sequentially added properties (`options.color = ...` on `{}`) need the properties moved into the literal or a typed assertion.
- Prefer `any` over `Object` or `{}` when you really mean "anything", but `any` loses most checking and editor support. Between `Object` and `{}`, prefer `{}`.
- Stricter checks after conversion: `noImplicitAny`; `strictNullChecks` (then `number | null` unions, and the postfix `!` operator for values you know are not null; dependencies may need updating too); `noImplicitThis` (fix with a `this:` parameter).

Self-check: with `noImplicitAny` on, a migrated file with an untyped parameter fails `tsc`.

## Checked

2026-11-08. Confirmed on the TypeScript Handbook "Migrating from JavaScript": config, early benefits, renaming, `noEmitOnError`, module and declaration-file fixes, overloads, `any`/`{}` guidance, and the strictness flags. Removed the leaf-modules-first ordering, `checkJs: false` / `noEmit: true` settings, the `unknown` and `// @ts-expect-error` advice, `declare module "x";` stubs, and the progress-counting script, none of which the page states.

Method: docs-only read of cited pages, 2026-11-08

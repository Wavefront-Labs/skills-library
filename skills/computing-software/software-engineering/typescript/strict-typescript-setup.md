---
id: computing-software.software-engineering.typescript.strict-typescript-setup
name: strict-typescript-setup
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, tsconfig, strict, nouncheckedindexedaccess, exactoptionalpropertytypes, nodenext, moduleresolution, bundler, esm, commonjs, verbatimmodulesyntax, isolatedmodules, tsc, noemit, type-checking, ci, typescript-eslint, vite, node, project-references, skiplibcheck]
level: practitioner
status: docs-checked
description: "Set up a strict tsconfig: which flags beyond strict to enable, choosing module/moduleResolution (NodeNext vs bundler), ESM vs CJS interop, and enforcing type-checks in CI."
sources:
  - https://www.typescriptlang.org/tsconfig/
  - https://www.typescriptlang.org/docs/handbook/modules/reference.html
  - https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-9.html
  - https://www.typescriptlang.org/docs/handbook/release-notes/typescript-6-0.html
  - https://nodejs.org/api/modules.html#loading-ecmascript-modules-using-require
  - https://typescript-eslint.io/getting-started/typed-linting/
  - https://github.com/tsconfig/bases
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Strict TypeScript setup — a tsconfig that catches bugs, not one that fights you

**Goal:** a tsconfig whose strictness catches real defects (undefined index access,
unhandled nulls), with module settings that match how the code actually runs, and a
CI step that blocks type errors.

## 1. Pick the module mode from the runtime, not by taste
| Code runs via… | `module` | `moduleResolution` |
|---|---|---|
| Node directly (tsc output, libraries for Node) | `NodeNext` (or `Node20` in TS 5.9+) | `NodeNext` |
| A bundler (Vite, webpack, esbuild, Next.js) | `ESNext` / `Preserve` | `Bundler` |
| Bun | `Preserve` | `Bundler` |
Under `NodeNext`, ESM vs CJS per file follows `package.json` `"type"` and the extension
(`.mts`/`.cts`), and **relative imports need the runtime extension**: `import "./db.js"`
even though the source is `db.ts` (TS 5.7+ can rewrite `.ts` imports with
`rewriteRelativeImportExtensions`). `Bundler` drops the extension requirement but
emits code Node can't run unbundled. `node10` (formerly `node`) is deprecated in TypeScript 6.0.

## 2. The tsconfig
```jsonc
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,                         // strictNullChecks, noImplicitAny, etc.
    "noUncheckedIndexedAccess": true,       // arr[i] / record[k] is T | undefined
    "exactOptionalPropertyTypes": true,     // {a?: string} rejects {a: undefined}
    "noImplicitOverride": true,
    "noFallthroughCasesInSwitch": true,
    "noPropertyAccessFromIndexSignature": true,
    "useUnknownInCatchVariables": true,     // already in strict; listed for clarity
    "verbatimModuleSyntax": true,           // forces `import type`; no elided surprises
    "isolatedModules": true,                // safe for esbuild/swc per-file transpile
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true,                   // don't type-check node_modules .d.ts
    "declaration": true, "sourceMap": true,
    "outDir": "dist", "rootDir": "src"
  },
  "include": ["src"]
}
```
The `@tsconfig/strictest` and `@tsconfig/node22` packages are reasonable bases to
`extends`. Note `"strict": true` gains new sub-flags in some releases — expect new
errors when upgrading TypeScript.

## 3. Living with `noUncheckedIndexedAccess`
It is the highest-value flag beyond `strict` and the most annoying at first:
```ts
const first = items[0];            // T | undefined
if (first === undefined) throw new Error("empty");
```
Use `.at()`, `Map.get()` + checks, or a small `assertDefined()` helper — not `!`.

## 4. ESM / CJS interop
- New Node packages: `"type": "module"`, publish ESM; ship dual ESM+CJS only if
  consumers need it (validate with
  `npx @arethetypeswrong/cli`).
- Node 22.12+/20.19+ can `require()` synchronous ESM, which removed most of the pain
  of CJS consumers — check your minimum Node version.
- `esModuleInterop` is on in the `@tsconfig/node22` base, and TypeScript 6.0 deprecates turning it off.

## 5. Type-checking in CI
Transpilers (esbuild, swc, Vite, `tsx`, Node's type stripping) **do not type-check**.
Add an explicit step:
```
tsc --noEmit                 # or: tsc -b for project references
```
Pair with type-aware lint: typescript-eslint `recommendedTypeChecked` with
`parserOptions.projectService: true`; key rules `no-floating-promises`,
`no-misused-promises`, `strict-boolean-expressions` (optional). Monorepos: project
references + `composite: true` and `tsc -b` for incremental builds.

## Gotchas
- `skipLibCheck: true` hides conflicts between installed `@types` versions — fine for
  speed, but a broken `.d.ts` you publish yourself won't be caught; check published
  types with `attw`.
- `paths` aliases are a type-checker feature only; the runtime/bundler needs its own
  mapping (Node: `"imports"` with `#alias` in package.json is the portable option).
- `as` casts and `any` from untyped JSON (`JSON.parse`, `fetch().json()`) bypass
  everything — validate at boundaries (zod/valibot) and type the result.
- Enabling strict flags on an existing codebase: turn on per-flag and fix, or use
  `// @ts-expect-error` with a ticket — never `// @ts-ignore` (it doesn't fail when
  the error disappears).
- TypeScript 6.0 changed defaults (`strict` is true, `module` is `esnext`, `types` is `[]`, so add
  `"types": ["node"]` for Node globals), and options it deprecates are removed in 7.0 (the native
  compiler) — check the 6.0 release notes before upgrading.

## Verify
- [ ] `module`/`moduleResolution` match the runtime (Node → NodeNext; bundled → Bundler).
- [ ] `strict`, `noUncheckedIndexedAccess`, `verbatimModuleSyntax` are on.
- [ ] `node dist/index.js` runs with no "ERR_MODULE_NOT_FOUND" (extension issues).
- [ ] CI runs `tsc --noEmit` (or `tsc -b`) and fails the build on any error.
- [ ] Type-aware lint flags floating promises.
- [ ] Published packages pass `@arethetypeswrong/cli`.

## Checked
Checked 2026-10-25 against the TypeScript-Website tsconfig reference, modules reference and 5.x/6.0 release notes, the Node.js modules docs, the typescript-eslint typed linting guide and the tsconfig/bases repository. Confirmed: `module` node20 (5.9), `preserve`, and bundler resolution for Bun; `rewriteRelativeImportExtensions` (5.7); strict family membership of useUnknownInCatchVariables (4.4) while exactOptionalPropertyTypes is not in strict; `noUncheckedIndexedAccess`, `noPropertyAccessFromIndexSignature`, `noImplicitOverride`, `verbatimModuleSyntax`, `isolatedModules`, `skipLibCheck` option semantics; `@tsconfig/strictest` and `@tsconfig/node22` exist (node22 sets esModuleInterop true); require() of synchronous ESM in Node 22.12 and 20.19; `projectService` with `recommendedTypeChecked`; TypeScript 6.0 default changes (strict true, module esnext, types []) and the 7.0 removal of deprecated options. Replaced the prose source titles with URLs and removed unconfirmed claims about noUncheckedIndexedAccess destructuring and for-of, tsup/tsdown, vue-tsc and svelte-check, and NodeNext implying esModuleInterop.
Method: documentation only; no commands were run.

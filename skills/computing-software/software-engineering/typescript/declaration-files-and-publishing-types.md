---
id: computing-software.software-engineering.typescript.declaration-files-and-publishing-types
name: declaration-files-and-publishing-types
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, tsconfig, typescript-build, declaration-files, d-ts, types-field, definitelytyped, api-extractor]
level: practitioner
status: docs-checked
description: "Write and ship .d.ts files: emitting declarations, package.json types and exports conditions, typing untyped JS packages, DefinitelyTyped, and validating with attw."
sources:
  - https://www.typescriptlang.org/docs/handbook/declaration-files/introduction.html
  - https://www.typescriptlang.org/docs/handbook/modules/reference.html#packagejson-exports
  - https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-5.html#isolated-declarations
  - https://www.typescriptlang.org/tsconfig/#stripInternal
  - https://nodejs.org/api/packages.html#conditional-exports
  - https://github.com/arethetypeswrong/arethetypeswrong.github.io/tree/main/packages/cli
  - https://github.com/DefinitelyTyped/DefinitelyTyped#readme
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Declaration files (.d.ts): writing and publishing

**Goal:** consumers of your package (ESM, CJS, bundlers) get correct types, and untyped dependencies get typed safely.

## 1. Emit declarations from TS sources
```jsonc
// tsconfig.build.json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "declaration": true,
    "declarationMap": true,          // go-to-definition jumps to .ts source
    "emitDeclarationOnly": false,
    "outDir": "dist",
    "stripInternal": true            // drop members tagged /** @internal */ (documented as an internal option: the result is not checked)
  },
  "include": ["src"]
}
```
`isolatedDeclarations` (TS 5.5; needs `declaration` or `composite`) reports errors when a module cannot be turned into a declaration file without a type-checker, so exports need explicit annotations; other tools can then emit `.d.ts` quickly.

## 2. package.json wiring
```json
{
  "type": "module",
  "exports": {
    ".": {
      "import": { "types": "./dist/index.d.ts",  "default": "./dist/index.js" },
      "require": { "types": "./dist/index.d.cts", "default": "./dist/index.cjs" }
    }
  },
  "types": "./dist/index.d.ts",
  "files": ["dist"]
}
```
Key order in `exports` is significant (earlier conditions take precedence and `default` should come last), so put `types` before `import`/`require`/`default` inside each branch. Dual packages need separate `.d.ts`/`.d.cts`: `.d.cts` is always treated as CommonJS, `.d.mts` as ESM, and `.d.ts` follows the nearest `package.json` `"type"`.

## 3. Typing an untyped JS dependency
Quick local shim:
```ts
// src/types/legacy-lib.d.ts
declare module "legacy-lib" {
  export function parse(input: string, opts?: { strict?: boolean }): Record<string, unknown>;
  const version: string;
  export default version;
}
```
Make sure the file is included by `tsconfig` (`include`). Last resort: `declare module "legacy-lib";` (everything `any`).
Share it: contribute to DefinitelyTyped (`@types/legacy-lib`), with tests in `legacy-lib-tests.ts`.

## 4. Globals and ambient declarations
```ts
// global.d.ts
export {};
declare global {
  interface Window { __APP_CONFIG__: { apiUrl: string } }
  var __DEV__: boolean;
}
```
A `.d.ts` with no top-level import/export is a global script; adding one makes it a module (then use `declare global`).

## 5. Validate before publishing
```bash
npm pack                                    # the tarball that would be published
npx @arethetypeswrong/cli --pack .          # resolution problems per moduleResolution mode
```
## Gotchas
- `skipLibCheck: true` hides errors in your own shipped `.d.ts` too; check them in a consumer test project.
- Declarations referencing devDependency types (`import type { X } from "some-dev-dep"`) break consumers: those packages must be dependencies.
- Handwritten `.d.ts` beside JS drifts; prefer authoring in TS or JSDoc with `checkJs` and `declaration`.

## Verify
- attw reports no problems for node10, node16 (CJS and ESM) and bundler resolution, and a scratch consumer project type-checks against the packed tarball.

## Checked
Checked 2026-10-25 against the TypeScript-Website docs (TypeScript 6.0 era), the Node.js packages docs, the attw CLI README and the DefinitelyTyped README. Confirmed: isolatedDeclarations (5.5, needs declaration or composite); stripInternal is documented as an internal option; `exports` key order is significant with `default` last; `.d.cts` is always CommonJS; `--pack` in the attw CLI and its node10/node16/bundler modes; DefinitelyTyped `<my-package>-tests.ts` naming. Removed unconfirmed claims about tsup/tsdown, publint and API Extractor.
Method: documentation only; no commands were run.

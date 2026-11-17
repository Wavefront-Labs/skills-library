---
id: computing-software.software-engineering.typescript.path-aliases-and-tsconfig-paths
name: path-aliases-and-tsconfig-paths
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, tsconfig, typescript-build, path-aliases, tsconfig-paths, subpath-imports, baseurl, monorepo]
level: practitioner
status: docs-checked
description: "Set up import aliases that work in tsc, bundlers, tests and Node: tsconfig paths, why baseUrl is deprecated, package.json subpath imports, and workspace packages."
sources:
  - https://www.typescriptlang.org/tsconfig/#paths
  - https://www.typescriptlang.org/docs/handbook/modules/reference.html#paths
  - https://www.typescriptlang.org/docs/handbook/release-notes/typescript-6-0.html#deprecated---baseurl
  - https://nodejs.org/api/packages.html#subpath-imports
  - https://vite.dev/config/shared-options.html#resolve-alias
  - https://jestjs.io/docs/configuration#modulenamemapper-objectstring-string--arraystring
  - https://github.com/aleclarson/vite-tsconfig-paths
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Path aliases and tsconfig paths pitfalls

**Goal:** short, stable imports (`#lib/db`, `@app/ui`) that resolve identically in the type checker, bundler, test runner and Node at runtime.

## 1. The core pitfall
`compilerOptions.paths` only affects **type resolution**. `tsc` does not rewrite import specifiers in emitted JS, so `import x from "@/lib/db"` compiled with plain tsc fails at runtime in Node (`ERR_MODULE_NOT_FOUND` for ES modules) unless something else resolves it.

## 2. Preferred: package.json subpath imports (works everywhere natively)
```json
{
  "imports": {
    "#lib/*": { "types": "./src/lib/*.ts", "default": "./dist/lib/*.js" },
    "#config": "./dist/config.js"
  }
}
```
```ts
import { db } from "#lib/db";
```
Supported by Node (entries in `imports` must start with `#`) and by TypeScript under `moduleResolution` `node16`/`nodenext`/`bundler`. TypeScript 6.0 also accepts specifiers starting with `#/`.

## 3. If you use tsconfig paths
```jsonc
{
  "compilerOptions": {
    "paths": { "@/*": ["./src/*"] }      // relative to the tsconfig file; baseUrl not required since TS 4.1
  }
}
```
Then mirror it in every tool:
- Vite: `vite-tsconfig-paths` plugin or `resolve.alias`.
- Jest: `moduleNameMapper: { "^@/(.*)$": "<rootDir>/src/$1" }`.

## 4. baseUrl
`baseUrl` made every bare specifier resolvable relative to it (so `import "utils"` silently found `src/utils` instead of a package). It is deprecated in TypeScript 6.0; remove it and write explicit `paths` entries with `./` prefixes.

## 5. Monorepos: use real packages instead of aliases
Workspace packages with their own `exports` resolve through node_modules for every tool; aliases into sibling packages' `src` bypass their build and boundaries. Use TS project references for incremental type checking.

## Gotchas
- Relative paths in a base tsconfig are resolved relative to the config file they were written in (`extends` docs).
- Published libraries must not ship unresolved aliases in `.js` or `.d.ts` output; consumers cannot resolve them.

## Verify
- Run the compiled output with plain `node dist/index.js`, the test runner and the bundler build: all three resolve aliased imports without errors.

## Checked
Checked 2026-10-25 against the TypeScript-Website tsconfig reference and 4.1 and 6.0 release notes, the Node.js packages and errors docs, the Vite shared-options docs, the Jest configuration docs and the vite-tsconfig-paths README. Confirmed: `paths` does not change how tsc emits import paths; `paths` works without `baseUrl` (4.1); `baseUrl` is deprecated in 6.0 and the replacement is `./`-prefixed `paths` entries; Node `imports` entries must start with `#`, and TypeScript 6.0 adds `#/` specifiers; ERR_MODULE_NOT_FOUND exists for ES module resolution; Vite `resolve.alias`, Jest `moduleNameMapper`, the vite-tsconfig-paths plugin; relative paths in an extended config resolve against the file that holds them. Removed unconfirmed claims about Jest and Vitest `imports` support, tsx and Bun, tsc-alias, the ESLint resolver, `extends` merging of `paths` and pnpm workspace syntax.
Method: documentation only; no commands were run.

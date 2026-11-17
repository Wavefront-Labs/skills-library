---
id: computing-software.web-development.frontend-development.tsconfig-for-frontend-apps
name: tsconfig-for-frontend-apps
category: computing-software
field: web-development
product: frontend-development
tags: [tsconfig, module-resolution-bundler, isolatedmodules, verbatimmodulesyntax, typescript-config, typescript]
level: practitioner
status: verified
description: "A correct tsconfig for bundled front-end apps: moduleResolution bundler, isolatedModules, verbatimModuleSyntax, strictness flags, path aliases and type-checking in CI."
sources:
  - https://www.typescriptlang.org/tsconfig/
  - https://www.typescriptlang.org/docs/handbook/modules/reference.html#bundler
  - https://vite.dev/guide/features#typescript
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tsconfig for front-end apps

## 1. Baseline for a Vite/Next-style app
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2023", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "noEmit": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true,
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noFallthroughCasesInSwitch": true,
    "skipLibCheck": true,
    "types": ["vite/client"],
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["src"]
}
```

Checked with `tsc` 6.0.3: this config accepts `@/util.ts` through `paths` without `baseUrl`, `import { k, T }` of a type fails with `TS1484` (needs `import type`), and `const x: number = arr[0]` fails because of `noUncheckedIndexedAccess`.

## 2. Why each matters
- `moduleResolution: "bundler"`: package `exports`, extensionless imports, no `.js` suffix requirement (unlike `node16/nodenext`, which you use for code Node runs directly).
- `isolatedModules` / `verbatimModuleSyntax`: esbuild/SWC compile files one at a time; type-only imports must say `import type`, `const enum` and namespace merging break otherwise.
- `noEmit`: the bundler emits; tsc only checks.
- `noUncheckedIndexedAccess`: `arr[i]` and `record[key]` become `T | undefined`; catches real bugs.
- `types`: limit global ambient types (stops Jest and Vitest globals colliding).

## 3. Project references (Vite template layout)
`tsconfig.json` with `"references"` to `tsconfig.app.json` (browser code, DOM lib) and `tsconfig.node.json` (vite.config.ts, Node types). `tsc -b` reported a deliberate type error in `src/` through the references (a `types: ["node"]` entry fails with TS2688 until `@types/node` is installed).

## 4. Type-check in CI
Vite and Next dev servers do not fail on type errors (Next build does, unless `typescript.ignoreBuildErrors` is true (default `false`, per the Next.js docs)). Add `"typecheck": "tsc -b --noEmit"` (or `vue-tsc -b`) to CI. `vite-plugin-checker` shows errors in the dev overlay.

## 5. Path aliases
`paths` only informs the type checker; the bundler needs the same alias (`resolve.alias` or `vite-tsconfig-paths`; Next reads tsconfig paths natively). Avoid `baseUrl`: in TS 6.0.3 it errors with `TS5101: Option 'baseUrl' is deprecated and will stop functioning in TypeScript 7.0` unless `"ignoreDeprecations": "6.0"` is set.

## Verify
- [ ] `tsc -b` passes in CI; a deliberate type error fails the pipeline.
- [ ] `import type` lint rule (`@typescript-eslint/consistent-type-imports`) enabled.

---
id: computing-software.web-development.vite.typescript-compiler-options
name: typescript-compiler-options
category: computing-software
field: web-development
product: vite
tags: [tsconfig-options, isolated-modules, use-define-for-class-fields, tsconfig-paths]
level: practitioner
status: docs-checked
description: "Which tsconfig compilerOptions Vite honours: isolatedModules, useDefineForClassFields, target ignored, emitDecoratorMetadata, paths via resolve.tsconfigPaths."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/features.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vite uses the closest parent `tsconfig.json` matching each file (also configs reached via `references`, matched by `files`/`include`/`exclude`). A value in the Vite config wins over `tsconfig.json`.

- `isolatedModules`: set it to `true`. Oxc transpiles without type info, so const enum and implicit type-only imports are unsupported. If a dependency breaks, `skipLibCheck: true` suppresses errors temporarily.
- `useDefineForClassFields`: defaults to `true` for target ES2022 or newer (including ESNext), otherwise `false`. Set `false` if a library does not support it.
- `target`: ignored, as esbuild does. Use `oxc.target` in dev (default `esnext`); `build.target` takes priority in builds.
- `emitDecoratorMetadata`: only partially supported.
- `paths`: enable `resolve.tsconfigPaths: true`. It has a performance cost and the TypeScript team discourages it for external tools.
- Also affecting output: `extends`, `verbatimModuleSyntax`, `jsx`, `jsxFactory`, `jsxFragmentFactory`, `jsxImportSource`, `experimentalDecorators`, `importsNotUsedAsValues`, `preserveValueImports`.

```json
{ "compilerOptions": { "isolatedModules": true, "skipLibCheck": true } }
```

## Checked

2026-11-07. Re-read the Features guide (docs/guide/features.md) in full, TypeScript Compiler Options section. Confirmed per-file closest tsconfig matching with references, Vite config precedence, isolatedModules and skipLibCheck, the useDefineForClassFields default, target being ignored with oxc.target and build.target, partial emitDecoratorMetadata support, resolve.tsconfigPaths and its cost, and the list of other options affecting output. Nothing removed.

Method: documentation only; no commands were run.

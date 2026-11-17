---
id: computing-software.web-development.vite.typescript-transpile-only
name: typescript-transpile-only
category: computing-software
field: web-development
product: vite
tags: [typescript-support, type-checking, tsc-noemit, oxc-transformer]
level: intro
status: docs-checked
description: "Vite transpiles TypeScript with the Oxc Transformer but never type checks; run tsc --noEmit or vite-plugin-checker, and use type-only imports."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/features.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vite imports `.ts` files out of the box, transpiling per file with the Oxc Transformer. It does NOT type check: type checking needs the whole module graph and would compromise on-demand speed. Keep static analysis (including ESLint) outside the transform pipeline.

- Production: run `tsc --noEmit` in addition to `vite build`.
- Development: run `tsc --noEmit --watch` in a separate process, or use `vite-plugin-checker` to show type errors in the browser.

Use type-only syntax to avoid type imports being wrongly bundled:

```ts
import type { T } from 'only/types'
export type { T }
```

The docs state HMR updates can reflect in the browser in under 50ms.

## Checked

2026-11-07. Re-read the Features guide (docs/guide/features.md) in full, TypeScript and Transpile Only sections. Confirmed transpile-only behaviour with the Oxc Transformer, the reason type checking is not done, tsc --noEmit for builds, tsc --noEmit --watch or vite-plugin-checker in development, the type-only import syntax and the under-50ms HMR statement. Nothing removed.

Method: documentation only; no commands were run.

---
id: computing-software.devops-ci-cd.turborepo.internal-packages-just-in-time-packages
name: internal-packages-just-in-time-packages
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, just-in-time, jit-package, exports-field, typescript-paths, subpath-imports, no-build-script, bundler, turbopack]
level: practitioner
status: docs-checked
description: "Just-in-Time internal packages export TypeScript directly and rely on the consumer's bundler; know when it fits and its four tradeoffs."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/core-concepts/internal-packages.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Just-in-Time package is compiled by the application that uses it, so you can use TypeScript (or uncompiled JavaScript) directly with far less configuration.

Use it when your apps are built with a modern bundler (Turbopack, webpack, Vite), you want to avoid setup, and you are satisfied with app build times even when the package cannot hit the cache.

```json
{
  "name": "@repo/ui",
  "exports": {
    "./button": "./src/button.tsx",
    "./card": "./src/card.tsx"
  },
  "scripts": {
    "lint": "eslint . --max-warnings 0",
    "check-types": "tsc --noEmit"
  }
}
```

Two things to notice: `exports` points **directly at TypeScript files**, which works because the application's bundler compiles them; and there is **no `build` script**, so no build tool to configure.

**Tradeoffs from the docs**
1. Only applicable when consumers transpile: the consumer's bundler (or a tool natively understanding TypeScript) must do it. Otherwise move to Compiled Packages.
2. No TypeScript `paths`: a library transpiled by its consumer cannot use `compilerOptions.paths`, because TypeScript assumes code is transpiled in the package that wrote it. With TypeScript 5.4 or later, use Node.js subpath imports (see the TypeScript guide).
3. Turborepo cannot cache a build for it, since there is no `build` step.
4. Errors in internal dependencies are reported: type-checking in a dependent package fails if the dependency has TypeScript errors, which may confuse.

## Checked

2026-11-04. Read the Just-in-Time Packages section of the Internal Packages page in full: when-to-use list, the example package.json, and all four tradeoffs match. Removed the invented Verify step.

Method: documentation only; no commands were run.

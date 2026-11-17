---
id: computing-software.devops-ci-cd.turborepo.internal-packages-compiled-packages
name: internal-packages-compiled-packages
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, compiled-packages, tsc, dist-outputs, exports-types-default, outputs-key, sideeffects, build-script]
level: practitioner
status: docs-checked
description: "Compiled internal packages build with tsc to dist, export types and default separately, and let Turborepo cache the build through outputs."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/core-concepts/internal-packages.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Compiled Package handles its own compilation with a build tool such as `tsc`:

```json
{
  "name": "@repo/ui",
  "exports": {
    "./button": {
      "types": "./src/button.tsx",
      "default": "./dist/button.js"
    },
    "./card": {
      "types": "./src/card.tsx",
      "default": "./dist/card.js"
    }
  },
  "scripts": { "build": "tsc" }
}
```

Compilation writes JavaScript to a directory (`dist`, `build`, etc.) used as the package entrypoints. Turborepo caches those outputs once you list them in the task's `outputs` key, giving faster builds.

**Tradeoffs from the docs**
- **Use the TypeScript compiler.** Most Compiled Packages should use `tsc`: the application that consumes the package normally has a bundler that prepares the library for final bundles, handling polyfilling, downleveling and similar. Use a bundler in the package only for a specific need, such as bundling static assets into its outputs.
- **More configuration.** You need deeper knowledge of the many TypeScript compiler options, plus optimisation for bundlers such as the `sideEffects` key in `package.json`. The TypeScript guide has recommendations.

Compare with Just-in-Time, which needs no build script but cannot be cached.

## Checked

2026-11-04. Read the Compiled Packages section of the Internal Packages page in full: the package.json example, the outputs-key caching statement, the `tsc` recommendation and the configuration tradeoffs match. Removed the invented Verify step.

Method: documentation only; no commands were run.

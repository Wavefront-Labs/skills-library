---
id: computing-software.devops-ci-cd.turborepo.internal-packages-workspace-syntax-and-compilation-strategies
name: internal-packages-workspace-syntax-and-compilation-strategies
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, internal-packages, workspace-protocol, workspace-star, compilation-strategies, just-in-time, compiled-packages, publishable-packages, changesets]
level: practitioner
status: docs-checked
description: "Install an internal package with the workspace syntax and choose between just-in-time, compiled and publishable compilation strategies."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/core-concepts/internal-packages.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Internal Packages are libraries whose source lives in your workspace. You install them in `package.json` like an external package, but instead of a version you use the package manager's workspace syntax:

```json
{ "dependencies": { "@repo/ui": "workspace:*" } }
```

The docs show `workspace:*` for pnpm, bun, nub and aube, and `"*"` for yarn and npm. You then import it as you would any external package.

**Three compilation strategies** (more configuration as you go down):
- **Just-in-Time**: minimal configuration; the application's bundler compiles the package as it uses it.
- **Compiled**: moderate configuration; compile with a build tool such as `tsc` or a bundler.
- **Publishable**: compile and prepare for the npm registry; the most configuration. Because you do not know how consumers use the package, many configurations are needed for robustness, and publishing needs specialised tooling. The docs recommend `changesets` for versioning, changelogs and publishing, and point to the Publishing packages guide.

The Creating an Internal Package guide builds a package from scratch with the Compiled strategy.

## Checked

2026-11-04. Read the opening, Compilation Strategies and Publishable packages sections of the Internal Packages page: the workspace syntax per package manager (the page shows `workspace:*` for pnpm, bun, nub and aube, and `*` for yarn and npm), the three strategies, and the `changesets` recommendation match. Removed the invented Verify step.

Method: documentation only; no commands were run.

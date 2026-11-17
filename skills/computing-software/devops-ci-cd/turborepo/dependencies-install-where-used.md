---
id: computing-software.devops-ci-cd.turborepo.dependencies-install-where-used
name: dependencies-install-where-used
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, managing-dependencies, internal-dependencies, external-dependencies, workspace-protocol, install-where-used, root-dependencies, pnpm-filter]
level: practitioner
status: docs-checked
description: "Install each dependency in the package that uses it, for clarity, flexibility, better cache hits and pruning, using package manager multi-package commands."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/managing-dependencies.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**External dependencies** come from the npm registry; **internal dependencies** share functionality within the repo. In an app's `package.json`: `"next": "latest"` (external) and `"@repo/ui": "workspace:*"` (internal; pnpm, bun, nub and aube use `workspace:*`, yarn and npm use `"*"`).

**Best practice: install dependencies where they are used**, both external and internal, so each package's `package.json` lists everything it needs. (Your package manager may place `node_modules` elsewhere.)

Installing one tool into multiple packages:
- pnpm: `pnpm add jest --save-dev --recursive --filter=web --filter=@repo/ui --filter=docs`
- Yarn 1: `yarn workspace web add jest --dev` per package
- Yarn 2+: `yarn workspaces foreach -R --from '{web,@repo/ui}' add jest --dev`
- npm: `npm install jest --workspace=web --workspace=@repo/ui --save-dev`
- bun, nub, aube: run the add command inside each package directory.

**Benefits**
- *Clarity*: dependencies are visible in each package's `package.json`.
- *Flexibility*: at scale, packages will not all use the same version. The `ui` team can bump TypeScript while `web` ships features; versions can still be synced deliberately.
- *Better caching*: dependencies in the root change the workspace root on every add, update or delete, causing unnecessary cache misses.
- *Pruning*: for Docker, `turbo prune` can read the lockfile and remove dependencies unused by the packages you need.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/managing-dependencies); commands, flags, key names, defaults and example values were matched against it. Removed: the Verify step the page does not support.

Method: documentation only; no commands were run.

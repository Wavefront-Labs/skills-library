---
id: computing-software.devops-ci-cd.turborepo.dependencies-keep-same-version-across-packages
name: dependencies-keep-same-version-across-packages
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, dependency-versions, syncpack, manypkg, sherif, pnpm-catalogs, version-sync, monorepo-consistency]
level: practitioner
status: docs-checked
description: "Keep dependencies on one version with syncpack, manypkg or sherif, package manager recursive update commands, pnpm catalogs or an IDE regex replace."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/managing-dependencies.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Some maintainers prefer one version of each dependency across all packages. Options from the docs:

- **Purpose-built tooling**: `syncpack`, `manypkg` (`@manypkg/cli`) and `sherif`.
- **Your package manager**, updating in one command:
  - pnpm: `pnpm up --recursive typescript@latest`
  - Yarn 1: `yarn upgrade-interactive --latest`
  - Yarn 2+: `yarn upgrade typescript@latest --upgrade`
  - npm: `npm install typescript@latest --workspaces`
  - bun: `bun update typescript --latest`
  - nub: `nub update typescript --latest`
  - aube: `aube update typescript --latest`
- **pnpm catalogs** (pnpm v9.5+): define version ranges as reusable constants referenced across the workspace so versions stay aligned.
- **Your IDE**: use find and replace across all `package.json` files with a regex such as `"next": ".*"` to set the wanted version, then run your package manager's install command to update the lockfile.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/managing-dependencies); commands, flags, key names, defaults and example values were matched against it. Removed: an unsourced closing stance and the Verify step.

Method: documentation only; no commands were run.

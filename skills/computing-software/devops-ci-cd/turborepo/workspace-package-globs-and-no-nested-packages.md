---
id: computing-software.devops-ci-cd.turborepo.workspace-package-globs-and-no-nested-packages
name: workspace-package-globs-and-no-nested-packages
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, workspace-globs, pnpm-workspace, nested-packages, package-grouping, apps-glob, workspaces-field, aube-workspace]
level: practitioner
status: docs-checked
description: "Declare package directories per package manager and avoid nested packages; group by directory with extra globs and no intermediate package.json."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/structuring-a-repository.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Your package manager must describe the locations of your packages. With `apps/*` and `packages/*`, every directory **with a `package.json`** in `apps` or `packages` is a package.

How to declare it:
- **pnpm**: `pnpm-workspace.yaml` with `packages:` listing `"apps/*"` and `"packages/*"`.
- **yarn, npm, bun, nub**: a `workspaces` array in the root `package.json`: `["apps/*", "packages/*"]`.
- **aube**: `aube-workspace.yaml` with the same `packages:` list.

Each package directory needs its own `package.json` so that both your package manager and `turbo` can discover it.

**Nested packages are not supported.** Turborepo does not support globs like `apps/**` or `packages/**` because package managers in the JavaScript ecosystem behave ambiguously there. A structure that places one package at `apps/a` and another at `apps/a/b` results in an error.

**Grouping by directory.** If you want to group packages, use globs like `packages/*` and `packages/group/*` and do **not** create a `packages/group/package.json` file.

## Checked

2026-11-04. Read the "Specifying packages in a monorepo" section of the Structuring a repository page in full: the `apps/` and `packages/` recommendation, each package manager's declaration (including `aube-workspace.yaml`), the nested-package error callout and the grouping advice match. Removed an invented yaml example and the invented Verify step.

Method: documentation only; no commands were run.

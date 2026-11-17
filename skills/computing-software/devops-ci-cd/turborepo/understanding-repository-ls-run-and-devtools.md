---
id: computing-software.devops-ci-cd.turborepo.understanding-repository-ls-run-and-devtools
name: understanding-repository-ls-run-and-devtools
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, turbo-ls, turbo-devtools, list-packages, list-tasks, repository-inspection, filter-ls, package-graph-visualization]
level: practitioner
status: docs-checked
description: "Inspect a monorepo with turbo devtools (browser package graph), turbo ls (packages and paths, filterable) and turbo run without tasks (available tasks)."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/understanding-your-repository.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Turborepo ships tools to understand repository structure.

**`turbo devtools`**: a browser-based visualisation of your package graph, helpful to diagnose task graph issues and understand structure (see the devtools reference).

**`turbo ls`** lists packages and their locations, e.g. `@repo/eslint-config packages/eslint-config`, `@repo/ui packages/ui`, `docs apps/docs`, `web apps/web`. It accepts filters like `run`: `turbo ls --filter ...ui` prints `3 packages (pnpm9)` — `@repo/ui`, `docs`, `web`.

**`turbo run` with no tasks** prints "No tasks provided, here are some potential ones" with each task and the packages that define it: for example `lint` in `@repo/ui, docs, web`; `build`, `dev` and `start` in `docs, web`; `generate:component` in `@repo/ui`.

For deeper questions about dependency counts or why a package is affected, `turbo query` (GraphQL, since 2.2.0) goes further.

## Checked

2026-11-04. Read the Understanding your repository page in full: the devtools, `ls` (with `--filter ...ui` output), bare `turbo run` and `turbo query` sections match. Removed the invented Verify step and the unsupported advice paragraphs built on it.

Method: documentation only; no commands were run.

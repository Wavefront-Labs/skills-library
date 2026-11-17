---
id: computing-software.devops-ci-cd.nx.nx-inferred-tasks-precedence
name: nx-inferred-tasks-precedence
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, monorepo, inferred-tasks, project-json, package-json, includedscripts, project-details]
level: intro
status: docs-checked
description: "Where Nx tasks come from (package.json scripts, project.json, plugins), how the three sources merge, and how to inspect or limit them."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/features/run-tasks.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/project-configuration.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/getting-started/how-nx-works.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: understand and debug where a task's configuration comes from.

Three sources, lowest to highest precedence:
1. Tasks inferred by plugins registered in `nx.json` (e.g. `@nx/jest` creates `test` when it sees a Jest config).
2. `targetDefaults` in `nx.json`.
3. The project's own `package.json` or `project.json`.
Each source overwrites the previous one per property; use `"..."` to merge (nx-spread-token). `tags` and `implicitDependencies` always merge.

package.json vs project.json: equivalent. In `package.json` put Nx config under `"nx"` (`targets`, `namedInputs`, `includedScripts`); the page's `project.json` example holds `root`, `sourceRoot`, `projectType`, `tags`, `implicitDependencies`, `namedInputs`, `targets`. Nx merges the two files per project. Targets accept `command` (shell) or `executor` + `options`.

Graph membership: any `package.json` referenced by root `workspaces` (or `lerna.json`, `pnpm-workspace.yml`) is a project; to exclude one, exclude it there (e.g. `!packages/myproject`).

Limit scripts: `package.json` `scripts` all become targets unless `"nx": { "includedScripts": ["build"] }` lists the ones to expose.

Implicit dependencies: `"implicitDependencies": ["anotherlib"]`, a glob like `"shop-*"` (minimatch), or removal with `"!anotherlib"`.

Inspect: `nx show project myproject --web` (project details with the source of every setting), `nx show target myproject:build --verbose`. Nx Console shows the same view in the IDE.

Gotcha: a target default overrides a plugin's inferred inputs/outputs; write project-level overrides only for what differs. Older workspaces can move to inferred tasks with the "Migrate to Inferred Tasks" guide (nx-convert-to-inferred).

## Checked

2026-11-07. Confirmed: the three-source precedence, package.json vs project.json, workspaces membership, includedScripts, implicitDependencies and the nx show commands against Run tasks, Project configuration and How Nx works. Removed: the claim that package.json nx holds tags and implicitDependencies (page shows targets, namedInputs, includedScripts), a vague nx migrate pointer (now the Migrate to Inferred Tasks guide) and an invented Verify step.

Method: documentation only; no commands were run.

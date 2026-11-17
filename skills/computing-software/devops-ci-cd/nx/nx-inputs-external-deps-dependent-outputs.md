---
id: computing-software.devops-ci-cd.nx.nx-inputs-external-deps-dependent-outputs
name: nx-inputs-external-deps-dependent-outputs
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, monorepo, inputs, externaldependencies, dependenttasksoutputfiles, caching]
level: advanced
status: docs-checked
description: "Nx inputs for npm packages (externalDependencies) and for files produced by dependency tasks (dependentTasksOutputFiles, transitive), with pitfalls."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/inputs.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/features/CI%20Features/affected.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: tighten cache hits for tools and for artifacts of upstream tasks.

externalDependencies:
- Imports in project source are tracked automatically; you only add entries for tools that run the task.
- If a target declares no external dependency inputs, Nx hashes ALL external dependencies of the workspace (safe, but e.g. an `eslint .` target reruns when any unrelated package updates).
- Override by listing them, keeping `default`:
```jsonc
"lint": { "command": "eslint .",
  "inputs": ["default", { "externalDependencies": ["eslint", "eslint-config-airbnb"] }] }
```
- Targets using executors from Nx-team plugins already get the right set.

dependentTasksOutputFiles: hash the content of files a dependency task produced.
```jsonc
"inputs": [
  { "dependentTasksOutputFiles": "**/*.d.ts" },
  { "dependentTasksOutputFiles": "**/*.d.ts", "transitive": true }
]
```
- The glob matches paths resolved from the workspace root. With `outputs: ["{workspaceRoot}/dist/{projectRoot}"]` and root `libs/my-lib`, `dist/libs/my-lib/index.d.ts` matches `**/*.d.ts`, `dist/**/*.d.ts`, or `dist/libs/my-lib/**/*.d.ts`.
- `transitive: true` also includes outputs of all tasks those depend on in the pipeline.
- Dependency tasks can change over time; do not scope the glob too tightly or you risk false cache hits.
- `nx affected` selects a task that reads a selected task's outputs this way; declare `outputs` on the producing task or a reader of its folder is not selected (nx-affected-ci-base).

## Checked

2026-11-07. Confirmed: externalDependencies default and override example and dependentTasksOutputFiles with transitive against the Inputs reference; the affected-selection note against the Affected page (added to sources). Removed: an invented Verify step and an unsourced outputs requirement (now stated as the Affected page puts it).

Method: documentation only; no commands were run.

---
id: computing-software.software-engineering.pnpm.task-orchestration-depends-on
name: task-orchestration-depends-on
category: computing-software
field: software-engineering
product: pnpm
tags: [tasks-setting, depends-on, task-graph, task-concurrency, task-cycle, pass-through-task, task-caching]
level: advanced
status: docs-checked
description: "Declare task relationships for pnpm -r run with the tasks setting: dependsOn, the ^ prefix, default behaviour, per-task concurrency, pass-through scripts and ERR_PNPM_TASK_CYCLE."
sources:
  - https://pnpm.io/workspace-task-orchestration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```yaml
# pnpm-workspace.yaml
tasks:
  build:
    concurrency: 2
    dependsOn:
      - ^build
  test:
    dependsOn:
      - build
```

A task is `<project>#<script>`. `dependsOn` entries: `build` (same project) or `^build` (each selected workspace dependency).

Rules:
- A task with no `tasks` entry defaults to depending on the same task in its workspace dependencies (`^build` for build).
- WARNING: once a task has an entry, omitting `dependsOn` means `dependsOn: []`. Add `^build` explicitly if you also set `concurrency`.
- Dependencies stay inside the projects selected by `--filter` and `includeWorkspaceRoot`; `dependsOn` never widens it.
- A project without the script is a pass-through: reported skipped after its own dependencies, so the chain is not severed.
- `concurrency` limits instances of that task across projects, separately from `--workspace-concurrency`; waiting for a slot does not occupy a workspace slot.
- Cycles fail before any script starts with `ERR_PNPM_TASK_CYCLE`. `ignoreWorkspaceCycles: true` downgrades it to a warning and removes ordering among members.
- `outputs`, `inputs`, `env`, `cache`, `cargoTargetDir` are read by `pnpm pipeline` only; recursive `pnpm run` never restores from cache.
- `--no-sort` and `--parallel` ignore `tasks`.

## Checked

2026-11-04. Confirmed dependsOn forms, default and omitted-dependsOn behaviour, selection limits, pass-through tasks, per-task concurrency, ERR_PNPM_TASK_CYCLE, ignoreWorkspaceCycles and the caching keys against pnpm.io/workspace-task-orchestration. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.

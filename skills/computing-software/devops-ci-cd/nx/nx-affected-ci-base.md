---
id: computing-software.devops-ci-cd.nx.nx-affected-ci-base
name: nx-affected-ci-base
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, monorepo, affected, ci, nx-base, nx-head, nx-set-shas]
level: practitioner
status: docs-checked
description: "Run nx affected correctly in CI: task-based selection via inputs, --base/--head, NX_BASE/NX_HEAD, nrwl/nx-set-shas, GitLab and CircleCI setup, .nxignore."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/features/CI%20Features/affected.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/getting-started/setup-ci.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run only tasks a change reaches: `nx affected -t lint test build`.

Selection (task-based, Nx 24): Git finds changed files; each requested task whose inputs include a changed file is selected, plus tasks that read the outputs of selected tasks; then those tasks and their dependencies run (unchanged ones restore from cache). Preview with `--graph`.

Gotchas:
- `dependsOn` alone does not make a task affected; inputs/outputs do. Declare inputs and outputs even for uncached tasks: if `web:test` lists only `{projectRoot}/**/*`, `ui` source changes miss it; undeclared `dist` outputs hide `ui` build changes from `web:build`.
- Sync generators that change files mid-run do not update the selection; run `nx sync` first.

Base/head: default `base` is `main` (or `defaultBase` in `nx.json`), default `head` is the working tree. In CI:
```shell
nx affected -t build --base=origin/main --head=$PR_BRANCH_NAME
NX_BASE=origin/main~1 NX_HEAD=origin/main nx affected -t build
```
Best base: the last successful commit on `main`.
- GitHub: checkout with `fetch-depth: 0` (required), then `uses: nrwl/nx-set-shas@v5`, then `npx nx affected -t lint test build`.
- CircleCI: Nx Orb step `nx/set-shas` with `main-branch-name: 'main'`.
- GitLab: `export NX_HEAD=$CI_COMMIT_SHA; export NX_BASE=${CI_MERGE_REQUEST_DIFF_BASE_SHA:-$CI_COMMIT_BEFORE_SHA}`.

Ignoring files: globs in `.gitignore` and an optional `.nxignore` are ignored. No Git: pass `--files`.

Lockfile: a lockfile change affects every task by default (see nx-affected-explain-legacy).

Pairs best with remote cache (nx-remote-cache) and Workers (nx-distributed-workers), since repeated pushes select the same tasks.

Verify: `nx affected -t build --explain` prints why each task is selected.

## Checked

2026-11-07. Confirmed: the task-based vs legacy affected selection, the base/head behaviour and the --explain output against the Affected page. Removed: nothing; no claim failed.

Method: documentation only; no commands were run.

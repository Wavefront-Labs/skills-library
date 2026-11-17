---
id: computing-software.devops-ci-cd.nx.nx-parallelism-false
name: nx-parallelism-false
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, monorepo, parallelism, e2e, scheduling-constraints, shared-resources]
level: practitioner
status: docs-checked
description: "Stop Nx tasks that share a port or resource from running together: parallelism false, per-machine scope, scheduling-constraints on Workers."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/project-configuration.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/features/CI%20Features/distribute-task-execution.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep tasks that conflict (same port, memory hog, shared database) from overlapping.

Nx 19.5.0+: by default tasks run in parallel on a machine. Opt a target out:
```json
{ "targets": { "e2e": { "parallelism": false } } }
```
Tasks with `parallelism: false` will not run alongside other tasks on the same machine (e.g. all `e2e` tasks needing port 4200).

Scope warning: it applies per machine only. With distributed execution, different Workers share no resources, so tasks run simultaneously on different machines, which is fine and the reason to use Workers for such tasks.

Finer control on Nx Cloud Workers, in `.nx/ci-config.yaml` (preferred over lowering `--parallel`, since dynamic task packing sizes load from measured CPU/memory):
```yaml
dte:
  distribute-on: 3 linux-large-js
  scheduling-constraints:
    - targets: ['e2e*']
      cannot-run-with:
        - targets: ['e2e*']
```
Selectors must also match themselves if tasks of one group must not overlap. Constraints only prevent overlap on the same worker; a resource shared across workers needs global serialization instead. Use `parallelism: false` to give a task a worker to itself.

Migrating an old `--parallel=1` setup (the page's agent prompt): find the tasks that ran with per-worker parallelism of 1 (check `--parallel=1`, assignment-rule `parallelism: 1`, workspace defaults and target-level `parallelism: false`, including plugin-generated split e2e targets), work out why, then use a scheduling constraint for a shared port, database or output directory, keep `parallelism: false` for a task that needs a whole worker, and keep global serialization for a resource shared across workers. Old CPU and memory limits are dropped.

## Checked

2026-11-07. Confirmed: parallelism: false (Nx 19.5.0+), per-machine scope, scheduling-constraints with cannot-run-with, the self-match rule and global serialization note against Project configuration and Distribute task execution. Removed: the unconfirmed claim that --parallel is for local runs only and an invented Verify step; the migration guidance is now attributed to the page's agent prompt.

Method: documentation only; no commands were run.

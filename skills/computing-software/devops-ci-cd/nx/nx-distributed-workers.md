---
id: computing-software.devops-ci-cd.nx.nx-distributed-workers
name: nx-distributed-workers
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, nx-cloud, distributed-execution, workers, dynamic-task-packing, ci-config]
level: advanced
status: docs-checked
description: "Distribute Nx CI tasks across Nx Cloud workers: .nx/ci-config.yaml distribute-on, changesets by PR size, start-workers, dynamic task packing, scheduling constraints."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/features/CI%20Features/distribute-task-execution.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: spread the tasks of one CI run over several machines with no manual sharding.

Setup:
1. `npx nx@latest connect`, then optionally `npx nx g ci-workflow` for a starter pipeline.
2. Create `.nx/ci-config.yaml`:
```yaml
dte:
  distribute-on: 3 linux-large-js
```
`linux-large-js` is a predefined launch template. Default worker image: `ubuntu22.04-node24.14-v1`.
3. In the main CI job, start workers before installing dependencies (checkout with `fetch-depth: 0`):
```yaml
- run: pnpm dlx nx-cloud start-workers
- run: pnpm exec nx affected -t lint test build
```
`start-workers` takes no configuration flags; all config lives in `ci-config.yaml`. It replaces the older `nx-cloud start-ci-run`. Every Nx command in the job then runs across the workers; logs and outputs replay in the main job.
4. Turn on **Dynamic task packing** in Nx Cloud workspace settings (applies to pipelines started after saving). Env var `NX_CLOUD_AUTO_TASK_PACKING` on a job overrides the setting.

Dynamic packing uses the task graph and past CPU/memory profiles, so there is no `--parallel` value to tune: drop old ones. If a worker fails during setup, others take its tasks.

Scale with PR size, ordered smallest to largest (equal share of the affected-project range each; `default` is reserved for one changeset used everywhere):
```yaml
dte:
  distribute-on:
    small-changeset: 3 linux-large-js   # 1-25% of projects affected
    medium-changeset: 6 linux-large-js  # 26-50%
    large-changeset: 10 linux-large-js  # 51-75%
    extra-large-changeset: 15 linux-large-js  # 76-100%
```

Keep tasks off the same worker (shared port/db), see nx-parallelism-false:
```yaml
dte:
  scheduling-constraints:
    - targets: ['e2e*']
      cannot-run-with:
        - targets: ['e2e*']
  assignment-rules: .nx/assignment-rules.yaml
```
Use assignment rules only to route targets to larger worker types; every referenced template must exist in every `distribute-on` tier. Constraints do not serialize across workers.

Gotchas (from the page's agent prompt): a tool missing from the default base image needs a worker init step; forward only the env vars workers need with `--with-env-vars`, and avoid `--with-env-vars=auto` unless broad forwarding is accepted.

Check (page's validation list): a trial CI run shows workers start, receive tasks, restore outputs and shut down.

## Checked

2026-11-07. Confirmed: ci-config.yaml distribute-on, changeset tiers, start-workers, dynamic task packing and scheduling constraints against the Distribute task execution page. Removed: an invented Verify step; the gotchas are now attributed to the page's agent prompt.

Method: documentation only; no commands were run.

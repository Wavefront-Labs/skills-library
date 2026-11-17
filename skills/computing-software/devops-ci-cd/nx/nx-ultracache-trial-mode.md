---
id: computing-software.devops-ci-cd.nx.nx-ultracache-trial-mode
name: nx-ultracache-trial-mode
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, nx-cloud, ultracache, nx-cloud-ultracache-mode, ci, trial]
level: practitioner
status: docs-checked
description: "Turn on or trial Nx Cloud Ultracache: workspace setting, NX_CLOUD_ULTRACACHE_MODE values and precedence, NX_CLOUD_USE_ULTRACACHE, what gets traced."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/features/CI%20Features/remote-cache.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/features/cache-task-results.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: enable Ultracache (hash tasks from files actually read) and trial it on one pipeline.

How it works: the first time a task runs on Workers, Nx hashes it from declared `inputs` and records the files read. Later CI runs hash from that recording (it grows if the task reads new files). The recording lives in Nx Cloud; your config files do not change and declared `outputs` still decide what is cached. Only Workers runs are recorded, but every CI run hashes from the recording; runs outside CI use declared inputs. Cache hits, continuous tasks, `cache: false` tasks and batch-executor tasks are not traced.

Enable: new Nx Cloud workspaces start with it on. Existing: Nx Cloud workspace Settings, set Ultracache to On. Requires Nx 24.0.0+ (uses it in CI by default); Nx 23 differs. Included in every Nx Cloud plan; traced tasks do not use credits.

Skip for one run: `NX_CLOUD_USE_ULTRACACHE=false`.

Trial one workflow/branch with `NX_CLOUD_ULTRACACHE_MODE` (case-insensitive; overrides the workspace setting for that pipeline only, no Nx 24 upgrade needed):
- `ON`: on; targets keep their own `mode`, others use `on`.
- `WARN` / `ERROR`: apply that mode to every task, overriding target modes.
- `OFF`: off for every task.
- unset: workspace setting. Any other value fails the run.
It beats `NX_CLOUD_USE_ULTRACACHE`: with `OFF`/`WARN`/`ERROR` recorded inputs are not used even if that is `true`. Do not combine `ON` with `NX_CLOUD_USE_ULTRACACHE=false` (Nx 24+ still skips it).

Set it at job/workflow level so both `npx nx-cloud start-workers` and Nx commands see it:
```yaml
env:
  NX_CLOUD_ULTRACACHE_MODE: 'ON'
```
It does not change which tasks `nx affected` selects, and does not alter the saved workspace setting.

Per-target opt-out: `"ultracache": { "mode": "off" }` (nx-ultracache-target-config).

Traced reads and writes appear in Nx Cloud under Analytics > Cache inputs and outputs.

## Checked

2026-11-07. Confirmed against Remote caching (Ultracache sections) and Cache Task Results: how it works (first Workers run hashes declared inputs and records reads, recording grows, stored in Nx Cloud, outputs unchanged), what is not traced, every Nx Cloud plan with no credits for traced tasks, new workspaces on, the Settings toggle, Nx 24.0.0 requirement, NX_CLOUD_USE_ULTRACACHE, the NX_CLOUD_ULTRACACHE_MODE value table, precedence over NX_CLOUD_USE_ULTRACACHE, the ON plus false caution, invalid values failing the run, job-level env placement, no change to affected selection or the saved workspace setting, and the per-target off setting. Removed: the Verify step as an instruction; kept as a statement drawn from the page.

Method: documentation only; no commands were run.

---
id: computing-software.devops-ci-cd.nx.nx-enable-caching
name: nx-enable-caching
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, monorepo, caching, cache, targetdefaults, inputs, outputs]
level: intro
status: docs-checked
description: "Turn on Nx computation caching with cache:true, what goes into the task hash, what an entry stores, and the side-effect-free rule."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/features/cache-task-results.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/project-configuration.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/nx-json.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/features/run-tasks.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make tasks cacheable and know what the cache keys on.

Enable per target name in `nx.json`:
```json
{ "targetDefaults": { "build": { "cache": true }, "test": { "cache": true } } }
```
Or `"cache": true` on a target in `project.json` / `package.json` `nx.targets`. Nx plugins infer `inputs` and `outputs` from tool config such as `vite.config.ts`, so you need not redefine them.

Task hash covers: project source files and files of dependencies, relevant workspace configuration, versions of external dependencies, runtime values (OS, CPU architecture), and command-line arguments. Nx hashes each task in the graph separately, so some tasks hit and others run.

Lookup order: local cache, then remote cache if configured (nx-remote-cache). Hit: Nx restores the stored terminal output and the output files. Miss: runs the task, stores the result locally (and remotely if permitted).

A cache entry holds stdout/stderr, files matched by the target's `outputs`, and the hash. Source files are not stored, only hashed.

Rules and gotchas:
- Only cache operations that are side-effect free: same inputs must give same outputs. An e2e run that hits a live backend must not be cached.
- Tune what is hashed or stored with `inputs` and `outputs` (nx-inputs-filesets, nx-outputs-globs). Example: `"inputs": ["{projectRoot}/**/*", "!{projectRoot}/**/*.md"]`, `"outputs": ["{workspaceRoot}/dist/{projectName}"]`.
- If you disable caching on a target while using distributed execution (Workers), that target and anything depending on it fails the pipeline (nx-distributed-workers).
- A target cannot be both cacheable and continuous.

For unexpected misses, the page points to its "Debug cache misses" guide (see nx-troubleshoot-cache-misses).

## Checked

2026-11-07. Confirmed: cache: true, hash contents, lookup order, entry contents and the side-effect-free rule against Cache task results; Workers and cacheable-vs-continuous against Project configuration and nx.json (added to sources); plugin-inferred inputs and outputs against Run tasks (added to sources). Removed: the unconfirmed "plugin-inferred tasks usually come already cached" claim and an invented run-twice Verify step.

Method: documentation only; no commands were run.

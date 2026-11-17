---
id: computing-software.devops-ci-cd.nx.nx-outputs-globs
name: nx-outputs-globs
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, monorepo, outputs, caching, glob, build-artifacts]
level: practitioner
status: docs-checked
description: "Declare Nx target outputs so cache hits restore the right files: tokens, default build locations, shared directories, glob and exclusion patterns."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/project-configuration.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/features/cache-task-results.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/kb/configure-outputs.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/nx-json.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/features/CI%20Features/affected.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/features/run-tasks.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: tell Nx which files a target creates so a cache hit restores them.

```json
{ "targets": { "build": {
  "outputs": ["{workspaceRoot}/dist/libs/mylib", "{workspaceRoot}/build/libs/mylib/main.js"] } } }
```
Tokens: `{workspaceRoot}`, `{projectRoot}`, `{projectName}`, and `{options.outputPath}` (used in an executor target, `"outputs": ["{options.outputPath}"]`).

Defaults: usually unnecessary, because the workspace presets cover these build locations: `{workspaceRoot}/dist/{projectRoot}`, `{projectRoot}/build`, `{projectRoot}/dist`, `{projectRoot}/public`. Plugin-inferred tasks take outputs from tool config (a `vite.config.ts` defines where the build output goes).

Prefer one directory per target. When targets must share a directory, use globs (GlobSet syntax from the Rust `globset` crate):
```json
"build-js":  { "outputs": ["{workspaceRoot}/dist/libs/mylib/**/*.{js,map}"] },
"build-css": { "outputs": ["{workspaceRoot}/dist/libs/mylib/**/*.css"] }
```
Exclusions in one pattern: `{workspaceRoot}/dist/libs/!(cache|.next)/**/*.{js,map}` and `{workspaceRoot}/dist/libs/mylib/**/!(secondary).css`.

Set globally via `targetDefaults`: `"build": { "outputs": ["{projectRoot}/custom-dist"] }`. An `outputs` value in a target default replaces what a plugin inferred; use `"..."` to extend (nx-spread-token).

Gotchas:
- Declare outputs even for tasks you do not cache: `nx affected` uses them to select downstream tasks that read the folder (nx-affected-ci-base).
- A cache entry stores only stdout/stderr, outputs and the hash.

## Checked

2026-11-07. Confirmed: output tokens, default build locations, GlobSet patterns, exclusion patterns and targetDefaults against Project configuration, Configure outputs and nx.json; declaring outputs for affected against the Affected page; Vite outputs against Run tasks (latter three added to sources). Removed: an invented Verify step.

Method: documentation only; no commands were run.

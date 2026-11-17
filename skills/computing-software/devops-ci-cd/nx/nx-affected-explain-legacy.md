---
id: computing-software.devops-ci-cd.nx.nx-affected-explain-legacy
name: nx-affected-explain-legacy
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, monorepo, affected, explain, legacy, nx-legacy-affected, lockfile]
level: advanced
status: docs-checked
description: "Debug nx affected: --explain output modes, affected.legacy and NX_LEGACY_AFFECTED, projectsAffectedByDependencyUpdates for lock file changes."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/features/CI%20Features/affected.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/nx-json.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/inputs.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: find out why tasks are affected, switch between task-based and project-based selection, and narrow lock-file effects.

Explain: `nx affected -t build --explain` prints reasons and exits without running anything. Output: "2 out of 2 build tasks are affected", then each changed file with the tasks it touches; add `--verbose` to list reasons per task.
- Needs targets via `-t`; without them, or with `affected.legacy` set, it errors.
- `--explain=stdout` emits JSON; `--explain=reasons.json` writes a file. Also works for `nx show projects --affected -t build --explain`.

Legacy (project-based) mode: Nx 23 and earlier ran every task of every changed project and its dependents. `nx migrate` to Nx 24 keeps that by writing `"affected": { "legacy": true }` into `nx.json`; remove it or set `false` for task-based. Env `NX_LEGACY_AFFECTED` (`true`/`false`) overrides per invocation; set it for the whole CI job so `nx show projects --affected -t test` and `nx affected -t test` agree. It applies to `nx affected -t` and `nx show projects --affected -t`. `nx graph --affected` always shows projects. In legacy mode `"inputs": false` on a `dependsOn` entry is ignored.

Lock files: by default a package manager lock file change affects every task. Narrow it via `pluginsConfig`:
```json
{ "pluginsConfig": { "@nx/js": { "projectsAffectedByDependencyUpdates": "auto" } } }
```
Values: `"all"` (default), `"auto"` (Nx diffs resolved packages between revisions; supports `pnpm-lock.yaml`/`.yml`, `package-lock.json`, `yarn.lock`, `bun.lock`, `bun.lockb`; binary Bun lock files need Bun installed where `nx affected` runs), or a `string[]` of project names/globs such as `["app-*", "shared-lib"]`.

## Checked

2026-11-07. Confirmed: the affected.legacy behaviour and the nx.json affected settings against the Affected page and nx.json reference; the "inputs": false note against the Inputs reference (added to sources). Removed: an invented Verify step.

Method: documentation only; no commands were run.

---
id: computing-software.devops-ci-cd.turborepo.turbo-json-task-tags-extends-and-description
name: turbo-json-task-tags-extends-and-description
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, task-tags, task-extends, extends-false, turbo-extends, task-description, package-configurations, inheritance]
level: advanced
status: docs-checked
description: "Task tags, the task-level extends false opt-out, and description fields; how arrays inherit, replace, or append with the $TURBO_EXTENDS$ marker."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/reference/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Task `tags`** are arbitrary string labels on a task in the root `turbo.json` or a Package Configuration, e.g. `"tags": ["ci", "slow"]`. Order and duplicates are preserved. They do not change dependencies, commands or boundary rules.

Inheritance in a Package Configuration:
- Omitting `tags` inherits them.
- An explicit array replaces inherited tags; `"tags": []` clears them.
- `$TURBO_EXTENDS$` appends: `"tags": ["$TURBO_EXTENDS$", "frontend"]` over inherited `["ci", "slow"]` resolves to `["ci", "slow", "frontend"]` (the marker is removed).
- A task with `"extends": false` starts fresh. Clearing task tags does not remove package tags.
Tags are not in the resolved task hash data, but changing tags in a package's `turbo.json` can still invalidate the cache when that file is in the task's file inputs.

**Task-level `extends`** (Package Configurations only, not the root): `false` excludes the task from inheritance. With no other config the task does not exist for the package; with other config it creates a fresh definition without inheritance. `true` (default) inherits normally. Example in `packages/ui/turbo.json`: `{ "extends": ["//"], "tasks": { "lint": { "extends": false } } }`.

**`description`**: a human- or agent-readable description of a task, for documentation only; it does not affect execution or caching.

## Checked

2026-11-04. Read the Task tags, task-level `extends`, `description` and `$TURBO_EXTENDS$` entries of the configuration reference in full; inheritance rules, the example and the hash note match. Removed the invented Verify step.

Method: documentation only; no commands were run.

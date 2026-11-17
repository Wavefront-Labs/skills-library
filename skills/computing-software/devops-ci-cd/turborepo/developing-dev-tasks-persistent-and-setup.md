---
id: computing-software.devops-ci-cd.turborepo.developing-dev-tasks-persistent-and-setup
name: developing-dev-tasks-persistent-and-setup
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, dev-task, persistent, cache-false, long-running-tasks, setup-tasks, dependson, filter-dev]
level: practitioner
status: docs-checked
description: "Register dev tasks with cache false and persistent true, run setup scripts first via dependsOn, and scope dev to one app with --filter."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/developing-applications.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Developing in a monorepo gives atomic commits and easy access to code. Most development tasks are long-running watchers. Registering a `dev` task in `turbo.json` tells Turborepo it is long-lived:

```json
{ "tasks": { "dev": { "cache": false, "persistent": true } } }
```

- `"cache": false` stops Turborepo caching the results; you are changing code frequently so caching is not useful.
- `"persistent": true` keeps the task running until you stop it. It signals to the terminal UI that the task is long-running and interactive, and prevents you from accidentally depending on a task that never exits.

Start dev scripts in parallel with `turbo dev`.

**Setup tasks before `dev`.** Use `dependsOn` to run codegen or pre-builds first:

```json
{
  "tasks": {
    "dev": { "cache": false, "persistent": true, "dependsOn": ["//#dev:setup"] },
    "//#dev:setup": { "outputs": [".codegen/**"] }
  }
}
```

This uses a Root Task, but you can do the same with arbitrary package tasks.

**Run one application** and its dependencies: `turbo dev --filter=web`.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/developing-applications); commands, flags, key names, defaults and example values were matched against it. Removed: the Verify step the page does not support.

Method: documentation only; no commands were run.

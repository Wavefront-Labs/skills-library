---
id: computing-software.devops-ci-cd.turborepo.configuring-tasks-defining-and-parallelism
name: configuring-tasks-defining-and-parallelism
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, tasks, turbo-json, tasks-key, turbo-run, parallelization, package-scripts, task-definition]
level: intro
status: docs-checked
description: "Each key in turbo.json tasks maps to package.json scripts of the same name; Turborepo parallelises everything it can, and an empty task definition is a trap."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/configuring-tasks.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A task is a script Turborepo runs. Relationships between tasks are expressed in the root `turbo.json` and the Package Graph. Turborepo always parallelises any work it can, which beats chaining `yarn workspaces run lint && yarn workspaces run build && yarn workspaces run test` sequentially; `turbo run lint build test` runs them with much less idle time.

**Defining tasks.** Each key in the `tasks` object is a task that `turbo run` can execute. Turborepo searches your packages for **scripts in their `package.json` with the same name as the task**.

The docs flag this as incorrect:

```json
{ "tasks": { "build": {} } }
```

With it, `turbo run build` runs all `build` scripts in your packages in parallel and caches no file outputs, which quickly leads to errors. You are missing task ordering (`dependsOn`) and `outputs`.

Getting started: with a new repo use `create-turbo` and edit its `turbo.json`; when adopting in an existing repo, create `turbo.json` in the repository root and run tasks with `turbo run`.

Next: add `dependsOn` for order and `outputs` for caching in the skills that follow.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/configuring-tasks); commands, flags, key names, defaults and example values were matched against it. Removed: the Verify step the page does not support.

Method: documentation only; no commands were run.

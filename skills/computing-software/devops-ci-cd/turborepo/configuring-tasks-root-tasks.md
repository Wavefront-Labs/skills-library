---
id: computing-software.devops-ci-cd.turborepo.configuring-tasks-root-tasks
name: configuring-tasks-root-tasks
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, root-tasks, root-hash-syntax, workspace-root-scripts, incremental-migration, lint-root, migration]
level: practitioner
status: docs-checked
description: "Register workspace-root scripts as //#task entries in turbo.json to cache and parallelise them, and know when root tasks are appropriate."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/configuring-tasks.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
You can run scripts from the workspace root `package.json` with `turbo`. Register them in `turbo.json` using the `//#` prefix. Example: a `lint:root` task for files in the workspace root in addition to per-package `lint`:

```json
// turbo.json
{ "tasks": { "lint": { "dependsOn": ["^lint"] }, "//#lint:root": {} } }
// package.json
{ "scripts": { "lint": "turbo run lint lint:root", "lint:root": "eslint ." } }
```

After registering, run `turbo run lint:root` from the root or `turbo run //#lint:root` from any workspace. `turbo run lint lint:root` runs all your linting tasks together.

**When to use Root Tasks** (from the docs):
- **Linting and formatting the workspace root**: running ESLint or Prettier on root-level code.
- **Incremental migration**: scripts you have not yet moved to packages can become Root Tasks, fanning them out to packages later.
- **Scripts without a package scope**: scripts that do not make sense in one package still get caching, parallelisation and workflow benefits.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/configuring-tasks); commands, flags, key names, defaults and example values were matched against it. Removed: the Verify step the page does not support.

Method: documentation only; no commands were run.

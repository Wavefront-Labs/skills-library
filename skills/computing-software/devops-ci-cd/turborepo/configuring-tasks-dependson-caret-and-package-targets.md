---
id: computing-software.devops-ci-cd.turborepo.configuring-tasks-dependson-caret-and-package-targets
name: configuring-tasks-dependson-caret-and-package-targets
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, dependson, caret-microsyntax, topological-dependencies, package-task-syntax, same-package-dependency, empty-dependson, task-ordering]
level: practitioner
status: docs-checked
description: "The four dependsOn forms: ^task for dependencies, plain task for the same package, pkg#task for a specific package, and empty for none."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/configuring-tasks.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`dependsOn` lists tasks that must complete before a task begins.

**`^build`** runs the task in direct dependencies before the target package. If an app depends on a `ui` library with a `build` task, `ui`'s build runs first, and once it succeeds the app's build runs. This ensures the app has everything needed to compile; it applies as the graph grows across many levels.

```json
{ "tasks": { "build": { "dependsOn": ["^build"] } } }
```

**Same package, plain string.** To run a library's `build` before its own `test`:

```json
{ "tasks": { "test": { "dependsOn": ["build"] } } }
```

**A specific task in a specific package.** `utils#build` must run before any `lint`:

```json
{ "tasks": { "lint": { "dependsOn": ["utils#build"] } } }
```

You can limit the dependent task to one package as well: `"web#lint": { "dependsOn": ["utils#build"] }` means the `web` package's `lint` runs only after the `build` task in `utils` completes.

**No dependencies.** For tasks that do not care about others (the docs' example is a `spell-check` for Markdown), omit `dependsOn` or use an empty array `[]`.

Warning from the docs: ordering alone does not mark outputs for caching; see the outputs skill.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/configuring-tasks); commands, flags, key names, defaults and example values were matched against it. Removed: the Verify step the page does not support.

Method: documentation only; no commands were run.

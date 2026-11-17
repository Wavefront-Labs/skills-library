---
id: computing-software.devops-ci-cd.turborepo.turbo-watch-dependency-aware-mode-and-teardown
name: turbo-watch-dependency-aware-mode-and-teardown
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, turbo-watch, watch-mode, dependency-aware-watcher, persistent-tasks, teardown, dev-teardown, tsc-watch]
level: practitioner
status: docs-checked
description: "turbo watch adds a Task-Graph-aware watcher to tools with no watcher, re-running dependents; teardown scripts cannot run on exit."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/developing-applications.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Many tools have a built-in watcher (like `tsc --watch`); some do not. `turbo watch` adds a **dependency-aware watcher to any tool**: source changes follow the Task Graph in `turbo.json` like your other tasks.

Example with `create-turbo`-style packages. Tasks: `dev` (`persistent: true`, `cache: false`) and `lint` (`dependsOn: ["^lint"]`). `@repo/ui` has `dev: tsc --watch` and `lint: eslint .`; `web` has `dev: next dev`, `lint: eslint .` and depends on `@repo/ui` as `workspace:*`.

Running `turbo watch dev lint` re-runs the `lint` scripts whenever source changes, despite ESLint having no watcher. Because `turbo watch` knows internal dependencies, a code change in `@repo/ui` re-runs the task in both `@repo/ui` and `web`. The Next.js dev server and the TypeScript compiler's watcher keep working normally because they are `persistent`.

See the `turbo watch` reference for the full details.

**Limitation: teardown.** If you want a script to run when `dev` stops, Turborepo cannot run it on exit because `turbo` exits when your dev tasks exit. Instead create a `turbo dev:teardown` script and run it separately after exiting `turbo dev`.

## Checked

2026-11-04. Read the Watch Mode and Teardown tasks sections of the Developing applications page in full; the example, the dependency-aware re-run and the teardown workaround match. Removed the invented Verify step.

Method: documentation only; no commands were run.

---
id: computing-software.devops-ci-cd.turborepo.running-tasks-root-scripts-and-global-turbo
name: running-tasks-root-scripts-and-global-turbo
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, running-tasks, turbo-run, root-scripts, global-turbo, package-scoping, recursive-turbo, one-off-commands]
level: intro
status: docs-checked
description: "Put turbo run commands in the root package.json only, use global turbo for on-demand runs, and let Automatic Package Scoping pick the package."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/running-tasks.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Once tasks are registered in `turbo.json`, three ways to run them: `scripts` in the root `package.json`, global `turbo`, and filters.

**Root scripts** for tasks you run often:

```json
{ "scripts": { "dev": "turbo run dev", "build": "turbo run build", "test": "turbo run test", "lint": "turbo run lint" } }
```

Run them with your package manager (`pnpm dev`, `yarn dev`, `npm run dev`, `bun run dev`, `nub run dev`, `aube run dev`). `turbo` is an alias for `turbo run`, but the docs recommend writing `turbo run` in `package.json` and CI to avoid collisions with subcommands that might be added in future.

**Warning:** write `turbo` commands only in the root `package.json`. Putting them in a package's `package.json` can lead to calling `turbo` recursively.

**Global turbo** makes it easy to run exactly what you need locally, and in CI gives the most control over which tasks run at each point.

**Automatic Package Scoping.** Inside a package directory, `turbo` scopes commands to the Package Graph of that package, so no filter is needed:

```bash
cd apps/docs
turbo build
```

This runs the `build` task for `docs`, using the definition in `turbo.json`. Using a filter overrides Automatic Package Scoping.

**Customising behaviour with global turbo:** variations of common commands (`turbo build --filter=@repo/ui`), one-off commands (`turbo build --dry`), and overriding `turbo.json` settings with an equivalent flag (`turbo lint --output-logs=errors-only` even if `outputLogs` is `full`).

## Checked

2026-11-04. Read the Running tasks page in full: root scripts example, the `turbo` alias recommendation, the recursion warning, global turbo, Automatic Package Scoping and the customising examples match. Removed the invented Verify step.

Method: documentation only; no commands were run.

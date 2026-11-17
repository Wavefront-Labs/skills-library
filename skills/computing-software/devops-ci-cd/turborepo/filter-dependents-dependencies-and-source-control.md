---
id: computing-software.devops-ci-cd.turborepo.filter-dependents-dependencies-and-source-control
name: filter-dependents-dependencies-and-source-control
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, filter, dependents, dependencies, git-filter, changed-packages, ellipsis-syntax, source-control-filter]
level: practitioner
status: docs-checked
description: "Use ...pkg for a package and its dependents, pkg... for it and its dependencies, and [ref] filters for packages changed in source control."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/running-tasks.mdx
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/understanding-your-repository.mdx
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/reference/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Include dependents.** When changing a package and wanting to be sure its dependents still work, prefix with `...`:

```bash
turbo build --filter=...ui
```

**Include dependencies.** Append `...` to run a package plus everything it depends on:

```bash
turbo dev --filter=web...
```

**Source control changes.** These filters run tasks only for packages affected by your changes. They **must be wrapped in `[]`**:
- Previous commit: `turbo build --filter=[HEAD^1]`
- Main branch: `turbo build --filter=[main...my-feature]`
- Specific SHAs: `turbo build --filter=[a1b2c3d...e4f5g6h]`
- Branch names: `turbo build --filter=[your-feature...my-feature]`

The docs note that you can usually rely on caching to stay fast; with Remote Caching, unchanged packages hit cache.

**Combining filters.** Multiple filters are a **union** of entry points into the Task Graph (tasks matching any filter are included):

```bash
turbo build --filter=...ui --filter={./packages/*} --filter=[HEAD^1]
```

Extra detail: `turbo ls --filter ...ui` is a quick preview of what a dependents filter selects: in the docs' example it prints 3 packages (`@repo/ui`, `docs`, `web`). The `filterUsingTasks` future flag changes resolution from the Package Graph to the Task Graph: git-range filters then match changed files against each task's `inputs`, and `...` follows task-level dependencies such as `web#build -> schema#gen`. In CI, `--affected` handles shallow clones more gracefully than bespoke filtering because it falls back to running all tasks (constructing-ci page).

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/running-tasks, crafting-your-repository/understanding-your-repository, reference/configuration); commands, flags, key names, defaults and example values were matched against it. Removed: the Verify step and the unsourced claim that --affected is simpler.

Method: documentation only; no commands were run.

---
id: computing-software.devops-ci-cd.turborepo.filter-by-package-directory-and-task-target
name: filter-by-package-directory-and-task-target
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, filter, package-filter, directory-filter, package-task-target, run-subset, glob-filter]
level: practitioner
status: docs-checked
description: "Limit a run with --filter by package name or directory glob, or name package#task targets directly from Turborepo 2.2.4."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/running-tasks.mdx
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/understanding-your-repository.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Filtering lets you run only a subset of the Task Graph. Caching keeps you fast by never repeating work; filters narrow which tasks are entry points.

**By package:**

```bash
turbo build --filter=@acme/web
```

**Task targets without `--filter`** (from Turborepo 2.2.4):

```bash
turbo run web#build            # build task for the web package
turbo run web#build docs#lint  # build for web, lint for docs
```

**By directory.** When related packages are grouped, capture the glob for that directory:

```bash
turbo lint --filter="./packages/utilities/*"
```

The docs point to the `--filter` reference for more advanced use cases.

Using a filter overrides Automatic Package Scoping, which otherwise scopes commands to the package whose directory you are in. Filters work the same in CI, where package, directory and Git history filters are all supported (Git history filters need history, so not with shallow clones). `turbo ls` accepts filters just like `run`: `turbo ls --filter ...ui` lists `@repo/ui`, `docs` and `web` in the docs' example (understanding-your-repository page). Multiple `--filter` flags combine as a union of entry points into the Task Graph.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/running-tasks, crafting-your-repository/understanding-your-repository); commands, flags, key names, defaults and example values were matched against it. Removed: the unsourced shell-quoting advice and the Verify step.

Method: documentation only; no commands were run.

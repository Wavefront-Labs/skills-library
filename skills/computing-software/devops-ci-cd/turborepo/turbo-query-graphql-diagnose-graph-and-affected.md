---
id: computing-software.devops-ci-cd.turborepo.turbo-query-graphql-diagnose-graph-and-affected
name: turbo-query-graphql-diagnose-graph-and-affected
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, turbo-query, graphql, direct-dependent-count, affected-packages, cache-miss-diagnosis, package-graph-analysis, filter-has-task]
level: advanced
status: docs-checked
description: "Use turbo query (GraphQL, since 2.2.0) to find packages with a task, over-imported packages causing cache misses, and the reason packages are affected."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/understanding-your-repository.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Since `2.2.0`, `turbo query` offers a GraphQL interface to your repository structure.

**Packages that have a task:**

```bash
turbo query "query { packages(filter: { has: { field: TASK_NAME, value: \"build\"}}) { items { name } } }"
```

The docs' output lists `//` (the root), `docs` and `web`.

**Diagnose frequent cache misses.** A package that keeps changing and is imported throughout the codebase invalidates many dependents. Find packages directly imported more than 10 times:

```bash
turbo query "query { packages(filter: { greaterThan: { field: DIRECT_DEPENDENT_COUNT, value: 10 } }) { items { name } } }"
```

The example returns `utils`. The docs suggest splitting such a package into smaller ones so a small change does not invalidate the whole graph.

**Why too many tasks with `--affected`?** Query affected packages and their reasons:

```bash
turbo query "query { affectedPackages(base: \"HEAD^\", head: \"HEAD\") { items { reason { __typename } } } }"
```

Reasons shown include `FileChanged` (for `utils`) and `DependencyChanged` (for `web`, `docs`, `cli`).

## Checked

2026-11-04. Read the `turbo query` section of the Understanding your repository page in full: the `2.2.0` note, all three queries, and the sample outputs and reasons match. Removed the invented Verify step.

Method: documentation only; no commands were run.

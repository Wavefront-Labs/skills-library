---
id: computing-software.devops-ci-cd.turborepo.task-graph-transit-nodes-and-entry-point-surprises
name: task-graph-transit-nodes-and-entry-point-surprises
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, transit-nodes, task-graph, dependson, caret-test, package-without-script, graph-semantics]
level: advanced
status: docs-checked
description: "Why a package without a script still appears in the task graph as a Transit Node, and how that includes unexpected tasks such as ^test under build."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/core-concepts/package-and-task-graph.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Transit Node.** Suppose `docs` depends on `ui`, which depends on `core`. `docs` and `core` have a `build` task, `ui` does not, and `build` has `"dependsOn": ["^build"]`. `turbo run build` builds this graph:
- `docs` only depends on `ui`.
- `ui` has no `build` script.
- `ui`'s dependencies do have `build`, so the graph includes them.

Turborepo calls `ui` a Transit Node: it executes nothing for it, but it stays in the graph so its own dependencies are included.

**Transit Nodes as entry points.** If `docs` did not implement `build` either, should `ui` and `core` still build? Turborepo's mental model is that **all nodes in the Task Graph are the same**, so Transit Nodes are included regardless of where they appear.

That can surprise you. With:

```json
{ "tasks": { "build": { "dependsOn": ["^test"] } } }
```

in a monorepo where all packages have `test` and only one app has `build`, `turbo run build` still brings the `test` tasks of all packages that are dependencies into the graph, even for an app that does not implement `build`.

## Checked

2026-11-04. Read the Transit Nodes and Transit Nodes as entry points sections of the Package and Task Graphs page in full; both scenarios match. Removed the invented Verify step.

Method: documentation only; no commands were run.

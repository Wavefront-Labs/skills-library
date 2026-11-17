---
id: computing-software.devops-ci-cd.turborepo.package-graph-and-task-graph-dag
name: package-graph-and-task-graph-dag
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, package-graph, task-graph, dag, dependson, caret-build, graph-flag, nodes-edges, package-manager-workspaces]
level: practitioner
status: docs-checked
description: "How Turborepo derives the Package Graph from installed internal packages and builds a task DAG from turbo.json dependsOn relationships."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/core-concepts/package-and-task-graph.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Package Graph.** The structure of your monorepo created by your package manager. When internal packages are installed into each other, Turborepo identifies those dependency relationships to understand the workspace.

**Task Graph.** In `turbo.json` you express how tasks relate to each other. Turborepo models this as a directed acyclic graph (DAG): nodes are tasks, edges are dependencies between tasks, and a directed edge from Task A to Task B means A depends on B.

Example: `apps/web` depends on `@repo/ui` and `@repo/utils`, and `turbo.json` says:

```json
{ "tasks": { "build": { "dependsOn": ["^build"] } } }
```

The graph has `apps/web#build` pointing at the `build` tasks of `packages/ui` and `packages/utils`, so those run first.

**Visualise it** with `turbo run build --graph`. Per the run reference, default `dot`; it can output `svg`, `html`, `mermaid` or `dot`, and with no file name prints the dot graph to stdout (for example `--graph=my-graph.svg`). The `.png`, `.jpg`, `.pdf` and `.json` formats are deprecated and will be removed in 3.0; use `turbo query` for programmatic access. Known bug per the docs: the graph may include task nodes for scripts a package does not have, overstating the packages and tasks involved, with no effect on execution.

Traversal order from the configuration reference: with `dependsOn: ["^build"]`, `turbo` starts at the "bottom" of the package graph and recursively visits each package until it finds one with no internal dependencies. It runs the `build` task at the end of the dependency chain first, then works back to the "top" until all `build` tasks are complete in order.

## Checked

2026-11-04. Read the Package and Task Graphs page in full, the `dependsOn` `^` section of the configuration reference, and `--graph` in the run reference. Removed the invented Verify step and the unsupported closing claim about installing packages where they are used.

Method: documentation only; no commands were run.

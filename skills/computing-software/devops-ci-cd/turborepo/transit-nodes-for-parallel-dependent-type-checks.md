---
id: computing-software.devops-ci-cd.turborepo.transit-nodes-for-parallel-dependent-type-checks
name: transit-nodes-for-parallel-dependent-type-checks
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, transit-nodes, check-types, parallel-tasks, cache-correctness, dependson, type-checking, task-graph]
level: advanced
status: docs-checked
description: "Make type checking both parallel and correct by declaring a no-op transit task so dependents rehash when their dependencies change."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/configuring-tasks.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Some tasks, such as type checkers, can run in parallel despite depending on other packages because they do not need dependency outputs. The tempting definition is wrong:

```json
{ "tasks": { "check-types": {} } }
```

It runs in parallel but ignores source changes in dependencies. You can break the interface of `ui`, run `turbo check-types`, and hit cache in an app that depends on `ui`: a false success.

Adding `"dependsOn": ["^check-types"]` fixes caching correctness but tasks are no longer in parallel.

To get both, introduce **Transit Nodes** into the Task Graph:

```json
{
  "tasks": {
    "transit": { "dependsOn": ["^transit"] },
    "check-types": { "dependsOn": ["transit"] }
  }
}
```

`transit` matches no script in any `package.json`, so it does nothing but create a relationship between package dependencies. Tasks run in parallel **and** are aware of changes to their internal dependencies. The name `transit` is arbitrary; use anything not already a script in the workspace.

## Checked

2026-11-04. Read the type-checking Transit Nodes section of the Configuring tasks page in full: the incorrect definition, the `^check-types` version, the `transit` pair and the naming note match. Removed the invented Verify step.

Method: documentation only; no commands were run.

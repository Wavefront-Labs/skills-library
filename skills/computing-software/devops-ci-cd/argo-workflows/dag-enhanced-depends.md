---
id: computing-software.devops-ci-cd.argo-workflows.dag-enhanced-depends
name: dag-enhanced-depends
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [enhanced-depends, dag-depends, task-results, depends-logic, any-succeeded]
level: advanced
status: docs-checked
description: "Use the DAG depends field with task results such as Succeeded, Failed and Daemoned plus boolean operators, and know how it differs from dependencies and continueOn."
sources: ["https://argo-workflows.readthedocs.io/en/latest/enhanced-depends-logic/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enhanced depends logic
`depends` lets a DAG task name which result of another task it needs. Operands look like `task-1.Succeeded`. Results:
- `.Succeeded`: finished without error
- `.Failed`: non-zero exit code
- `.Errored`: any other error
- `.Skipped`: its `when` was false
- `.Omitted`: its own `depends` was false
- `.Daemoned`: daemon task no longer `Pending`
- `.AnySucceeded` and `.AllFailed`: for tasks with `withItems`

A bare task name equals `(task.Succeeded || task.Skipped || task.Daemoned)`, which is how `dependencies` behaves. So `depends: "task || task-2.Failed"` expands to that term OR `task-2.Failed`.

Operators are `&&`, `||` and `!`, with parentheses:

```yaml
depends: "(task-2.Succeeded || task-2.Skipped) && !task-3.Failed"
```

Rules:
- `dependencies` and `depends` cannot appear in the same task group.
- To convert, join with `&&`: `dependencies: [A, B, C]` becomes `depends: "A && B && C"`.
- `dag.task.continueOn` is unavailable with `depends`; use `.Failed` in the expression instead.
- ContainerSet templates cannot use it.

Skipped or Omitted tasks produce no outputs, so references such as `{{tasks.stage-b.outputs.parameters.message}}` resolve to an empty string.

## Checked
2026-11-03. Confirmed against the Argo Workflows Enhanced Depends Logic page: task results table, the default expansion for a bare task name, operators, AnySucceeded and AllFailed, the compatibility rules with dependencies and continueOn, and empty-string output references. The ContainerSet limitation is confirmed on the ContainerSet Template page. Nothing removed.
Method: documentation only; no commands were run.

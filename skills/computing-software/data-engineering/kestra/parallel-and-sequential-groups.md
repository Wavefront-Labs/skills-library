---
id: computing-software.data-engineering.kestra.parallel-and-sequential-groups
name: parallel-and-sequential-groups
category: computing-software
field: data-engineering
product: kestra
tags: [parallel, sequential, concurrent, task-groups, process-runner]
level: intro
status: docs-checked
description: "Run Kestra tasks in parallel with a concurrent cap, or in ordered groups with Sequential, including Sequential groups nested inside Parallel."
sources:
  - https://kestra.io/docs/how-to-guides/parallel-vs-sequential
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`Parallel` runs child tasks together; `concurrent` caps how many run at once. With `concurrent: 3`, a new task starts as soon as a running one completes. A task placed after the group runs once the whole group is done.

```yaml
tasks:
  - id: parent
    type: io.kestra.plugin.core.flow.Parallel
    concurrent: 3
    tasks:
      - id: t1
        type: io.kestra.plugin.scripts.shell.Commands
        taskRunner:
          type: io.kestra.plugin.core.runner.Process
        commands:
          - 'echo "running {{task.id}}"'
  - id: last
    type: io.kestra.plugin.core.log.Log
    message: "{{task.id}} > {{taskrun.startDate}}"
```

`Sequential` runs its children in order. Nest `Sequential` groups inside `Parallel` to run two ordered chains side by side:

```yaml
- id: parent
  type: io.kestra.plugin.core.flow.Parallel
  tasks:
    - id: seq1
      type: io.kestra.plugin.core.flow.Sequential
      tasks: []   # t1, t2, t3 run one after another
    - id: seq2
      type: io.kestra.plugin.core.flow.Sequential
      tasks: []   # t4, t5, t6 run one after another
```

(`tasks: []` abbreviates the children shown on the page.)

## Checked

2026-11-04. Confirmed against the Kestra parallel versus sequential how-to page: Parallel with concurrent 3, the start-as-one-completes behaviour, the last task running after the group, and Sequential groups nested in Parallel. Nothing removed.

Method: documentation only; no commands were run.

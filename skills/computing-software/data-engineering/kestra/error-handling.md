---
id: computing-software.data-engineering.kestra.error-handling
name: error-handling
category: computing-software
field: data-engineering
product: kestra
tags: [errors, allowfailure, allowwarning, error-handler, taskswithstate, alerting]
level: practitioner
status: docs-checked
description: "Handle failures in Kestra with flow-level and task-level errors blocks, allowFailure and allowWarning, and the tasksWithState expression."
sources:
  - https://kestra.io/docs/workflow-components/errors
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three controls:

- `errors`: tasks that run sequentially when a task or the flow fails.
- `allowFailure`: downstream tasks continue; the execution ends in `WARNING`.
- `allowWarning`: downstream tasks continue; the execution ends in `SUCCESS`.

Flow-level handler:

```yaml
errors:
  - id: error_handler
    type: io.kestra.plugin.core.log.Log
    message: I'm failing task '{{ tasksWithState('FAILED')[0]['taskId'] }}'
    level: INFO
```

`tasksWithState()` returns an array; `[0]` is the first failed task. Other expressions seen on the page: `{{ flow.namespace }}`, `{{ flow.id }}`, `{{ execution.id }}`, `{{ task.id }}`.

A local handler is an `errors` list on a flowable task and covers only that task's children. An `errors` on a `Sequential` named `t2` catches `t2-t1` but not a sibling task `t1`.

```yaml
  - id: allow_failure
    type: io.kestra.plugin.core.execution.Fail
    allowFailure: true
```

By default a failed task stops downstream tasks. For actions based on the final state, use `afterExecution`.

## Checked

2026-11-04. Confirmed against the Kestra errors page: errors, allowFailure (execution ends WARNING), allowWarning (ends SUCCESS), tasksWithState('FAILED')[0], local handler scope with the t2 example, afterExecution pointer. Nothing removed.

Method: documentation only; no commands were run.

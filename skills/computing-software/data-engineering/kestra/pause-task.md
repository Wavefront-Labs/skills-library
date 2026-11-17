---
id: computing-software.data-engineering.kestra.pause-task
name: pause-task
category: computing-software
field: data-engineering
product: kestra
tags: [pause, approval, resume, onresume, pauseduration]
level: practitioner
status: docs-checked
description: "Halt a Kestra execution with the Pause task for approvals or delays: pauseDuration, behavior on timeout, onResume inputs, and resume via UI or API."
sources:
  - https://kestra.io/docs/workflow-components/tasks/flowable-tasks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`Pause` halts an execution until it is resumed manually or a timeout expires.

Properties:

- `pauseDuration`: ISO 8601 duration.
- `behavior`: what happens when the duration ends: `RESUME` (default), `WARN`, `CANCEL`, `FAIL`.
- `onResume`: inputs the approver supplies when resuming.

Resume from the Gantt tab or the API:

```
POST /api/v1/executions/{executionId}/resume
```

Read what the approver entered with:

```
{{ outputs.<pause_task_id>.onResume.<input_id> }}
```

Execution state while waiting is `PAUSED`, which returns directly to `RUNNING` on resume. A paused execution keeps its concurrency slot until it reaches a terminal state, so approvals can hold limits. Do not confuse it with `BREAKPOINT` (Enterprise debug state).

## Checked

2026-11-04. Confirmed against the Kestra flowable tasks page: pauseDuration, behavior values RESUME (default), WARN, CANCEL and FAIL, onResume inputs and their output path, resume from the Gantt tab or POST /api/v1/executions/{executionId}/resume. PAUSED returning directly to RUNNING, BREAKPOINT being Enterprise, and the paused execution keeping its concurrency slot are confirmed on the Kestra states and concurrency pages. Nothing removed.

Method: documentation only; no commands were run.

---
id: computing-software.data-engineering.kestra.replay-execution
name: replay-execution
category: computing-software
field: data-engineering
product: kestra
tags: [replay, recovery, revisions, executions, validate-replay, correlation-id]
level: practitioner
status: docs-checked
description: "Replay a Kestra execution from a chosen task, reuse upstream outputs, pick a flow revision, and understand the revision safety check and its limits."
sources:
  - https://kestra.io/docs/how-to-guides/replay
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Replay re-runs an execution from a chosen task. Tasks that already succeeded are skipped and Kestra reuses their outputs.

In the UI: Gantt or Logs tab, three-dot menu on a task, Replay; or replay one or many from the Executions page. The dialog offers the original revision, the latest, or a specific one; pick the latest to include a fix saved as a new revision.

Afterward: skipped tasks keep their output, the replayed task shows a higher attempt count, and the Overview tab shows labels `system.replay: true` and `system.correlationId` linking to the original.

Revision check: replaying on the Latest or a Specific revision is refused if a task before the replay point changed, was renamed, was removed, or had a task inserted in front of it; if an input was removed, changed type or lost its default value; or if a variable was removed or changed. You can still edit the replayed task, later tasks and tasks that never ran. Changes to `description`, `retry`, `timeout`, `workerSelector`, `allowFailure` and `allowWarning` are ignored. On failure choose "Replay the whole execution instead".

API check:

```
POST /api/v1/{tenant}/executions/{executionId}/actions/replay/validate
```

with `taskRunId` and `revision` query parameters; `200` if possible, `409` with the reason otherwise.

A passing check is no guarantee of identical results: secrets may have changed, file and non-interactive inputs may differ, and Pebble calls to external systems may return other values.

To rerun missed schedule intervals use Backfill instead.

## Checked

2026-11-04. Confirmed against "Re-run Any Workflow Execution from a Chosen Task" (how-to-guides/replay): UI paths, revision options, system.replay and system.correlationId labels, attempt label, revision check rules and ignored properties, Replay the whole execution instead, validate endpoint with 200 and 409, limits of the check, Backfill pointer. Corrected the revision check rule: inputs and variables are checked by their own rules (removed, retyped, lost default), not as task properties.
Method: documentation only; no commands were run.

---
id: computing-software.data-engineering.kestra.execution-states
name: execution-states
category: computing-software
field: data-engineering
product: kestra
tags: [execution-states, terminal-states, cancelled, killed, paused, task-run-states]
level: practitioner
status: docs-checked
description: "Kestra execution and task run states: transient vs terminal, how CANCELLED differs from KILLED, key transitions, and which states task runs lack."
sources:
  - https://kestra.io/docs/workflow-components/states
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Transient: `CREATED`, `SUBMITTED`, `QUEUED` (only when concurrency slots are full), `RUNNING`, `PAUSED` (approval or fixed delay), `BREAKPOINT` (Enterprise only), `RESTARTED`, `RETRYING` (flow-level retry), `KILLING`.

Terminal:

- `SUCCESS`: completed, or only allowed failures.
- `WARNING`: completed with warnings.
- `FAILED`: a task failed and will not be retried.
- `RETRIED`: retried under `CREATE_NEW_EXECUTION`; a new execution replaces it.
- `RESUBMITTED`: resubmitted directly.
- `SKIPPED`: blocked by a condition, SLA policy or concurrency behavior.
- `CANCELLED`: system action when a concurrency limit with `CANCEL` is hit.
- `KILLED`: user stopped it via the Kill button or API; passes through `KILLING`.

Transitions:

- `PAUSED` goes straight back to `RUNNING` on resume; there is no RESUMING state.
- `FAILED` runs `errors` handlers first; with `RETRY_FAILED_TASK` it moves to `RETRYING` instead.
- `RETRYING` ends in `SUCCESS`, `WARNING` or `FAILED`.

Task runs use the same states except `QUEUED`, `CANCELLED` and `PAUSED`. For a task run, `SUBMITTED` means queued to a worker.

## Checked

2026-11-04. Confirmed against the Kestra states page: the transient and terminal state lists and meanings, CANCELLED versus KILLED, PAUSED returning directly to RUNNING, FAILED and RETRY_FAILED_TASK, RETRIED with CREATE_NEW_EXECUTION, and the task run state differences. Nothing removed.

Method: documentation only; no commands were run.

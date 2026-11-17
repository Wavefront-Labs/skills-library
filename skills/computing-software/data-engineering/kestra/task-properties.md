---
id: computing-software.data-engineering.kestra.task-properties
name: task-properties
category: computing-software
field: data-engineering
product: kestra
tags: [tasks, flowable, runnable, runif, allowfailure, loglevel, timeout]
level: practitioner
status: docs-checked
description: "Kestra task basics: flowable vs runnable tasks and the common properties id, type, retry, timeout, runIf, disabled, allowFailure, logLevel and logToFile."
sources:
  - https://kestra.io/docs/workflow-components/tasks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Tasks are the steps of a flow.

- Flowable tasks orchestrate (for example `io.kestra.plugin.core.flow.Parallel`, `Switch`, `Loop`).
- Runnable tasks do the work and run on workers (for example `io.kestra.plugin.core.http.Request`).

Common properties:

- `id`, `type` (full class name), `description`.
- `retry`: how often and how to retry a failed task.
- `timeout`: maximum duration, ISO 8601.
- `runIf`: skips the task when false. A task run is still created with state `SKIPPED`.
- `disabled`: removes the task; no task run is created, no trace.
- `allowFailure`: continue the execution even if this task fails.
- `allowWarning`: allow the task run to be marked Success despite warnings.
- `logLevel`: level persisted to the database; `INFO` excludes `DEBUG` and `TRACE`. By default all logs are stored.
- `logToFile`: store logs as a file in internal storage instead of the database; also settable on triggers.
- `workerSelector`: Enterprise Edition only.

Dynamic properties accept Pebble expressions. Check the plugin docs or the task's documentation tab in the UI to see which properties are dynamic.

## Checked

2026-11-04. Confirmed against "Understand Runnable vs. Flowable Tasks in Your Flows" (workflow-components/tasks): flowable and runnable examples, every core property description, runIf SKIPPED versus disabled behaviour, workerSelector EE-only, logLevel and logToFile semantics, dynamic property advice. No claims removed.
Method: documentation only; no commands were run.

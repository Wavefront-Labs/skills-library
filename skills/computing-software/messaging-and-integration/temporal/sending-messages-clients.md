---
id: computing-software.messaging-and-integration.temporal.sending-messages-clients
name: sending-messages-clients
category: computing-software
field: messaging-and-integration
product: temporal
tags: [signal-with-start, update-with-start, startupdate, query, stack-trace, workflowidconflictpolicy, sending-messages]
level: practitioner
status: docs-checked
description: "Send Signals, Updates and Queries to a Temporal workflow: Signal-With-Start, update stages Accepted or Completed, Update-With-Start conflict policies, stack trace query."
sources:
  - https://docs.temporal.io/sending-messages
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Signals go from any Client, the CLI, or one workflow to another. Signal-With-Start signals a running execution with the given Workflow ID or starts it and signals at once, atomically.

Updates are synchronous: Client or CLI calls the handler. Before v1.25.0 enable `frontend.enableUpdateWorkflowExecution` and `frontend.enableUpdateWorkflowExecutionAsyncAccepted` (for the dev server pass `--dynamic-config-value key=true` to `temporal server start-dev`). Except in Go, `executeUpdate` returns the result; `startUpdate` takes a stage and returns a handle:
- Accepted: the Worker was contacted, so the Update is persisted (a Validator may reject it).
- Completed: wait for the handler's result, same as `executeUpdate`.

Update-With-Start (server 1.28 recommended) needs a `WorkflowIDConflictPolicy`. If the workflow exists, you gave an Update ID, and that Update exists in the latest run, it attaches to it regardless of policy (for a closed workflow, only if the Update completed). Otherwise policy and `WorkflowIDReusePolicy` decide whether to start, then the Update begins. Patterns:
- Lazy init, such as a shopping cart: `USE_EXISTING`.
- Early return, such as payment validation while the workflow continues: `FAIL` plus a unique Update ID.
It is not atomic: if the Update cannot be delivered (no Worker), the workflow still starts; SDKs retry without guarantee.

Queries run via Client or CLI, even on completed workflows. Many SDKs expose the built-in `__stack_trace` Query (call stack of all threads, running executions only) for diagnosing stuck workflows; it needs no workflow code.

## Checked

2026-11-03. Confirmed against the Temporal documentation pages: sending-messages (under https://docs.temporal.io/). Nothing removed.

Method: documentation only; no commands were run.

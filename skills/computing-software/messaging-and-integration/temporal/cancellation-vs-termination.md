---
id: computing-software.messaging-and-integration.temporal.cancellation-vs-termination
name: cancellation-vs-termination
category: computing-software
field: messaging-and-integration
product: temporal
tags: [cancellation, termination, workflow-cancel, workflow-terminate, cancelled-failure, disconnected-context]
level: practitioner
status: docs-checked
description: "Cancel or terminate a Temporal workflow: events recorded, cleanup outside the cancelled scope, activity heartbeats, pending activities, pause interaction and reset."
sources:
  - https://docs.temporal.io/encyclopedia/workflow/cancellation-and-termination
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Cancellation is cooperative: the Workflow receives it and decides what to do. Termination is forceful: the execution closes immediately and code never sees it. Prefer Cancellation; terminate when a workflow cannot process it (nondeterminism error, no Workers). CLI: `temporal workflow cancel` and `temporal workflow terminate`; both also take a List Filter instead of a Workflow ID for bulk action.

Cancel: records `WorkflowExecutionCancelRequested` (requester and reason), schedules a new Workflow Task, and the SDK raises a Cancelled Failure in workflow code. Unhandled it closes as Canceled (`WorkflowExecutionCanceled`); handled and returned normally it closes Completed (Java still closes as Canceled). Cleanup that runs Activities must execute outside the cancelled scope (Go: `workflow.NewDisconnectedContext`). Activities get cancellation only when they heartbeat; throttling can delay it. A workflow can cancel another (`RequestCancelExternalWorkflowExecutionInitiated`, then `ExternalWorkflowExecutionCancelRequested`; a child records `ChildWorkflowExecutionCanceled`).

Terminate: records `WorkflowExecutionTerminated` with an optional reason (defaults to the user's name; always give one). No cleanup or compensation, and pending Activities are not stopped cleanly; reserved inventory, locks and partial writes remain.

Comparison: cancel takes effect on the next Workflow Task and does not work on a stuck workflow; terminate is immediate and does.

Related: Parent Close Policy uses these for children (Terminate default). A cancel sent to a Paused workflow takes effect after unpause; terminate is immediate. Reset ends the current run and starts a new one from a chosen history point. Timeouts close as Timed Out.

## Checked

2026-11-08. Read in full: the Cancellation and Termination page (docs.temporal.io/encyclopedia/workflow/cancellation-and-termination). Every remaining claim matches those pages. Nothing removed.

Method: documentation only; no commands were run.

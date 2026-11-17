---
id: computing-software.messaging-and-integration.temporal.workflow-lifecycle-end-to-end
name: workflow-lifecycle-end-to-end
category: computing-software
field: messaging-and-integration
product: temporal
tags: [how-temporal-works, lifecycle, frontend, history-service, matching-service, commands, events, task-queue]
level: practitioner
status: docs-checked
description: "Trace one Temporal workflow and activity through Client, Frontend, History, Matching and Worker, including which commands and events appear."
sources:
  - https://docs.temporal.io/encyclopedia/architecture/how-temporal-works
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: know which component does what when a workflow runs, so you can reason about stuck or duplicated work.

Three separate parts talk over gRPC. The Client only sends control requests (start, signal, query, cancel, get result). The Server records Event History, queues Tasks and persists to a database. The Worker polls Task Queues and runs your Workflow and Activity code; the Server never runs it.

Workflow side:
1. Client calls `StartWorkflowExecution` on Frontend with Workflow type, input and Task Queue; Frontend forwards to History.
2. History writes `WorkflowExecutionStarted` and `WorkflowTaskScheduled`, plus an internal Transfer Task.
3. A History queue processor calls Matching `AddWorkflowTask`.
4. A Worker's `PollWorkflowTask` is matched; History appends `WorkflowTaskStarted`.
5. The SDK replays history, then runs workflow code until it finishes or blocks.
6. Calls such as execute-Activity become Commands (`ScheduleActivityTask`, `StartTimer`), sent in `RespondWorkflowTaskCompleted`.
7. History turns Commands into Events (`WorkflowTaskCompleted`, `ActivityTaskScheduled`).

Activity side: Matching receives `AddActivityTask`; a Worker's `PollActivityTask` takes it. History sets timeout timers but does not write `ActivityTaskStarted` until the final attempt ends. Success (`RespondActivityTaskCompleted`) appends `ActivityTaskStarted`, `ActivityTaskCompleted` and `WorkflowTaskScheduled`. On failure (`RespondActivityTaskFailed`) a retry is scheduled with no Events written; only when retries are exhausted or the error is non-retryable does `ActivityTaskFailed` appear.

The loop repeats until a `CompleteWorkflowExecution` command yields `WorkflowExecutionCompleted`. Closed executions never reopen; open ones accept queries and signals.

## Checked

2026-11-08. Read in full on the How Temporal works page: every concrete claim (names, events, rules, fields) matches the page. Component roles, the 15-step sequence, Command and Event names and the activity retry rules all confirmed.

Method: documentation only; no commands were run.

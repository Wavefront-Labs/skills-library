---
id: computing-software.messaging-and-integration.temporal.workflow-tasks-and-task-failures
name: workflow-tasks-and-task-failures
category: computing-software
field: messaging-and-integration
product: temporal
tags: [workflow-task, activity-task, nexus-task, replay, task-failure, execution-failure, tasks]
level: practitioner
status: docs-checked
description: "Temporal task types: when Workflow Tasks are scheduled, replay on each task, task failure versus execution failure, activity and Nexus task events."
sources:
  - https://docs.temporal.io/tasks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Task is a unit of work Workers poll from Task Queues. Three kinds: Workflow, Activity, Nexus.

Workflow Tasks are scheduled when the execution starts, on a Signal, on an Update, when an Activity completes or fails, when a Timer fires, when a Child Workflow completes, and when a failed Workflow Task must be retried. A task bundles all new events since the last one finished. The Worker receives the full Event History, replays code from the start (completed Activities and Timers return results from history, no I/O), runs new code to the next blocking point, then returns Commands, which the Service persists as Events.

Task failure versus execution failure:
- Workflow Task failure (nondeterminism, unhandled exception, task timeout, invalid Commands, bad binary checksum): retried automatically with exponential backoff, the execution stays Open, the same history keeps growing; fix code or infrastructure and redeploy.
- Workflow Execution failure (business logic error, uncaught Activity failure, external terminate or cancel): closes Failed, not retried unless a Workflow Retry Policy exists, in which case each retry is a new Run with its own history.

Activity Task: one attempt. `ActivityTaskScheduled` is written when queued and `ActivityTaskStarted` at pickup, ending in Completed, Failed, TimedOut, Canceled or Terminated.

Nexus Task: delivers a request to start or cancel an Operation. `NexusOperationScheduled`, `NexusOperationStarted` (returns an operation token), then a final event. The Service may issue several Nexus Tasks per call, so handlers must be idempotent; `WorkflowRunOperation` dedupes by Workflow ID.

## Checked

2026-11-08. Read in full on the Tasks page: every concrete claim (names, events, rules, fields) matches the page.

Method: documentation only; no commands were run.

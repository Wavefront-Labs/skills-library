---
id: computing-software.messaging-and-integration.temporal.activity-execution-async-completion
name: activity-execution-async-completion
category: computing-software
field: messaging-and-integration
product: temporal
tags: [activity-execution, async-completion, task-token, activity-id, cancellation, standalone-activity, heartbeat]
level: practitioner
status: docs-checked
description: "Temporal activity execution kinds, cancellation delivery, Activity ID rules, async completion with Task Token versus Signals."
sources:
  - https://docs.temporal.io/activity-execution
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An Activity Execution orchestrates the whole lifecycle including retries. Three flavours: Workflow Activity (scoped to a Workflow Run, recorded in Event History, result goes to the Workflow); Standalone Activity (started by a Client, own top-level lifetime, no Event History, separate Activity ID space, suited to job processing); Local Activity (same process as the Workflow, skips the Task Queue, not fully durable).

Temporal guarantees an Activity Task either runs or times out. Lost tasks are detected only through Start-To-Close timeout, then retried per policy. With a maximum of 1 attempt, a timeout means no retry.

Cancellation: Activities must heartbeat to receive it. It arrives when cancellation was requested, a timeout fired (Cancelled Failure message `TIMED_OUT`), the Workflow Run closed (`NOT_FOUND`), or, in some SDKs, the Worker is shutting down or heartbeat details failed conversion. Let the failure propagate to accept; catch it to ignore. Cancellation is delivered only once per Activity.



Async completion: the function returns without completing; any Client later heartbeats and completes it, identified by a Task Token or by Activity ID plus Workflow ID (and optional Run ID). Prefer passing IDs to external services because a retry invalidates the Task Token.

Choosing: Async Completion if the external system is unreliable or needs heartbeats or cancellation. Signals if it is trusted: use a one-minute Start-To-Close, notify the system, complete without result, and let it Signal back, so a failed notification retries in a minute instead of after a week-long timeout.

## Checked

2026-11-08. Read in full on the Activity Execution page: every concrete claim (names, events, rules, fields) matches the page.

Method: documentation only; no commands were run.

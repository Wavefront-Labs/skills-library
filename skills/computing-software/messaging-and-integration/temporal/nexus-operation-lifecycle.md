---
id: computing-software.messaging-and-integration.temporal.nexus-operation-lifecycle
name: nexus-operation-lifecycle
category: computing-software
field: messaging-and-integration
product: temporal
tags: [nexus-operation, circuit-breaker, schedule-to-close, nexus-timeouts, exactly-once, nexus-cancellation, callbacks]
level: advanced
status: docs-checked
description: "Temporal Nexus operation lifecycle: schedule-to-close, schedule-to-start and start-to-close timeouts, circuit breaker states, idempotency, cancellation versus termination."
sources:
  - https://docs.temporal.io/nexus/operations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Handlers are defined with SDK builders: New-Workflow-Run-Operation (async, backed by a workflow) and New-Sync-Operation (Query, Signal, Update or other reliable code via the Client). The caller issues `ScheduleNexusOperation`, handing off atomically to Nexus Machinery; history shows `NexusOperationScheduled`, then for async `NexusOperationStarted` (operation token returned) and a Nexus Completion Callback, ending in Completed, Failed, Canceled or TimedOut.

Retries: retryable Nexus errors, or upstream timeouts, are retried until Schedule-to-Start or Schedule-to-Close expires; return a non-retryable Nexus error to stop. This differs from Activity error handling.

Timeouts (set by the caller):
- Schedule-to-Close: total duration, 60 days maximum in Cloud; expiry gives `NexusOperationTimedOut`.
- Schedule-to-Start: wait for the handler to start (or finish, if sync); `TIMEOUT_TYPE_SCHEDULE_TO_START`; needs Server 1.31.0+; zero means none.
- Start-to-Close: async only, from start to completion; `TIMEOUT_TYPE_START_TO_CLOSE`; Server 1.31.0+.

Circuit breaker: per caller-Namespace and Endpoint pair. It opens after 5 consecutive retryable errors (Worker outages causing timeouts count), goes half-open after 60 seconds for one probe, and closes on success or reopens for another 60 seconds on failure. Pending operations then show state `Blocked` with `BlockedReason` ("The circuit breaker is open."); inspect with `temporal workflow describe -w <id>`. Sync handlers that fail repeatedly can trip it.

Semantics: at-least-once, so make handlers idempotent. For exactly-once, back the Operation with a workflow using `WorkflowIDReusePolicy` of RejectDuplicates.

Cancelling a caller propagates to pending operations; terminating it abandons them and handlers keep running. Version with a new Service name and Task Queue (for example `prod.payments.v2`).

## Checked

2026-11-03. Confirmed against the Temporal documentation pages: nexus/operations (under https://docs.temporal.io/). Nothing removed.

Method: documentation only; no commands were run.

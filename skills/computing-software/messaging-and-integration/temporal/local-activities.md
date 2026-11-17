---
id: computing-software.messaging-and-integration.temporal.local-activities
name: local-activities
category: computing-software
field: messaging-and-integration
product: temporal
tags: [local-activity, markerrecorded, workflow-task-heartbeat, low-latency, at-least-once]
level: practitioner
status: docs-checked
description: "When to use Temporal local activities: in-process execution, MarkerRecorded events, workflow task heartbeating at 80 percent of timeout, at-least-once semantics."
sources:
  - https://docs.temporal.io/local-activity
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Local Activity runs in the same Worker process as the Workflow that schedules it. It never enters an Activity Task Queue: the Workflow Worker runs it from an in-process queue, skipping the Service round trip, so latency and Event History size drop. It is an optimisation, not a replacement for regular Activities.

Flow: schedule, in-process queue, immediate execution, result returned directly, and when the Workflow Task completes the Worker records one `MarkerRecorded` Event holding the result. Regular Activities instead send `ScheduleActivityTask` and are tracked by the Service.

Use one only if the operation is short (a few seconds including retries), runs in the Workflow's binary, needs no routing or global rate limiting, and is idempotent. Good fits: light transforms, small computations, in-memory cache reads, fast local file operations. Use regular Activities for network requests, databases, external APIs, long work, heartbeating, or durable retries.

No Activity heartbeats. Instead, Workflow Task heartbeating: when a Local Activity nears about 80% of the Workflow Task Timeout (default 10 seconds), the Worker completes the Workflow Task and requests a new one. Costs: extra Events; Signals are not processed until Local Activities finish; Workflow Commands are held until completion or the next heartbeat. If work regularly nears the timeout, make it a regular Activity.

Durability: the result is durable only once the marker is written. A Worker crash before then re-runs the Local Activity, so semantics are at-least-once. After the marker exists, replay uses the recorded result.

## Checked

2026-11-08. Read in full: the Local Activity page (docs.temporal.io/local-activity). Every remaining claim matches those pages. Nothing removed.

Method: documentation only; no commands were run.

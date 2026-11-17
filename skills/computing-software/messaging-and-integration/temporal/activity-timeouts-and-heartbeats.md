---
id: computing-software.messaging-and-integration.temporal.activity-timeouts-and-heartbeats
name: activity-timeouts-and-heartbeats
category: computing-software
field: messaging-and-integration
product: temporal
tags: [activity-timeouts, start-to-close, schedule-to-close, schedule-to-start, heartbeat, heartbeat-timeout, throttling]
level: practitioner
status: docs-checked
description: "Choose Temporal activity timeouts: Schedule-To-Start, Start-To-Close, Schedule-To-Close and Heartbeat timeout, with throttling intervals and defaults."
sources:
  - https://docs.temporal.io/encyclopedia/detecting-activity-failures
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An Activity Execution has several Activity Task Executions (attempts). Timeouts:

Start-To-Close: limit for one attempt; no default of its own. If only Schedule-To-Close is set, the Service uses it as Start-To-Close. If neither is set the Activity is rejected (for Workflow Activities a Bad Schedule Activity Attributes Workflow Task error). Always set it, longer than the longest legitimate run: the Server cannot detect a crashed Worker, so this timeout forces the retry. On expiry `ActivityTaskTimedOut` is written, retry is scheduled if the policy allows, and the timer resets.

Schedule-To-Close: whole Execution from first schedule to last attempt closing; default infinity. Caps total duration without touching Maximum Attempts. One of the two must be set.

Schedule-To-Start: time queued before a Worker picks the task; enforced per attempt; default infinity. Non-retryable by design, since a retry would land in the same queue. Prefer watching `temporal_activity_schedule_to_start_latency`.

Heartbeats: pings from the Activity proving progress, optionally carrying a payload the next attempt can read to resume. Heartbeat Timeout is the maximum gap; on breach the attempt fails and may retry. `0s` (also the stored value when unset) disables it, and it is capped at Start-To-Close. Cancellation is delivered only on a heartbeat. Local Activities do not heartbeat.

Throttling: the Worker sends at most one heartbeat per interval = min(0.8 x heartbeat timeout, or `defaultHeartbeatThrottleInterval` 30 s if unset; `maxHeartbeatThrottleInterval` 60 s), both settable in Worker options. The final heartbeat before a failure is not throttled.

## Checked

2026-11-03. Confirmed against the Temporal documentation pages: encyclopedia/detecting-activity-failures (under https://docs.temporal.io/). Nothing removed.

Method: documentation only; no commands were run.

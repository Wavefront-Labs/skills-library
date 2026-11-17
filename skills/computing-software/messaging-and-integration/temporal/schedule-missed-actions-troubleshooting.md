---
id: computing-software.messaging-and-integration.temporal.schedule-missed-actions-troubleshooting
name: schedule-missed-actions-troubleshooting
category: computing-software
field: messaging-and-integration
product: temporal
tags: [schedule-missed-actions, catchup-window, overlap-policy, buffer-one, buffer-all, skip-policy, schedule-describe, backfill]
level: practitioner
status: docs-checked
description: "Investigate Temporal Schedules that skipped Actions: schedule_missed_catchup_window alert, temporal schedule describe counters, overlap policy pitfalls and remediation."
sources:
  - https://docs.temporal.io/troubleshooting/schedule-missed-actions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Alert on any non-zero skip counter: self-hosted `schedule_missed_catchup_window` (group by `namespace`), Cloud `temporal_cloud_v1_schedule_missed_catchup_window_count` (group by `temporal_namespace`), for example `sum by (namespace) (increase(schedule_missed_catchup_window[5m])) > 0`. It is Namespace-scoped, so find the Schedule:

    temporal schedule list --namespace <ns>
    temporal schedule describe --schedule-id <id> --namespace <ns>

Add `-o json` to script across Schedules. The `info` counters: `missedCatchupWindow` (identifies the culprit), `overlapSkipped` (Skip policy), `bufferDropped` (buffer full), `bufferSize`, `recentActions`, `runningWorkflows`.

Root causes: an outage longer than a tight Catchup Window (default is one year, minimum ten seconds); Namespace rate limiting (check `schedule_rate_limited`); `BufferAll` overruns (`temporal_cloud_v1_schedule_buffer_overruns_count` in Cloud, `schedule_buffer_overruns` self-hosted; also examine `bufferSize`).

Policy pitfalls, using a 5-minute Schedule whose first run takes 22 minutes:
- `Skip` (default) discards overlapping Actions: only 09:00 and 09:25 start.
- `BufferOne` keeps the oldest waiting Action (09:05), and skips later ones while the buffer is occupied. On the current Scheduler it must still be inside its Catchup Window when eligible.
- `BufferAll` starts one Action after each close; backlog grows if runs outlast the interval, with an internal limit of roughly 1,000 per Schedule. With a 5-minute window, at 09:22 only the 09:20 Action survives.
- `CancelOther` waits for the Workflow to process cancellation, then starts the newest waiting Action, so a slow Workflow can push it past the window. `TerminateOther` needs no cooperation.
- `AllowAll` means unbounded concurrency if runs are long.

Remediate: widen the Catchup Window beyond worst-case downtime, revisit the Overlap Policy, raise throughput limits, and Backfill the missed interval.

## Checked

2026-11-03. Confirmed against the Temporal documentation pages: troubleshooting/schedule-missed-actions (under https://docs.temporal.io/). Replaced the elided buffer-overrun metric name with the page names.

Method: documentation only; no commands were run.

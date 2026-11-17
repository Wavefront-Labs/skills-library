---
id: computing-software.messaging-and-integration.temporal.schedules-spec-and-policies
name: schedules-spec-and-policies
category: computing-software
field: messaging-and-integration
product: temporal
tags: [schedule, overlap-policy, catchup-window, phase-offset, backfill, pause-on-failure, calendar-spec]
level: practitioner
status: docs-checked
description: "Temporal Schedules: action and spec, intervals with phase offset, overlap policies, catchup window default one year, pause-on-failure, backfill and last completion result."
sources:
  - https://docs.temporal.io/schedule
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Schedule has its own identity, independent of any execution, and is itself implemented as a workflow (hidden when using Elasticsearch). For one future start use Start Delay instead. Started workflows get the action timestamp appended to the Workflow ID plus Search Attributes `TemporalScheduledStartTime` and `TemporalScheduledById`.

Spec: actions normally start within 1 second. Either an interval (`45m`; `6h/5h` adds a phase) or calendar fields `year, month, dayOfMonth, dayOfWeek, hour, minute, second, comment`, or a 5 to 7 field cron string via the CLI. Hour, minute and second default to `0`, others to `*`. Intervals align to the Unix epoch; for a phase offset use `offset = referenceTimestampUTC % interval` (every 10 days at 17:00 UTC on 2024-06-19: `1718816400 % 864000 = 320400`). Also: multiple specs, start/end bounds, exclusions (not in CLI or UI), jitter, and time zones (UTC by default; UTC recommended).

Overlap Policy when a prior run is still open: `Skip` (default), `BufferOne`, `BufferAll`, `CancelOther`, `TerminateOther`, `AllowAll` (the only one permitting concurrent runs). A Workflow Pause counts as still running.

Catchup Window: how late an action may start; default one year, minimum ten seconds; manual triggers and backfills ignore it.

Pause stops future actions but not started runs; `temporal schedule trigger` still works, and a notes field explains the state. Pause-on-failure pauses after a failed or timed-out (not cancelled or terminated) run. Backfill runs missed actions in a window now. A limit on actions makes it act paused afterwards.

## Checked

2026-11-03. Confirmed against the Temporal documentation pages: schedule (under https://docs.temporal.io/). Nothing removed.

Method: documentation only; no commands were run.

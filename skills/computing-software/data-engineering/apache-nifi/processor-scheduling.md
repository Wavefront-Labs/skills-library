---
id: computing-software.data-engineering.apache-nifi.processor-scheduling
name: processor-scheduling
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, scheduling, timer-driven, cron-driven, concurrent-tasks, run-schedule]
level: intro
status: docs-checked
description: "Processor Scheduling tab: timer, event and CRON strategies, Run Schedule default 0 sec, concurrent tasks, execution on primary node, and run duration slider."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scheduling tab

- Scheduling Strategy:
  - Timer driven (default): runs every Run Schedule interval.
  - Event driven: triggered when FlowFiles enter the feeding connections; marked experimental as of NiFi 1.10.0 and not supported by all processors; Run Schedule is not configurable, and it is the only mode where Concurrent Tasks may be 0 (threads then limited by the Event-Driven Thread Pool size).
  - CRON driven: six required fields (seconds, minutes, hours, day of month, month, day of week) and an optional year (empty or 1970-2099), separated by spaces; for example `0 0 13 * * ?` runs at 1:00 PM every day.
- Concurrent Tasks: thread count; acts as a relative weighting of resources among processors.
- Run Schedule: a duration like `1 second` or `5 mins`; default `0 sec` means run as often as data is available.
- Execution: All Nodes or Primary Node (marked with a "P").
- Run Duration slider: Lower latency to Higher throughput.

"Run Once" in the context menu runs the processor exactly once and works only with Timer driven and CRON driven strategies; it does not trigger if the processor is blocked, for example by back pressure.

Verify: the processor's tasks/time statistics reflect the schedule you set.

## Checked

Confirmed in the NiFi User Guide, Scheduling Tab: the three strategies and Timer driven as default, experimental note, CRON field table and example, Concurrent Tasks as relative weighting, Run Schedule default of 0 sec, Execution All Nodes or Primary Node with the P marker, the Run Duration slider labels, and the Run Once description.

Method: docs-only read of cited pages, 2026-11-08

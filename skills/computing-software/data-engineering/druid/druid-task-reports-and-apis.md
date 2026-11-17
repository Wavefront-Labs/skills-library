---
id: computing-software.data-engineering.druid.druid-task-reports-and-apis
name: druid-task-reports-and-apis
category: computing-software
field: data-engineering
product: druid
tags: [tasks, task-reports, overlord-api, sys-tasks, ingestion-stats]
level: practitioner
status: docs-checked
description: "Inspect running and finished ingestion tasks with the Overlord API, sys.tasks and task reports."
sources:
  - https://github.com/apache/druid/blob/master/docs/ingestion/tasks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Tasks do all ingestion work. For batch ingestion you usually submit tasks yourself through the task APIs; for streaming, supervisors submit them for you.

Where to look:
- The Overlord HTTP API submits and cancels tasks, checks status, and fetches logs and reports.
- Druid SQL has a read-only `sys.tasks` table with active and recently completed tasks, holding a subset of what the Overlord API returns.

Task reports show rows ingested and any parse exceptions. They are supported by native batch tasks and Kafka and Kinesis ingestion tasks, for both running and completed tasks. After completion fetch the report from:

```
http://<OVERLORD-HOST>:<OVERLORD-PORT>/druid/indexer/v1/task/{taskId}/reports
```

The report has an `ingestionStatsAndErrors` section with the `taskId`, a `payload` containing `ingestionState`, `unparseableEvents` and `rowStats`. The row stats include `processed`, `processedBytes` and `processedWithError` counters, which is where to look when rows seem to go missing.

## Checked

2026-11-09: confirmed against the Druid Tasks page (docs/ingestion/tasks.md): the Overlord HTTP APIs, the read-only `sys.tasks` table holding a subset of the full report, task report support in native batch and Kafka and Kinesis ingestion tasks, the `/druid/indexer/v1/task/{taskId}/reports` path and the `ingestionStatsAndErrors` fields and counters.

Method: documentation only; no commands were run.

---
id: computing-software.data-engineering.databricks.dlt-event-log-monitoring
name: dlt-event-log-monitoring
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, dlt, delta-live-tables, lakeflow, dlt-event-log, event-log, data-quality-metrics, pipeline-observability, expectations]
level: practitioner
status: docs-checked
description: "Monitor Lakeflow declarative (DLT) pipelines from the event log: event_log() queries, expectation metrics, flow progress, backlog, lineage and publishing the log to a table."
sources:
  - https://docs.databricks.com/aws/en/dlt/observability
  - https://docs.databricks.com/aws/en/dlt/monitor-event-logs
  - https://docs.databricks.com/aws/en/sql/language-manual/functions/event_log
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DLT / Lakeflow pipeline event log monitoring

**Goal:** answer "did the pipeline run, how much data moved, how many rows failed expectations, and why did it fail" with SQL, and alert on it.

## 1. Open the event log
```sql
-- by table owned by the pipeline (Unity Catalog)
SELECT * FROM event_log(TABLE(prod.silver.orders));
-- by pipeline id
SELECT * FROM event_log('<pipeline-id>');
```
Wrap it in a view for dashboards: `CREATE VIEW ops.dlt_orders_events AS SELECT * FROM event_log('<pipeline-id>');`
Alternatively configure the pipeline to **publish the event log to a UC table** (pipeline settings > event log: catalog, schema, name) so any job or alert can query it with normal grants.

Key columns: `timestamp`, `event_type`, `level` (INFO/WARN/ERROR/METRICS), `message`, `details` (JSON), `origin` (pipeline, update_id, flow_name), `error`.

## 2. Useful event types
| `event_type` | Tells you |
|---|---|
| `update_progress` | update state: QUEUED, RUNNING, COMPLETED, FAILED, CANCELED |
| `flow_progress` | per-flow status, rows written, expectations, backlog |
| `planning_information` | why a materialized view refreshed fully vs incrementally |
| `cluster_resources` | autoscaling, task slots, utilisation |
| `user_action` | who started/stopped/edited the pipeline |
| `flow_definition` | schema and input datasets (lineage) |

## 3. Data-quality metrics
```sql
SELECT timestamp, origin.flow_name, e.name AS expectation, e.passed_records, e.failed_records
FROM event_log('<pipeline-id>')
LATERAL VIEW explode(from_json(details:flow_progress:data_quality:expectations,
  'array<struct<name:string,dataset:string,passed_records:bigint,failed_records:bigint>>')) x AS e
WHERE event_type = 'flow_progress'
  AND details:flow_progress:data_quality:expectations IS NOT NULL
ORDER BY timestamp DESC;
```
Dropped-row counts: `details:flow_progress:data_quality:dropped_records`.

## 4. Throughput, backlog, failures
```sql
-- rows written per flow per update
SELECT origin.update_id, origin.flow_name, sum(details:flow_progress:metrics:num_output_rows::bigint) AS rows_out
FROM event_log('<pipeline-id>') WHERE event_type='flow_progress' GROUP BY ALL;
-- streaming backlog
SELECT timestamp, origin.flow_name, details:flow_progress:metrics:backlog_bytes
FROM event_log('<pipeline-id>') WHERE event_type='flow_progress';
-- errors with stack
SELECT timestamp, origin.flow_name, message, error FROM event_log('<pipeline-id>') WHERE level='ERROR' ORDER BY timestamp DESC;
```

## 5. Alerting
- SQL alert on failed-record ratio above threshold, or on latest `update_progress` = FAILED.
- Pipeline notifications (email on update failure/success, flow failure) in pipeline settings; job-level notifications if scheduled by a job.

## Verify
- [ ] Expectation metrics query returns rows for each flow with expectations.
- [ ] A deliberately failing update triggers an alert within the expected time.
- [ ] Event log is queryable by the on-call group without owner privileges (published table or view with grants).

## Checked

2026-10-28: reviewed against the official documentation fetched this batch.

Confirmed on the Databricks pipeline event log pages and the event_log function reference: event_log(TABLE(...)) and event_log(pipeline id), publishing the event log to a Unity Catalog table, event types update_progress, flow_progress, planning_information, cluster_resources and user_action, flow_progress data_quality expectations and dropped_records, metrics num_output_rows and backlog_bytes, pipeline notifications.

Removed: backlog_files metric and the event log retention remark (not on the pages read).

Method: documentation only; no commands were run.

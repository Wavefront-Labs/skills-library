---
id: computing-software.cloud-infrastructure-engineering.google-cloud.exporting-traces-to-bigquery
name: exporting-traces-to-bigquery
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, trace-profiler, trace-bigquery-export, cloud-trace, observability-analytics, latency-analysis]
level: advanced
status: docs-checked
description: "Analyse Cloud Trace spans with SQL: Observability Analytics on the _AllSpans view, when a linked BigQuery dataset is needed, and the deprecated trace sinks to BigQuery."
sources: ["https://cloud.google.com/trace/docs/trace-export-bigquery", "https://cloud.google.com/trace/docs/analytics"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exporting traces to BigQuery

## 1. Current approach: Observability Analytics
Observability Analytics runs SQL against the default `_AllSpans` view, which holds all trace data stored by the project. Prerequisites: billing enabled, the Observability API enabled, and these roles: Observability View Accessor (`roles/observability.viewAccessor`) on the views to query, and Observability Analytics User (`roles/observability.analyticsUser`) on the project.

In the console open Observability Analytics, then Views, Traces, `_Trace.Spans._AllSpans`. The fully qualified name is `PROJECT_ID.LOCATION._Trace.Spans._AllSpans`. If the view is missing, the project has no observability bucket named `_Trace` (see the page's "Trace storage initialization fails" troubleshooting).

You do NOT need a linked BigQuery dataset just to query traces (or traces plus logs). You need one to:
- join trace data with other BigQuery datasets;
- query traces from BigQuery Studio or Data Studio;
- run Observability Analytics queries on your BigQuery reserved slots;
- monitor query results with an alerting policy.

## 2. Query
The documented example groups spans by hour, name and kind and averages duration:
```sql
SELECT
  TIMESTAMP_TRUNC(start_time, HOUR) AS hour_start_time,
  name AS span_name,
  kind,
  AVG(duration_nano) AS average_duration_nano,
  COUNT(*) AS count_all
FROM `PROJECT_ID.us._Trace.Spans._AllSpans`
GROUP BY TIMESTAMP_TRUNC(start_time, HOUR), name, kind
LIMIT 100
```
Columns used there: `start_time`, `name`, `kind`, `duration_nano`. Check the Schema pane for the rest, and cast fields when stored as strings. Use the time-range selector for time filters: a `WHERE` on the timestamp field overrides it and disables the selector. If the toolbar shows "Run in BigQuery", switch Settings back to Analytics (default).

## 3. Legacy trace sinks (deprecated)
- From 18 February 2026 export of spans to BigQuery through Cloud Trace sinks is deprecated; sinks are removed on or after 18 February 2027; you cannot create or modify trace sinks. Migrate to Observability Analytics.
- An existing sink writes to an ingestion-time partitioned table whose schema follows the Trace V2 API `Span`; Trace patches the table when a span carries a new attribute. You manage retention of those tables yourself in BigQuery.
- The legacy export docs mark the feature Beta (pre-GA terms).

## Gotchas
- Trace holds sampled requests only, so percentiles are estimates (general tracing caveat; not stated on the cited pages).
- Attribute keys depend on the instrumentation; inspect the schema before filtering.

## Checked
Confirmed 2026-11-08 against "Query and analyze traces" and "Export to BigQuery" (Cloud Trace). Removed claims the pages do not state or contradict: `gcloud alpha trace sinks create` and the `bigquery.dataEditor` writer-identity step (sinks can no longer be created), the legacy-sink sample query and `bq show --schema` advice, the 30-day Trace retention figure, and cost advice. The linked-datasets source returned 404 and was dropped.
Method: docs-only read of cited pages, 2026-11-08

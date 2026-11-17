---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-logging-queries-and-log-based-metrics
name: cloud-logging-queries-and-log-based-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-logging, logging, log-queries, logging-query-language, log-based-metrics, log-exclusions, logs-explorer, log-analytics, structured-logging, jsonpayload, severity, trace-correlation, log-ingestion-cost, default-sink, saved-queries, error-logs, logging-iam]
level: practitioner
status: docs-checked
description: "Use Cloud Logging well: query operators, structured JSON logging, log-based metrics, exclusions for cost control, and Log Analytics."
sources: ["https://cloud.google.com/logging/docs/view/logging-query-language", "https://cloud.google.com/logging/docs/structured-logging", "https://cloud.google.com/logging/docs/logs-based-metrics", "https://cloud.google.com/logging/docs/exclusions", "https://cloud.google.com/logging/docs/log-analytics", "https://cloud.google.com/logging/docs/view/building-queries", "https://cloud.google.com/sdk/gcloud/reference/logging/metrics/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Logging queries and log-based metrics

**Goal:** find the one request that failed across every service in a minute, turn
patterns in logs into metrics and alerts, and keep the logging bill under control.

## 1. Query language essentials
```
resource.type="cloud_run_revision" resource.labels.service_name="payments-api"
severity>=ERROR
timestamp>="2026-10-15T08:00:00Z" AND timestamp<"2026-10-15T09:00:00Z"
jsonPayload.message:"timeout"                 -- has: substring match
logName=~"cloudaudit.googleapis.com%2F(activity|data_access)"   -- regex
NOT textPayload:robot                         -- negation
jsonPayload.user_id:*                         -- field exists
SEARCH("ORD-12345678")                        -- full text search across fields
```
- Operators: `=`, `!=`, `>` `<` `>=` `<=`, `:` (has: any substring of the field), `=~` and `!~` (regex), `AND`, `OR`, `NOT`; multiple statements on separate lines are joined with an implicit `AND`.
- Structured logs (a JSON object in `jsonPayload`) let you query and index specific JSON paths; a string in `textPayload` can be searched but its content cannot be indexed. Log JSON, one object per line, and keep key names stable because they are your query API.
- `gcloud logging read '<FILTER>' --project=<P> --limit=50 --format=json --freshness=1h` (`--freshness` defaults to 1d, `--order` to `desc`).
- Logs Explorer shows a selectable time range; narrow it before running broad queries.

## 2. Log-based metrics
```bash
gcloud logging metrics create payments_declined --description="declined payments" \
  --log-filter='resource.type="cloud_run_revision" jsonPayload.message="payment declined"'
```
- `gcloud logging metrics create` takes `--description`, `--log-filter` and `--bucket-name` (bucket-scoped metric), or `--config-from-file=<PATH>` with a full metric definition (use the file for labels and value extractors; see the log-based metrics docs for its schema).
- User-defined metrics only see log entries received after the metric is created; they are not retroactively populated.
- User-defined (project-scoped) log-based metrics are calculated from both included and excluded logs; system log-based metrics are calculated from included logs only.

## 3. Cost control
- Add exclusions to a sink: `gcloud logging sinks update _Default --add-exclusion=name=drop-hc,filter='<FILTER>'` (the flag takes `name`, `filter`, `description`, `disabled`). Excluded logs are not stored in the bucket, but user-defined log-based metrics still count them.
- Entries with timestamps older than the bucket's retention period or more than 24 hours in the future are discarded.

## 4. Log Analytics
Enable analytics on a bucket with `--enable-analytics` (accepted by `gcloud logging buckets create` and `update`). After upgrading the bucket you can query it with SQL in Log Analytics, and create a linked BigQuery dataset to query the same data from BigQuery without exporting it.

## Gotchas
- `textPayload` entries cannot be indexed on content: prefer structured JSON.

## Verify
- [ ] A test entry with a known field value is found by `jsonPayload.<FIELD>="..."`.
- [ ] A log-based metric appears in Metrics Explorer after creation and increments on a test event (only entries after creation count).
- [ ] After adding an exclusion, matching entries no longer appear in the bucket.

## Checked

2026-10-27. Confirmed in the Logging query language, structured logging, log-based metrics, exclusions, Log Analytics and building-queries pages and the `gcloud logging read`, `metrics create`, `sinks update` and `buckets create/update` reference pages: query operators and `SEARCH()`, `textPayload` not indexable, `gcloud logging read` flags and defaults, `metrics create` flags (`--description`, `--log-filter`, `--bucket-name`, `--config-from-file`), no retroactive population, included versus excluded logs for user-defined and system metrics, `sinks update --add-exclusion` keys, 24-hour future timestamp rule, `--enable-analytics`, linked BigQuery dataset. Removed: `--label-extractors` and `--value-extractor` (not flags of `gcloud logging metrics create`), the special `logging.googleapis.com/...` key list and sample payload, the indexed-field list, `logging-sample-rate`, price and percentage figures, the 30-day retention and sampling advice, metric-descriptor and cardinality remarks, the Python library names, the agent-platforms source (404). Read end to end.

Method: documentation only; no commands were run.

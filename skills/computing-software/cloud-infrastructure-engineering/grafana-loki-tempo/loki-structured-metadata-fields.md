---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.loki-structured-metadata-fields
name: loki-structured-metadata-fields
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [structured-metadata, loki, trace-id, high-cardinality-fields, otlp-attributes, schema-v13]
level: practitioner
status: docs-checked
description: "Attach high-cardinality fields such as trace_id to log lines as Loki structured metadata without creating streams."
sources: ["https://grafana.com/docs/loki/latest/get-started/labels/structured-metadata/", "https://grafana.com/docs/loki/latest/reference/loki-http-api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep trace IDs, pod names and process IDs queryable without blowing up stream cardinality.

Requirements: schema version 13 or higher (chunk format V4) and the `tsdb` index; boltdb-shipper does not support it.
```yaml
limits_config:
  allow_structured_metadata: true
  volume_enabled: true
```
`allow_structured_metadata` defaults to true in the latest configuration reference; set it to false (or `-validation.allow-structured-metadata=false`) to disable it. OTLP ingestion requires structured metadata. Logs Drilldown needs `discover_log_levels` and `allow_structured_metadata` set to true.

Ways to attach it: add a JSON object as the third element of a push value (flat, string keys and string values, directly after the log line), or use Grafana Alloy's `stage.structured_metadata` block.

When to use it: OpenTelemetry-format ingestion, or high-cardinality metadata that should not be a label and is not in the log line (process_id, thread_id, Kubernetes pod names).

Query: structured metadata is added to the labels of each returned line, so filter with a label filter after the selector, without a parser:
```logql
{job="example"} | pod="myservice-abc1234-56789"
{job="example"} | pod="myservice-abc1234-56789" | trace_id="0242ac120002"
count_over_time({job="example"} | trace_id="0242ac120002" | keep job [5m])
```
Because the metadata becomes result labels, metric queries can hit `maximum of series (50000) reached for a single query`; use the `keep` or `drop` stages to remove labels you do not need.

Limits (latest reference defaults): `max_structured_metadata_size: 64KB` per line and `max_structured_metadata_entries_count: 128` per line. Lines over either limit are rejected by the distributor with HTTP 400. Metadata size also counts toward the ingestion rate limit.

## Verify
Run one of the queries above in Explore or with `logcli`; returned entries show the metadata fields as labels.

## Checked
2026-11-03. Confirmed against the Loki structured metadata page, HTTP API reference (third element in push values) and the configuration reference defaults. Removed: Alloy `loki.process`/`stage.json` snippet (only the `stage.structured_metadata` mention is on the page), the `otlp_config` label-mapping claim, and "scan within selected streams" wording.
Method: documentation only; no commands were run.

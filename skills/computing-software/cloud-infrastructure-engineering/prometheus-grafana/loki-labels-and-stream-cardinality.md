---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.loki-labels-and-stream-cardinality
name: loki-labels-and-stream-cardinality
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, loki, loki-labels, labels, streams, stream-cardinality, cardinality, structured-metadata, static-labels, dynamic-labels, label-design, max-streams-per-user, per-stream-rate-limit, chunk-efficiency, index-volume, series-api, analyze-labels, logcli, bloom-filters, otlp-ingest, otel-resource-attributes]
level: advanced
status: verified
description: "Design Loki labels so streams stay few and chunks full: static labels only, high-cardinality values into structured metadata, measuring streams with series/volume APIs, fixing a blow-up."
sources: ["https://grafana.com/docs/loki/latest/get-started/labels/", "https://grafana.com/docs/loki/latest/get-started/labels/bp-labels/", "https://grafana.com/docs/loki/latest/get-started/labels/structured-metadata/", "https://grafana.com/docs/loki/latest/operations/request-validation-rate-limits/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loki labels and stream cardinality

**Goal:** labels that describe *where logs come from* (a few thousand streams per tenant),
with everything else searchable via filters or structured metadata, so ingestion is cheap
and queries are fast.

## 1. Why Loki is different from Prometheus
A **stream** is a unique label set; every stream has its own chunks. Loki's index holds
only labels; line content is not indexed. Consequences:
- A new label value = a new stream = a new chunk being built in ingester memory and flushed
  (ideally when full ~1.5 MB). Thousands of tiny streams produce thousands of tiny chunks:
  expensive to write, store, and query.
- Prometheus-style cardinality (user id, request id, status code, path) is **catastrophic**
  here but harmless as line content, because queries brute-force lines fast with filters.
- Target: streams in the low thousands per tenant; chunks mostly > 500 KB
  (`loki_ingester_chunk_size_bytes` histogram) and age > several minutes
  (`loki_ingester_chunk_age_seconds`).

## 2. Label rules
Keep: `namespace`, `app`/`service_name`, `container`, `env`, `cluster`, `level` (bounded,
useful for filtering by selector), maybe `pod` on small clusters (pods churn → streams churn;
on large clusters move `pod` to structured metadata). Count: 5–8 labels.
Never: `trace_id`, `request_id`, `user_id`, `ip`, `path`, `status_code`, `timestamp`,
`hostname` on autoscaled fleets, anything from the log line itself.
For the Kubernetes+Alloy/Promtail defaults: keep the `kubernetes_sd` relabeled `namespace`,
`app` (from `app.kubernetes.io/name`), `container`; drop `pod_template_hash`, `controller_revision_hash`,
`instance`.

## 3. Structured metadata: the escape hatch
High-cardinality values that must be **filterable without parsing** go into structured
metadata: stored alongside each line, not in the index, filterable with label syntax.
```alloy
loki.process "k8s" {
  stage.json { expressions = { trace_id = "trace_id", user = "user.id" } }
  stage.structured_metadata { values = { trace_id = "", user = "" } }
  stage.labels { values = { level = "" } }
  forward_to = [loki.write.default.receiver]
}
```
```logql
{app="api"} | trace_id="4bf92f3577b34da6a3ce929d0e0e4736"
```
Requires schema v13 + TSDB and `allow_structured_metadata: true`. OTLP ingestion
(`/otlp/v1/logs`) maps a default list of resource attributes → labels (configure under `limits_config.otlp_config.resource_attributes`; a `default_resource_attributes_as_index_labels` key does not exist and is rejected at start-up)
and everything else → structured metadata; prune the resource attributes you promote.

## 4. Measure
```bash
logcli series '{namespace="prod"}' --analyze-labels      # streams and unique values per label
logcli series '{}' --since=1h | wc -l                     # total active streams
curl -G loki/loki/api/v1/index/volume --data-urlencode 'query={namespace="prod"}' --data-urlencode 'aggregateBy=labels'
curl -G loki/loki/api/v1/index/volume_range --data-urlencode 'query={namespace="prod"}' --data-urlencode 'targetLabels=app'
```
Prometheus metrics: `loki_ingester_memory_streams`, `sum by (tenant) (loki_ingester_streams_created_total)`,
`loki_discarded_samples_total{reason="per_stream_rate_limit"|"stream_limit"}`, chunk size/age histograms.

## 5. Guard rails
```yaml
limits_config:
  max_label_names_per_series: 15
  max_label_name_length: 1024
  max_label_value_length: 2048
  max_streams_per_user: 10000            # per ingester; 0 = unlimited
  max_global_streams_per_user: 50000     # across ingesters
  per_stream_rate_limit: 3MB
  per_stream_rate_limit_burst: 15MB
  max_entries_limit_per_query: 5000
```
Pair with a `stream_limit` discard alert so a cardinality explosion pages the platform team,
not the app team's dashboards.

## 6. Fix a blow-up
1. `--analyze-labels` on the hot selector: find the label with thousands of values.
2. Remove it at the shipper (Alloy `stage.label_drop`), or keep it as
   structured metadata (`stage.structured_metadata`).
3. Existing streams expire from ingester memory after `chunk_idle_period`; old chunks stay
   until retention — accept it or issue a delete request for the window.
4. Add a CI check on shipper config (`alloy fmt` and `alloy validate`)
   and a limit so it cannot recur silently.

## Gotchas
- `level` as a label is fine (≤ 6 values) and speeds selectors; but if the app writes
  `level=INFO`/`info`/`Info` variants you just tripled streams; normalize in the pipeline
  (`stage.template`/`ToLower`).
- `pod` on a Deployment with hourly rollouts creates permanent stream churn; the stream count
  looks fine instantly but the index grows.
- Static labels from `static_configs.labels` on every host (`host=...`) are fine; the
  **number of hosts** bounds them.
- OTLP ingestion defaults promote 18 resource attributes (`service.name`, `service.namespace`, `service.instance.id`, `deployment.environment(.name)`, `cloud.region`, `cloud.availability_zone`, `k8s.cluster.name`, `k8s.namespace.name`, `k8s.pod.name`, `k8s.container.name`, `container.name` and the k8s replicaset/deployment/statefulset/daemonset/cronjob/job names) to labels in Loki 3.7.9; `k8s.pod.name` is on the default list, so use `ignore_defaults: true` and your own list.

## Verify
- [ ] Streams per tenant in the low thousands; no label with > 1000 values in `--analyze-labels`.
- [ ] p50 chunk size > 500 KB and `discarded_samples{reason="stream_limit"}` is 0.
- [ ] Query by `trace_id` returns in < 2 s via structured metadata, with no parser in the query.

## Checked
Ran Loki 3.7.9 (local TSDB v13): pushed lines with an extra label and OTLP/HTTP logs to `/otlp/v1/logs`, checked which attributes became labels versus structured metadata, `{service_name=...} | trace_id=...` without a parser, `logcli series --analyze-labels`, `series '{}'`, `/index/volume` (`aggregateBy=labels`, `targetLabels=app`), `/index/volume_range`, `/index/stats`, and that the metrics named exist on `/metrics` (`loki_ingester_memory_streams`, `streams_created_total`, `chunk_size_bytes`, `chunk_age_seconds`, `discarded_samples_total`). The guard-rail `limits_config` block loaded with `-verify-config`; the default values were read from `-print-config-stderr` (labels 15/1024/2048, streams 5000 global, rate 3MB/15MB, entries 5000, chunk_target_size 1572864, chunk_idle_period 30m). `default_resource_attributes_as_index_labels` is rejected as an unknown field. The Alloy block was fixed to include `forward_to` and checked with `alloy validate` (v1.21.1), and the same stages ran end to end against Loki. Docs read: Loki otel/_index.md and get-started/labels (v3.7.9 source).

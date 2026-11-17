---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.loki-structured-metadata-and-otlp-ingestion
name: loki-structured-metadata-and-otlp-ingestion
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [loki, structured-metadata, structured-metadata-config, otlp-attribute-mapping-loki, loki-otlp-endpoint, otlp-loki-config, index-stats, volume-api, label-volume, stream-limit-tuning, max-line-size]
level: advanced
status: gated
description: "Use Loki's native OTLP endpoint and structured metadata: which OTel attributes become labels, customising otlp_config, analysing label volume, and tuning stream and line limits."
sources: ["https://grafana.com/docs/loki/latest/send-data/otel/", "https://grafana.com/docs/loki/latest/get-started/labels/structured-metadata/", "https://grafana.com/docs/loki/latest/reference/loki-http-api/#query-log-volume"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Structured metadata and OTLP ingestion

## Native OTLP endpoint
Loki 3.x accepts OTLP/HTTP at `/otlp/v1/logs`. Requirements: `schema: v13` + `store: tsdb`,
`limits_config.allow_structured_metadata: true` (default true in 3.7.9; with schema v12 Loki refuses to start and the error tells you to set it to false).
Collector side (gated: unconfirmed, source is paywalled or blocked): the OpenTelemetry Collector was not run here, so the exporter name and endpoint form come from the Loki OTLP docs only:
```yaml
exporters:
  otlphttp/loki:
    endpoint: http://loki-gateway.monitoring/otlp
    headers: {X-Scope-OrgID: tenant-a}
```

## What becomes what
- **Index labels** (default): 18 resource attributes in Loki 3.7.9: `service.name`, `service.namespace`,
  `service.instance.id`, `deployment.environment`, `deployment.environment.name`, `cloud.region`, `cloud.availability_zone`,
  `k8s.cluster.name`, `k8s.namespace.name`, `k8s.pod.name`, `k8s.container.name`, `container.name`, and the `k8s.{replicaset,deployment,statefulset,daemonset,cronjob,job}.name` ones (dots become underscores: `service_name`).
- **Structured metadata**: all other resource attributes, scope attributes, log attributes, plus `trace_id`, `span_id`, `severity_text` (a test also showed `severity_number`, `scope_name` and `detected_level`).
- **Log line**: the OTLP body.
Customise per tenant:
```yaml
limits_config:
  otlp_config:
    resource_attributes:
      attributes_config:
        - action: index_label
          attributes: [team]
        - action: drop
          regex: process\.command_line
    log_attributes:
      - action: drop
        attributes: [http.request.header.authorization]
```
Query structured metadata like labels after the selector: `{service_name="checkout"} | trace_id="4bf9..."`
(no parser needed).

## Label volume analysis
```bash
curl -sG $LOKI/loki/api/v1/index/volume --data-urlencode 'query={namespace=~".+"}' --data-urlencode 'targetLabels=app' -H 'X-Scope-OrgID: t'
curl -sG $LOKI/loki/api/v1/index/stats  --data-urlencode 'query={namespace="checkout"}'   # streams, chunks, entries, bytes
```
`volume_enabled` defaults to true in 3.7.9. `index/stats` returned zeros for data still in the ingester head, so expect counts only after flush.

## Stream and line limits
- `max_global_streams_per_user`, `max_label_names_per_series` (15 default), `max_label_value_length`.
- `max_line_size` + `max_line_size_truncate: true` to keep, not reject, huge lines.
- High-cardinality attributes (user IDs, request IDs) must stay structured metadata; promoting them to labels
  explodes streams.

## Verify
- [ ] `{service_name="x"}` returns OTLP logs with trace_id in structured metadata.
- [ ] Stream count per tenant stable after enabling OTLP (`loki_ingester_memory_streams`).

## Checked
Ran Loki 3.7.9 with the page's `otlp_config` (index_label `team`, drop regex on `process.command_line`, drop log attribute `http.request.header.authorization`) and posted an OTLP/HTTP JSON log record to `/otlp/v1/logs` with resource attributes `service.name`, `k8s.pod.name`, `team`, `process.command_line`, `host.name` and a trace/span id: labels became `service_name`, `k8s_pod_name`, `team`; `host_name`, `scope_name`, `severity_text`, `trace_id`, `span_id`, `user_id` were structured metadata; the dropped attributes were absent; `| trace_id="..."` matched without a parser. Checked the schema-v12 startup error and the `-verify-config` output, the default index-label list from `-print-config-stderr`, `max_structured_metadata_entries_count` 128 (a 129-entry push was rejected with 400), `max_line_size` 256KB and `max_line_size_truncate` (a 300KB line was accepted when truncation was on), and the `/index/volume` and `/index/stats` endpoints. Docs read: Loki send-data/otel and structured-metadata (v3.7.9). The Collector exporter snippet is gated as marked.

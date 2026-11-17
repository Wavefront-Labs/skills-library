---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.tempo-metrics-generator-configuration
name: tempo-metrics-generator-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [tempo-metrics-generator, tempo, span-metrics, service-graphs-processor, remote-write, host-info]
level: practitioner
status: docs-checked
description: "Configure the Tempo metrics-generator with span-metrics, service-graphs and host-info processors, remote write and per-tenant enablement via overrides."
sources: ["https://grafana.com/docs/tempo/latest/metrics-from-traces/metrics-generator/", "https://grafana.com/docs/tempo/latest/metrics-from-traces/metrics-generator/multitenancy/", "https://grafana.com/docs/tempo/latest/configuration/", "https://grafana.com/docs/tempo/latest/metrics-from-traces/span-metrics/span-metrics-metrics-generator/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: RED metrics and service graph series derived from spans. The metrics-generator is optional; in current Tempo it consumes spans from Kafka (the distributor writes them there) and remote-writes to a Prometheus-compatible endpoint. Processors available: service graphs, span metrics, host info. Tempo 3.0 removed the `local-blocks` processor; delete it from `processors`.

Processors are disabled by default and enabled per tenant in overrides:
```yaml
metrics_generator:
  registry:
    external_labels:
      source: tempo
  storage:
    path: /var/tempo/generator/wal
    remote_write:
      - url: http://<MIMIR_HOST>/api/v1/push    # Mimir; Prometheus uses /api/v1/write
        send_exemplars: true
  processor:
    span_metrics:
      dimensions: [http.method, http.route]
    service_graphs:
      peer_attributes: [peer.service, db.name, db.system]
overrides:
  defaults:
    metrics_generator:
      processors: [span-metrics, service-graphs]
```
Series: span metrics export `traces_spanmetrics_latency` (histogram), `traces_spanmetrics_calls_total` and `traces_spanmetrics_size_total` with labels `service`, `span_name`, `span_kind`, `status_code` (plus `status_message` only if enabled). Service graphs include `traces_service_graph_request_total` and `traces_service_graph_request_failed_total`. Host info emits `traces_host_info`.

Defaults worth knowing: `registry.collection_interval` 15s, `registry.stale_duration` 15m, `metrics_ingestion_time_range_slack` 30s (older spans are discarded), service graph `wait` 10s and `max_items` 10000, `intrinsic_dimensions` on except `status_message`.

Multi-tenancy: with multi-tenancy on, the generator forwards the `X-Scope-OrgID` header to remote write (`remote_write_add_org_id_header`, default true). Per-tenant credentials go in the `remote_write_headers` override (e.g. `Authorization: ${PROM_A_BASIC_AUTH}`, which needs `--config.expand-env`); do not put secrets in the `headers` map of `storage.remote_write` (shown in plaintext at `/status/config`), use `http_headers` with `secrets`. Tempo 3.0 disables legacy flat overrides unless `enable_legacy_overrides: true`.

Gotchas
- Each extra `dimensions` entry multiplies series; the docs describe a cardinality estimation page and a dry-run.
- A tenant without the processors in overrides gets no metrics.
- Missing `send_exemplars: true` removes metric-to-trace exemplar links.
- On Deployments (not StatefulSets) set `leave_consumer_group_on_shutdown: true` so partitions are reassigned quickly on rollout.

## Verify
Query `traces_spanmetrics_calls_total` in the receiving store and confirm series with your service names.

## Checked
2026-11-03. Confirmed against the Tempo metrics-generator overview, multitenancy page, configuration reference (metrics-generator block and defaults), span metrics page and configuration examples. Removed: the `histogram_buckets` example values, `distributor.metrics_generator_forwarder` remark, `tempo_metrics_generator_spans_received_total` check, the old generator-ring description and the `path`/`X-Scope-OrgID` header snippet.
Method: documentation only; no commands were run.

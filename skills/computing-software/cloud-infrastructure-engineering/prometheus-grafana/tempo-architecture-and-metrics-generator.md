---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.tempo-architecture-and-metrics-generator
name: tempo-architecture-and-metrics-generator
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, tempo, grafana-tempo, tempo-architecture, tempo-deployment, tempo-storage, distributor, live-store, block-builder, querier, query-frontend, compactor, metrics-generator, service-graph-metrics, span-metrics, service-graphs, traceql-metrics, otlp, object-storage, retention, parquet, vparquet, helm-tempo-distributed, trace-sampling, tenant-overrides]
level: advanced
status: docs-checked
description: "Run Grafana Tempo: monolithic vs microservices mode, Parquet blocks on object storage, per-tenant limits, and the metrics-generator for span metrics and service graphs."
sources: ["https://grafana.com/docs/tempo/latest/introduction/architecture/", "https://grafana.com/docs/tempo/latest/set-up-for-tracing/setup-tempo/", "https://grafana.com/docs/tempo/latest/metrics-from-traces/metrics-generator/", "https://grafana.com/docs/tempo/latest/configuration/", "https://grafana.com/docs/tempo/latest/operations/monitor/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tempo architecture, storage and metrics-generator

**Goal:** a trace backend that accepts OTLP from every service, stores traces cheaply in object storage, and derives
RED metrics and service graphs so dashboards and alerts do not depend on sampling luck.

Version note: the current docs describe the newer (3.0-era) architecture with Kafka, live-store and block-builder.
Older Tempo versions used ingesters and a compactor, and `local-blocks` was a metrics-generator processor. Check your
running version against the docs for that version before copying settings.

## 1. Components (current docs)
- **Distributor**: entry point; accepts OTLP (recommended), Jaeger and Zipkin, validates against per-tenant ingestion
  limits. Microservices mode: shards traces by trace ID and writes to Kafka. Monolithic mode: pushes in-process to the
  live-store and metrics-generator.
- **Kafka-compatible queue** (microservices mode only): durable write-ahead log; because Kafka acknowledges durability,
  Tempo can run at replication factor 1 on the write path.
- **Block-builder** (microservices mode): consumes from Kafka, builds Apache Parquet blocks and flushes them to object
  storage. In monolithic mode the live-store flushes blocks.
- **Live-store**: serves recent data from memory and a local WAL; can be deployed across availability zones.
- **Query frontend**: shards TraceQL queries and trace-ID lookups into jobs for queriers and merges results.
- **Querier**: runs jobs against live-stores (recent) and object storage (older).
- **Backend scheduler and worker**: compaction, retention and blocklist maintenance; they replace the legacy compactor.
- **Metrics-generator** (optional): derives RED metrics and service graphs from traces and remote-writes them to a
  Prometheus-compatible backend such as Prometheus or Mimir.

Modes: all components are in one binary and `-target` picks what runs. **Monolithic** is `-target=all` (the default),
needs no Kafka. **Microservices** runs each component as its own process, needs a Kafka-compatible system, and is
recommended for production. Object storage is recommended in both modes; a local filesystem backend is for development
and testing.

## 2. Storage
- Object storage backends: Amazon S3 (and S3-compatible such as MinIO), Google Cloud Storage, Azure Blob Storage.
- Data is stored in Apache Parquet blocks (columnar), so attribute queries read only the columns they need.
- Config reference (configuration page): block `version` options are `vParquet4` and `vParquet5` (default `vParquet5`);
  compaction `block_retention` default `336h`, `compacted_block_retention` default `1h`.
- `multitenancy_enabled` defaults to `false`. Tempo is multi-tenant when enabled; tenants are isolated at the storage
  level. Per-tenant overrides live in a file referenced by `per_tenant_override_config`, which is dynamically loaded
  and reloaded without a restart.

## 3. Limits (overrides)
- `rate_limit_bytes` default 30000000 (30 MB) and `burst_size_bytes` default 30000000, enforced by the distributor.
  `rate_strategy` is `local` (default; each distributor enforces the full rate, so the cluster rate grows with
  distributors) or `global` (the rate is divided across healthy distributors); it only affects `rate_limit_bytes`.
- `max_bytes_per_trace` default 5000000 (5 MB), enforced in the live-store and block-builder.
- `metrics_generator.max_active_series` caps active series per tenant.

## 4. Metrics-generator
Processors: `service-graphs`, `span-metrics`, `host-info`. Tempo 3.0 removed the `local-blocks` processor: remove any
`local-blocks` entries from `metrics_generator.processors`; the live-store handles TraceQL metrics on recent data.
- **Service graphs**: finds edges (parent-child spans that jump between two services), records request count and
  duration. Settings: `wait` (default `10s`, how long to wait for an edge to complete), `max_items` (default 10000),
  `histogram_buckets`, `dimensions`, `enable_client_server_prefix` (default false), `peer_attributes`,
  `filter_policies`.
- **Span metrics**: RED metrics per unique combination of dimensions. `intrinsic_dimensions` default true for
  `service`, `span_name`, `span_kind`, `status_code`; `status_message` default false and may have very high
  cardinality. Extra `dimensions` are searched in resource and span attributes. More dimensions mean higher
  cardinality, so keep them bounded. `filter_policies` include or exclude spans. Default `histogram_buckets` run from
  0.002 to 16.384 seconds.
- **Host info**: emits the `traces_host_info` gauge from `host_identifiers` (default `k8s.node.name`, `host.id`).
- Remote write: the generator runs a Prometheus Agent that sends to a configurable `remote_write` endpoint every
  `registry.collection_interval` (default `15s`). With multi-tenancy on, the original `X-Scope-OrgID` header is
  forwarded unless `remote_write_add_org_id_header` is false.
- Native histograms are supported; the receiving endpoint and dashboard queries must be updated for them.
- Sampling: if you sample before Tempo, where you generate metrics depends on how you sample (see Tempo docs "Choose
  where to generate metrics from traces"). `span_multiplier_key` and `enable_tracestate_span_multiplier` scale span
  metrics for sampled data.
- Rollouts: set `leave_consumer_group_on_shutdown: true` for Deployment-style rollouts (needs Kafka 2.4 or later);
  keep the default `false` for StatefulSets.
- Remote-writing to Grafana Cloud Metrics adds active series that can affect billing.

## 5. Operate
- Tempo emits Prometheus RED metrics for most services and logs in logfmt; the Tempo repository has a mixin with ten
  dashboards (Reads, Writes, Resources, Operational, Backend Work and others) that expect `cluster` and `namespace`
  labels.
- `tempo_query_frontend_bytes_inspected_total` (per tenant and op: traces, search, metadata, metrics) shows uncached
  query I/O; `tempo_live_store_query_inspected_bytes_total` isolates live-store bytes.
- Tempo self-tracing is configured through OpenTelemetry or Jaeger environment variables.

## Gotchas
- Dimensions on high-cardinality attributes (URLs, statements) inflate generated series; use bounded attributes and
  `max_active_series`.
- Service graph edges need both client and server spans arriving within `wait`.
- An oversized trace (above `max_bytes_per_trace`) means something is emitting unbounded spans; fix the
  instrumentation before raising the limit.

## Verify
- [ ] An OTLP span sent by a test generator is retrievable by trace ID in Grafana.
- [ ] Generated span metrics arrive in the remote-write target and the service graph renders edges.
- [ ] Traces older than the retention period are gone from object storage.

## Checked
2026-11-08: confirmed against the Tempo architecture overview, the metrics-generator page, the monitor page and the
configuration reference (defaults for block version, retention, rate limits, max_bytes_per_trace, processor settings,
registry collection_interval, multitenancy). Removed: the old ingester, compactor and WAL-flush description, the
`local-blocks` processor (removed in Tempo 3.0), the YAML sample with unconfirmed values, derived metric names, PromQL
examples, the Grafana data source settings and sizing claims (100k spans/s), because the fetched pages did not support
them or contradicted them.
Method: documentation only; no commands were run.

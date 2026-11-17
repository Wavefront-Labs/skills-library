---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.tempo-distributed-operations
name: tempo-distributed-operations
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [tempo-deployment, tempo-distributed-helm, tempo-helm-values, tempo-distributor-receivers, tempo-otlp-config, metrics-generator-config, span-metrics-config, service-graph-config, tempo-overrides, tempo-tenant-limits, tempo-multitenancy, tempo-tenant-header, tempo-compaction, block-retention-tempo, tempo-caching]
level: advanced
status: docs-checked
description: "Operate Tempo in microservices mode: Helm charts, multitenancy with X-Scope-OrgID, per-tenant overrides and their zero-value trap, metrics-generator settings, and retention."
sources: ["https://grafana.com/docs/tempo/latest/set-up-for-tracing/setup-tempo/deploy/kubernetes/helm-chart/", "https://grafana.com/docs/tempo/latest/configuration/", "https://grafana.com/docs/tempo/latest/metrics-from-traces/metrics-generator/", "https://grafana.com/docs/tempo/latest/operations/manage-advanced-systems/multitenancy/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Operating Tempo in microservices mode

Version note: current Tempo docs describe a 3.0 architecture (Kafka-compatible queue, live-store, block-builder, backend
scheduler and workers). The overrides mechanism works on both Tempo 2.x and 3.x; check the Tempo 3.0 migration guide
if upgrading. See `...prometheus-grafana.tempo-architecture-and-metrics-generator` for the component overview.

## Helm charts
- `tempo-distributed` deploys Tempo in microservices mode; `tempo` deploys it in monolithic (single binary) mode.
- The Tempo repository has an example Helm chart showing a complete microservices deployment. Chart values are not
  reproduced here; take them from the chart's own documentation.

## Multitenancy
- Tempo uses the `X-Scope-OrgID` header, set to the tenant name, for scoped writes and reads. It must be on all
  requests when multi-tenancy is enabled; OTLP ingestion supports it over gRPC and HTTP.
- Set it in the OpenTelemetry Collector (`headers`) or Grafana Alloy (`otelcol.exporter.otlphttp` `client { headers }`)
  on push, and in the Grafana Tempo data source via a custom HTTP header (`httpHeaderName1` plus the value in
  `secureJsonData.httpHeaderValue1`).
- Enable on the backend with `multitenancy_enabled: true` on all components (or `--multitenancy.enabled=true`); this
  forces every component to require the header. Default is `false`.

## Per-tenant overrides
- Point `overrides.per_tenant_override_config` at a separate file. It is loaded dynamically and can change at runtime
  without a restart.
- In the overrides file, tenants sit under `overrides:` with sections such as `compaction.block_retention`,
  `ingestion` (`rate_limit_bytes`, `burst_size_bytes`, `max_traces_per_user`), `global.max_bytes_per_trace` and
  `metrics_generator` (`processors`, `max_active_series`, `ring_size`, `collection_interval`, `forwarder`).
- **Trap:** set every field you want to keep. Unset fields become zero values, not the defaults from your main config;
  for example a `0s` retention effectively disables block retention for that tenant.
- Limit semantics: `rate_limit_bytes` default 30 MB with `rate_strategy` `local` (default) or `global`;
  `max_bytes_per_trace` default 5 MB. Compaction `block_retention` default is `336h`.

## Metrics-generator
- Processors: service graphs, span metrics, host info. `local-blocks` was removed in Tempo 3.0; remove it from
  `metrics_generator.processors`.
- It remote-writes to a Prometheus-compatible endpoint; with multi-tenancy on it forwards the original `X-Scope-OrgID`
  unless `remote_write_add_org_id_header` is false.
- Keep span-metrics `dimensions` low-cardinality; more dimensions mean higher cardinality. Use `max_active_series` per
  tenant.
- For Deployment rollouts, `leave_consumer_group_on_shutdown: true` (Kafka 2.4 or later); keep `false` for
  StatefulSets.

## Monitoring
The Tempo mixin (in the Tempo repository) has ten dashboards, including Reads, Writes, Resources, Operational and
Backend Work, which expect `cluster` and `namespace` labels. Use `tempo_query_frontend_bytes_inspected_total` for
query I/O.

## Verify
- [ ] A write without `X-Scope-OrgID` is rejected when multi-tenancy is on, and with the header lands under the tenant.
- [ ] Every tenant in the overrides file has all intended fields set (check retention is not `0s`).
- [ ] Generated span metrics reach the remote-write target under the expected tenant.

## Checked
2026-11-08: confirmed against the Tempo Helm chart page, multi-tenancy page (header, collector and data source setup,
overrides file, zero-value warning), the metrics-generator page and the configuration reference (defaults). Removed:
the Helm values sample, receiver port numbers, replica counts, memcached advice, the `local-blocks` processor,
metric names and alert names, because the fetched pages did not state them or showed them as removed.
Method: documentation only; no commands were run.

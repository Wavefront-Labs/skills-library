---
id: computing-software.search-and-information-retrieval.qdrant.monitoring-metrics
name: monitoring-metrics
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [monitoring, metrics, prometheus, telemetry, mon-metrics]
level: practitioner
status: docs-checked
description: "Scrape Prometheus metrics from /metrics, per-collection metrics and prefix, and read telemetry endpoints."
sources:
  - "https://qdrant.tech/documentation/ops-monitoring/monitoring/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Qdrant exposes metrics in Prometheus/OpenMetrics format at `/metrics` on the HTTP port (6333); configure it as a scrape target.

Facts from the docs:

- `/metrics` reports only the peer you connect to, so scrape each peer individually even with a load balancer in front. Counters such as created snapshots reset when the node restarts.
- Qdrant Cloud also offers `/sys_metrics` for cluster-level CPU, memory, disk and load balancer telemetry.
- Metric groups include application (`app_info`, `app_status_recovery_mode`, `quota_exceeded` from v1.19), collection (`collections_total`, `collection_points`, `collection_running_optimizations`, `collection_dead_replicas`, active replica min/max, from v1.16), snapshot, API response (`rest_responses_*` and `grpc_responses_*` including duration histograms from v1.8), process (jemalloc `memory_*_bytes`, `process_open_fds`, `process_max_fds`, `process_open_mmaps`, `system_max_mmaps`, page faults, from v1.16) and cluster consensus (`cluster_peers_total`, `cluster_term`, `cluster_pending_operations_total`, only in distributed mode).
- From v1.16.0 `service.metrics_prefix` (or `QDRANT__SERVICE__METRICS_PREFIX="qdrant_"`) adds a name prefix; by default there is none.
- From v1.18.0 `/metrics?per_collection=true` replaces the global API response metrics with series labelled by `collection` (plus `method`, `endpoint`, `status` for REST). It raises cardinality, so make sure the monitoring system can cope.
- `/telemetry` reports state from the queried peer's point of view (counts of vectors, shards and more; from v1.19.0 it includes a top-level `quota` field). `/cluster/telemetry` aggregates all peers with less detail but more reliable shard transfer progress.
- Hardware metrics (`collection_hardware_metric_*`, v1.13+) are reported only if `service.hardware_reporting` is enabled.

Sensible first signals from the same table: error counts and duration histograms per API, running optimizations, dead replicas, open file descriptors versus the maximum, and memory metrics.

## Checked

Method: docs-checked 2026-11-09 against the Qdrant monitoring and telemetry page (landing_page repo, ops-monitoring/monitoring.md), read in full. Removed the unconfirmed scrape YAML, the api-key header advice, the telemetry_disabled and memory-usage notes, and the trend alerting advice.

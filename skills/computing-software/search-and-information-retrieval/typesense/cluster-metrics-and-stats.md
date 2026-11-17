---
id: computing-software.search-and-information-retrieval.typesense.cluster-metrics-and-stats
name: cluster-metrics-and-stats
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [metrics-json, stats-json, health-endpoint, typesense]
level: practitioner
status: docs-checked
description: "Monitor Typesense with /health, /metrics.json (system and jemalloc memory metrics) and /stats.json (per-endpoint latency and requests per second); OUT_OF_DISK errors."
sources: ["https://typesense.org/docs/30.2/api/cluster-operations.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metrics, stats and health

## Health

`GET /health` returns health information about a node. When a node runs short of resources, the response also has a `resource_error` field set to `OUT_OF_DISK` or `OUT_OF_MEMORY`.

## Metrics

`GET /metrics.json` returns current RAM, CPU, disk and network usage. System metrics: `system_cpu_active_percentage`, per-core `system_cpuN_active_percentage`, `system_disk_total_bytes`, `system_disk_used_bytes`, `system_memory_total_bytes`, `system_memory_used_bytes`, `system_memory_total_swap_bytes`, `system_memory_used_swap_bytes`, `system_network_received_bytes`, `system_network_sent_bytes`.

Process memory comes from jemalloc: `typesense_memory_allocated_bytes` is the most direct measure of memory in use; `typesense_memory_active_bytes` is page-rounded and never below allocated; `typesense_memory_fragmentation_ratio` is `1 - (allocated_bytes / active_bytes)` (near 0 means low fragmentation); plus `mapped`, `metadata`, `resident` and `retained` bytes.

## API stats

`GET /stats.json` returns average requests per second and latencies for all requests in the last 10 seconds, per API endpoint.

A community Prometheus exporter (imatefx/typesense-prometheus-exporter) can poll the metrics and stats endpoints.

## Checked

Method: 2026-11-09 docs-only read of the cited Cluster Operations page in full. Confirmed the endpoints, resource_error values, metric names and definitions, and the 10-second stats window. Removed sample-response details (JSON field names and shapes), which the page text does not show.

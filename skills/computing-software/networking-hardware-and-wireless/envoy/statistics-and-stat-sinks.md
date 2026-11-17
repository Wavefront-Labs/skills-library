---
id: computing-software.networking-hardware-and-wireless.envoy.statistics-and-stat-sinks
name: statistics-and-stat-sinks
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, statistics, stats, counters, gauges, histograms, statsd, stat-prefix, stats-sinks]
level: practitioner
status: docs-checked
description: "Read Envoy server, HCM and cluster statistics, view them locally, and ship them via stat sinks with sensible tag extraction."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/observability/statistics.rst
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/operations/stats_overview.rst
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/configuration/observability/statistics.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# statistics and stat sinks
Envoy emits counters, gauges and histograms whose set depends on config. See them locally with `GET /stats` (add `?filter=regex`, `?format=prometheus`, `?usedonly`) and normally flush them to a sink such as statsd or Prometheus scraping.

The most used trees:
- `server.*`: `uptime`, `concurrency`, `memory_allocated`, `live` (1 unless draining), `state`, `total_connections`, `parent_connections` (old process during hot restart).
- `http.<stat_prefix>.*`: the HTTP connection manager; the prefix comes from the HCM `stat_prefix`.
- `cluster.<name>.*`: upstream cluster stats (for example `upstream_rq_total`, `upstream_cx_overflow`, `upstream_rq_pending_overflow`).
- `listener.<address>.*` and `control_plane.*`.

```yaml
stats_sinks:
- name: envoy.stat_sinks.statsd
  typed_config:
    "@type": type.googleapis.com/envoy.config.metrics.v3.StatsdSink
    tcp_cluster_name: statsd_cluster
```
Gotchas: during hot restart `server.memory_allocated` and `server.total_connections` cover both the old and new processes, and `server.parent_connections` is the old process only. Verify with `curl -s localhost:9901/stats?filter=server.live`.

## Checked

2026-11-03. Confirmed against: observability/statistics.rst (server.* gauges), cluster_stats.rst, http_conn_man stats, admin.rst (/stats options) and metrics stats.proto (StatsdSink). Removed or corrected: health_check.* and outlier.* tree names, the stat_prefix merge and cardinality claims, and the version hedge.

Method: documentation only; no commands were run.

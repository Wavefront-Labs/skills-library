---
id: computing-software.cloud-infrastructure-engineering.etcd.monitoring-metrics-endpoint
name: monitoring-metrics-endpoint
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [monitoring, metrics, prometheus, listen-metrics-urls, grafana, metrics-endpoint, observability]
level: practitioner
status: docs-checked
description: "Scrape etcd's Prometheus metrics at /metrics, the --metrics basic or extensive setting and separate metrics listeners."
sources:
  - "https://etcd.io/docs/v3.5/op-guide/monitoring/"
  - "https://etcd.io/docs/v3.5/metrics/"
  - "https://etcd.io/docs/v3.5/op-guide/configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Each etcd server exports metrics under the `/metrics` path on its client port, and optionally on the locations given by `--listen-metrics-urls`.

```bash
curl -L http://localhost:2379/metrics | grep -v debugging   # ignore unstable debugging metrics
```

- `--metrics` is `basic` (default) or `extensive`; `extensive` includes server-side gRPC histogram metrics.
- `--listen-metrics-urls` is a list of URLs for the metrics and health endpoints. Since v3.3.0 those locations also answer `/health`, which helps when the standard endpoint uses mutual TLS but a load balancer or monitoring service still needs the health check.
- Prometheus is the easiest way to ingest etcd's metrics: point its scrape config at each member's client endpoint (the page's example uses a 10s `scrape_interval`). The docs provide default alerts for etcd v3 clusters (adjust job labels, and pick labels unique to a cluster) and a default Grafana dashboard template to import after adding a Prometheus data source.
- etcd does not persist its metrics; they reset when a member restarts.

Metric names have an `etcd` or `etcd_debugging` prefix plus a subsystem prefix. The `etcd` namespace is stable, for monitoring and alerting, and changes appear in release notes. The `etcd_debugging` namespace is volatile and may change or be removed without warning. gRPC request metrics come from go-grpc-prometheus, and the Prometheus client adds `go` and `process` metrics such as `process_open_fds` and `process_max_fds` (not supported on macOS).

Key metrics from the metrics page: `etcd_server_has_leader` (1 or 0), `etcd_server_leader_changes_seen_total`, `etcd_server_proposals_committed_total`, `etcd_server_proposals_applied_total`, `etcd_server_proposals_pending`, `etcd_server_proposals_failed_total`, `etcd_disk_wal_fsync_duration_seconds`, `etcd_disk_backend_commit_duration_seconds` and `etcd_network_peer_round_trip_time_seconds`.

## Checked

2026-11-08. Read in full: etcd v3.5 Monitoring etcd page, Metrics page and Configuration options page (added as a source for the --metrics and --listen-metrics-urls flags). Confirmed everything above. Removed: the TLS curl example, the histogram-buckets wording, the repository dashboard JSON claim, the stable-name promotion remark, the mvcc size metric, and the scrape-per-member, 15s interval and history-retention advice (not on the pages read).
Method: documentation only; no commands were run.

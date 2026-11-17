---
id: computing-software.database-administration.dragonfly.prometheus-metrics-endpoint
name: prometheus-metrics-endpoint
category: computing-software
field: database-administration
product: dragonfly
tags: [prometheus, metrics, monitoring, grafana, dragonfly]
level: practitioner
status: docs-checked
description: "Scrape Dragonfly's Prometheus-compatible /metrics endpoint on the main or admin port and note the expired and evicted key counters."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/monitoring.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/getting-started/kubernetes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dragonfly allows HTTP on its main TCP port (6379 by default) and exposes Prometheus-compatible metrics at `:6379/metrics`. They include connection memory and pipeline metrics and replication metrics (role, connected replicas, backlog, lag).

Facts from the docs:

- From Dragonfly v2.0.0 the `dragonfly_expired_keys_total` and `dragonfly_evicted_keys_total` counters are always exported, even at zero. Earlier versions omitted them until the first key expired or was evicted.
- Batch I/O counters are available through `INFO stats` but are not currently exported to Prometheus.
- On Kubernetes, metrics are also available on admin port `9999`. Scraping port 6379 there may fail with `Received HTTP/0.9 when not allowed`, so scrape the admin port.
- The `/metrics` page bypasses authentication.

Steps:

1. Confirm manually: `curl http://host:6379/metrics`.
2. Add the target to Prometheus (with the Helm chart on Kubernetes, enable `serviceMonitor` and `prometheusRule` in the values file).
3. A complete Grafana monitoring stack example lives in the Dragonfly repository under `tools/local/monitoring`.
4. The Helm guide's alert rule uses `absent(dragonfly_uptime_in_seconds) == 1`; also alert on replication lag.

## Checked

2026-11-04. Confirmed in the Monitoring page (port, `/metrics`, v2.0.0 counters, batch I/O note, admin port 9999 on Kubernetes, replication metrics) and the Kubernetes getting-started page (`serviceMonitor`, `prometheusRule`, `absent(...)` rule). Removed the PodMonitor mention and the dashboard import step, which the pages do not state.

Method: documentation only; no commands were run.

---
id: computing-software.cloud-infrastructure-engineering.docker.grafana-dashboards-for-container-metrics
name: grafana-dashboards-for-container-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, grafana-docker-dashboard, cadvisor, node-exporter, grafana, promql, container-dashboards]
level: practitioner
status: docs-checked
description: "Build Grafana dashboards for Docker hosts from cAdvisor metrics: the documented mounts, core panels and PromQL, and which memory metric to graph."
sources:
  - https://github.com/google/cadvisor/blob/master/docs/storage/prometheus.md
  - https://grafana.com/docs/grafana/latest/dashboards/variables/
  - https://grafana.com/grafana/dashboards/1860-node-exporter-full/
  - https://prometheus.io/docs/guides/cadvisor/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Grafana dashboards for cAdvisor metrics

## Stack
cAdvisor exports per-container metrics on port 8080, Prometheus scrapes it, and Grafana
visualises it. The Prometheus cAdvisor guide runs cAdvisor in Compose with read-only mounts of
`/` (as `/rootfs`), `/sys` and `/var/lib/docker/`, plus `/var/run`. Add a scrape job for the
cAdvisor target in `prometheus.yml`.

## Core panels and PromQL
Metric names below are listed in cAdvisor's Prometheus metrics table. The `name` label is the
usual container-name label in cAdvisor output but is not documented in the table: open
Prometheus, look at the labels on `container_last_seen`, and adjust the selectors to match.

| Panel | Query |
|---|---|
| CPU per container (cores) | `sum by (name) (rate(container_cpu_usage_seconds_total{name=~"$container"}[5m]))` |
| CPU throttling ratio | `sum by (name) (rate(container_cpu_cfs_throttled_periods_total{name=~"$container"}[5m])) / sum by (name) (rate(container_cpu_cfs_periods_total{name=~"$container"}[5m]))` |
| Memory working set | `sum by (name) (container_memory_working_set_bytes{name=~"$container"})` |
| Memory vs limit | `container_memory_working_set_bytes / (container_spec_memory_limit_bytes > 0)` |
| OOM events | `increase(container_oom_events_total{name=~"$container"}[1h])` |
| Network receive | `sum by (name) (rate(container_network_receive_bytes_total{name=~"$container"}[5m]))` |
| Disk writes | `sum by (name) (rate(container_fs_writes_bytes_total{name=~"$container"}[5m]))` |
| Restarts (proxy) | `changes(container_start_time_seconds{name=~"$container"}[1h])` |

`container_memory_usage_bytes` is documented as including all memory regardless of when it was
accessed, so prefer `container_memory_working_set_bytes` ("current working set") for pressure panels.
`container_spec_memory_limit_bytes` is documented as the memory limit for the container; the
`> 0` filter above is a PromQL choice to drop series with no limit set, so check how your containers report it.

## Dashboard variables
Create a `container` dashboard variable from a Prometheus label query over `container_last_seen`
(see the Grafana variables documentation). Keep dashboards in Git rather than hand-edited in production.

## Community dashboards
The Grafana site hosts "Node Exporter Full" (dashboard ID 1860) for host metrics. Check any
imported dashboard against your cAdvisor version's metric names.

## Verify
- [ ] Selecting a container filters all panels; numbers roughly match `docker stats`.
- [ ] Every metric in the queries appears in the Prometheus UI for your cAdvisor target.

## Checked
2026-11-09. Confirmed against cAdvisor's Prometheus metrics page (all `container_*` metric names, types and the usage-versus-working-set descriptions) and the Prometheus cAdvisor guide (Compose mounts, port 8080).
Removed as unsupported by the fetched sources: `--docker_only=true`, the `/dev/disk` mount, host (node-exporter) panel queries and the `node_uname_info` host variable, the `$__rate_interval` usage, the `image` and Compose-service label claims, the OOM-killer comparison claim, provisioning paths, and the alert thresholds (90 percent, 25 percent, 15 percent free, 3 restarts).
Method: documentation only; no commands were run.

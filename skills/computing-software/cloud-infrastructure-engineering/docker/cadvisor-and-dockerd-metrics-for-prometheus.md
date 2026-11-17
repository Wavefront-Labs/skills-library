---
id: computing-software.cloud-infrastructure-engineering.docker.cadvisor-and-dockerd-metrics-for-prometheus
name: cadvisor-and-dockerd-metrics-for-prometheus
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, cadvisor, cadvisor-prometheus, container-metrics, metrics-addr, daemon-metrics, prometheus, observability]
level: practitioner
description: "Scrape per-container metrics with cAdvisor and engine metrics from dockerd metrics-addr into Prometheus, with the cAdvisor metric names to query."
sources: ["https://github.com/google/cadvisor/blob/master/docs/running.md", "https://docs.docker.com/engine/daemon/prometheus/", "https://github.com/google/cadvisor/blob/master/docs/storage/prometheus.md"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# cAdvisor and dockerd metrics for Prometheus

## cAdvisor
Run it as a container with the host mounts from cAdvisor's "Running" page (root filesystem read-only at `/rootfs`, plus the Docker state directories it lists), publishing port 8080:
```sh
docker run --volume=/:/rootfs:ro --publish=8080:8080 --detach=true --name=cadvisor <IMAGE> 
```
Take the full list of `--volume` mounts from the Running page. For a non-privileged container the page shows adding host devices (for example `--device=/dev/kmsg`) instead of `--privileged`; on RHEL and CentOS it says `--privileged=true` is required. The UI is then on `http://localhost:8080/`.

- Prometheus metrics are served under `/metrics` by default; the path can be changed with `-prometheus_endpoint`, and metric groups switched off or on with `-disable_metrics` / `-enable_metrics` (the Prometheus page lists each metric with its option group).
- Scrape target: `cadvisor:8080` in your Prometheus config.

Metrics named on cAdvisor's Prometheus page and useful in PromQL:
- `container_cpu_usage_seconds_total` (counter, cumulative CPU seconds): use `rate(...[5m])` for cores used.
- `container_memory_working_set_bytes` (gauge) against `container_spec_memory_limit_bytes` (gauge, memory limit).
- `container_network_receive_bytes_total` (counter).
- `container_oom_events_total` (counter of out-of-memory events).

## dockerd metrics
In `daemon.json` (Docker Desktop: Settings, then Docker Engine):
```json
{ "metrics-addr": "127.0.0.1:9323" }
```
Restart Docker. Metrics are exposed on port 9323 on the loopback interface; binding `0.0.0.0` exposes the port to the wider network, so weigh your threat model. From a Prometheus container, Docker's page scrapes `host.docker.internal:9323` (add `--add-host host.docker.internal=host-gateway` on Linux; Docker Desktop does it by default). Engine metric names carry an `engine_daemon_` prefix.

## Checked
2026-10-28. Confirmed against cAdvisor's Running and Prometheus pages (mounts, port 8080, `/metrics`, `-prometheus_endpoint`, `-disable_metrics`, metric names and types) and Docker's "Collect Docker metrics with Prometheus" page (`metrics-addr`, 9323, loopback default, `host.docker.internal`, Docker Desktop path). Removed unconfirmed claims: pinned image version, the `docker_only`, `housekeeping_interval`, `store_container_labels` and label whitelist flags, cardinality remarks, cgroup v2 version note, dockerd metric names beyond the prefix, Compose label aggregation advice.
Method: documentation only; no commands were run.

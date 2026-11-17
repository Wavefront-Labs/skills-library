---
id: computing-software.cloud-infrastructure-engineering.docker.container-metrics-and-log-shipping
name: container-metrics-and-log-shipping
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, cadvisor, fluent-bit, loki, promtail, container-metrics, log-shipping, observability, prometheus, grafana, docker-stats, node-exporter, docker-sd, alloy, otel-collector]
level: practitioner
status: gated
description: "Observability for a Docker host: cAdvisor + Prometheus for per-container CPU/memory/restart metrics, Fluent Bit or Alloy shipping json-file logs to Loki, and day-one alerts."
sources: ["https://github.com/google/cadvisor/blob/master/docs/running.md", "https://prometheus.io/docs/prometheus/latest/configuration/configuration/#docker_sd_config", "https://docs.fluentbit.io/manual/pipeline/inputs/docker-events", "https://docs.fluentbit.io/manual/pipeline/inputs/tail", "https://grafana.com/docs/loki/latest/send-data/docker-driver/", "https://grafana.com/docs/alloy/latest/reference/components/discovery/discovery.docker/", "https://docs.docker.com/engine/daemon/prometheus/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container metrics and log shipping

**Goal:** dashboards and alerts that answer "which container is eating memory / restarting /
throwing errors" on a Docker host, without an agent inside any image.

## Metrics: cAdvisor + Prometheus
cAdvisor reads cgroups and the Docker API and exposes per-container metrics at `:8080/metrics`.
```yaml
services:
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:v0.49.1
    privileged: true
    devices: ["/dev/kmsg"]
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    command: ["--docker_only=true", "--housekeeping_interval=10s", "--store_container_labels=false",
              "--whitelisted_container_labels=com.docker.compose.service,com.docker.compose.project"]
  node-exporter:
    image: prom/node-exporter:v1.8.2
    pid: host
    volumes: ["/:/host:ro,rslave"]
    command: ["--path.rootfs=/host"]
  prometheus:
    image: prom/prometheus:v2.54.1
    volumes: ["./prometheus.yml:/etc/prometheus/prometheus.yml:ro", "promdata:/prometheus"]
```
- `--docker_only` drops the raw cgroup tree noise; `--store_container_labels=false` plus a
  whitelist stops label cardinality explosions (every Compose label becomes a Prometheus
  label by default).
- `cgroup v2` hosts (Ubuntu 22.04+, Fedora): cAdvisor ≥ 0.45 required; older versions show
  zero for memory.
- `node-exporter` gives the host side (disk full on `/var/lib/docker` is the #1 incident).
- The daemon itself exports metrics (`"metrics-addr": "0.0.0.0:9323"` in `daemon.json`):
  engine-level counters (builds, image pulls, `engine_daemon_container_states_containers`).

Key cAdvisor series (names are the same ones Kubernetes dashboards use):
`container_memory_working_set_bytes` (what OOM uses, not `_usage_bytes` which includes
cache), `container_spec_memory_limit_bytes`,
`rate(container_cpu_usage_seconds_total[5m])`, `container_network_receive_bytes_total`,
`container_fs_usage_bytes`, `container_last_seen`. Restarts: not in cAdvisor — scrape the
engine metrics or alert on `changes(container_start_time_seconds[15m]) > 2`.

Prometheus can discover containers directly for apps that expose `/metrics`:
```yaml
scrape_configs:
  - job_name: docker
    docker_sd_configs: [{host: unix:///var/run/docker.sock}]
    relabel_configs:
      - source_labels: [__meta_docker_container_label_prometheus_scrape]
        regex: "true"
        action: keep
      - source_labels: [__meta_docker_container_label_prometheus_port]
        target_label: __address__
        regex: (.+)
        replacement: ${1}
      - source_labels: [__meta_docker_container_name]
        regex: /(.*)
        target_label: container
```
Containers opt in with `labels: {prometheus.scrape: "true", prometheus.port: "app:9090"}`.
Prometheus needs to be on the same Docker network as the targets.

## Logs: ship the json-file logs, keep `docker logs` working
Don't switch the daemon log driver to `fluentd`/`loki` unless you accept that `docker
logs` stops working (and that a dead collector blocks the container's stdout with the
default `mode: blocking`). Tail the files instead:

**Fluent Bit**
```ini
[INPUT]
    Name              tail
    Path              /var/lib/docker/containers/*/*-json.log
    Parser            docker
    Tag               docker.*
    DB                /var/log/flb_docker.db
    Mem_Buf_Limit     50MB
    Skip_Long_Lines   On
[FILTER]
    Name    lua
    Match   docker.*
    script  /fluent-bit/etc/container_id.lua       # extract the id from the path into a field
    call    add_id
[OUTPUT]
    Name   loki
    Match  docker.*
    Host   loki
    Port   3100
    labels job=docker, container_id=$container_id
```
Mount `/var/lib/docker/containers:ro` and run as root (the log files are 0640 root). The
`docker` built-in parser splits `{"log":..., "stream":..., "time":...}`. Container *names*
aren't in the file path; either use the Docker API from Lua, or prefer:

**Promtail / Grafana Alloy** (does the name/label enrichment for you):
```river
discovery.docker "host" { host = "unix:///var/run/docker.sock" }
discovery.relabel "docker" {
  targets = discovery.docker.host.targets
  rule { source_labels = ["__meta_docker_container_name"]; regex = "/(.*)"; target_label = "container" }
  rule { source_labels = ["__meta_docker_container_label_com_docker_compose_service"]; target_label = "service" }
}
loki.source.docker "host" {
  host       = "unix:///var/run/docker.sock"
  targets    = discovery.relabel.docker.output
  forward_to = [loki.write.default.receiver]
}
loki.write "default" { endpoint { url = "http://loki:3100/loki/api/v1/push" } }
```
This reads via the Docker API (like `docker logs`), so it works with the `local` driver
too and survives log rotation. The Loki Docker **driver plugin** (`docker plugin install
grafana/loki-docker-driver`) is the alternative; keep `--log-opt max-size` and
`loki-batch-size`, and know a Loki outage blocks logging unless `mode=non-blocking`.

**OpenTelemetry Collector** (`docker_stats` receiver for metrics, `filelog` receiver with
the `container` parser operator for logs) when you want one agent to many backends.

Keep labels low-cardinality in Loki: container name, compose service/project, host. Never
`container_id` as a label on a host with churn — put it in the line instead.

## Alerts worth having on day one
- `container_memory_working_set_bytes / container_spec_memory_limit_bytes > 0.9` for 5m.
- `increase(engine_daemon_container_actions_seconds_count{action="start"}[10m]) > 5` per
  container → crash loop (or `changes(container_start_time_seconds[10m])`).
- `node_filesystem_avail_bytes{mountpoint="/var/lib/docker"} < 10%`.
- `time() - container_last_seen > 60` for a container that should exist.
- Loki: `sum by (service) (rate({job="docker"} |= "panic" [5m])) > 0`.

## Verify
```bash
curl -s localhost:8080/metrics | grep container_memory_working_set_bytes | grep -v '^#' | head
curl -s 'localhost:9090/api/v1/query?query=up' | jq '.data.result[].metric.job'
logcli query --since 5m '{service="api"}' | head        # or Grafana Explore
docker run --rm --name canary alpine sh -c 'echo CANARY-LOG; sleep 1' && sleep 10 && logcli query '{container="canary"} |= "CANARY"'
```

## Checked

- Date: 2026-11-02.
- Confirmed against: cAdvisor run documentation (/dev/kmsg device), Compose labels com.docker.compose.project and .service, Prometheus docker_sd_configs and the Docker daemon metrics page.
- Not confirmed: the cAdvisor flags --docker_only, --housekeeping_interval, --store_container_labels, node_exporter --path.rootfs, and the Alloy discovery.relabel wiring (gated: unconfirmed, source is paywalled or blocked). Treat as unverified and check the current vendor documentation.

Method: documentation only; no commands were run.

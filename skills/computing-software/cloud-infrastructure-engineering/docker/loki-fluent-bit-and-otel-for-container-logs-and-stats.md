---
id: computing-software.cloud-infrastructure-engineering.docker.loki-fluent-bit-and-otel-for-container-logs-and-stats
name: loki-fluent-bit-and-otel-for-container-logs-and-stats
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, observability, log-shipping, loki, loki-driver, loki-docker-driver, fluent-bit, fluent-bit-input, otel-docker-stats, docker-stats-receiver, opentelemetry]
level: advanced
description: "Ship container logs with the Loki Docker driver or Fluent Bit (tail json-file or forward input), and collect container metrics with the OpenTelemetry docker_stats receiver."
sources: ["https://grafana.com/docs/loki/latest/send-data/docker-driver/", "https://docs.fluentbit.io/manual/pipeline/inputs/forward", "https://docs.fluentbit.io/manual/pipeline/inputs/tail", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/dockerstatsreceiver"]
status: gated
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Loki driver, Fluent Bit and OTel docker_stats

## Loki Docker logging driver
```sh
docker plugin install grafana/loki-docker-driver:3.7.0-amd64 --alias loki --grant-all-permissions
```
```json
{ "log-driver": "loki",
  "log-opts": { "loki-url": "https://loki.example.com/loki/api/v1/push",
                "loki-batch-size": "400", "loki-retries": "2", "loki-max-backoff": "800ms",
                "loki-timeout": "1s", "keep-file": "true", "mode": "non-blocking" } }
```
- Labels: `container_name`, `compose_project`, `compose_service`, `host`; add with
  `loki-external-labels` / `loki-pipeline-stages`.
- Known risk: if Loki is unreachable the driver can block container stop/start; use
  `mode=non-blocking`, low timeouts/retries, and `keep-file` so `docker logs` still works.
- Plugin must be installed on every host and upgraded with `docker plugin disable/upgrade`.

## Fluent Bit: tail json-file (no driver change)
```ini
[INPUT]
    Name              tail
    Path              /var/lib/docker/containers/*/*-json.log
    Parser            docker
    Tag               docker.*
    Refresh_Interval  5
    Mem_Buf_Limit     50MB
    DB                /fluent-bit/state/docker.db
[OUTPUT]
    Name   loki
    Match  docker.*
    Host   loki.example.com
    Labels job=docker
```
Run Fluent Bit as a container with `/var/lib/docker/containers:ro` and a state volume.
Container names aren't in the json-file; enrich via container `config.v2.json` or labels attrs
(`--log-opt labels=...` adds them to each line's `attrs`).

## Fluent Bit: forward input with the fluentd driver
```ini
[INPUT]
    Name   forward
    Listen 0.0.0.0
    Port   24224
```
```sh
docker run --log-driver fluentd --log-opt fluentd-address=127.0.0.1:24224 \
  --log-opt tag='docker.{{.Name}}' --log-opt fluentd-async=true --log-opt mode=non-blocking app:1
```
Gives container name/ID in records, but `docker logs` relies on dual logging cache.

## OTel Collector docker_stats receiver
```yaml
receivers:
  docker_stats:
    endpoint: unix:///var/run/docker.sock
    collection_interval: 15s
    container_labels_to_metric_labels: { com.docker.compose.service: service }
    metrics:
      container.cpu.utilization: { enabled: true }
exporters:
  otlphttp: { endpoint: https://otel-gateway.example.com }
service:
  pipelines:
    metrics: { receivers: [docker_stats], exporters: [otlphttp] }
```
Run `otel/opentelemetry-collector-contrib` with the socket mounted read-only (or via a
GET-only socket proxy). Emits CPU, memory, network, blkio per container.

## Verify
Loki: `{compose_service="api"}` returns lines in Grafana; Fluent Bit metrics endpoint
`:2020/api/v1/metrics` shows input/output counts; OTel: `container.memory.usage.total` arrives.

## Checked

- Date: 2026-11-02.
- Confirmed against: Loki driver install syntax with --alias loki --grant-all-permissions, loki-retries, loki-max-backoff, loki-timeout and keep-file behaviour (Grafana Loki Docker driver page). Corrected the plugin tag to the version the page shows.
- Not confirmed: loki-batch-size, loki-external-labels and loki-pipeline-stages option details and Fluent Bit Mem_Buf_Limit sizing (gated: unconfirmed, source is paywalled or blocked). Treat as unverified and check the current vendor documentation.

Method: documentation only; no commands were run.

---
id: computing-software.messaging-and-integration.ntfy.scale-tuning-metrics
name: scale-tuning-metrics
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, metrics, prometheus, health, tuning]
level: advanced
status: docs-checked
description: "Tune a busy ntfy server (cache batching, file descriptors) and expose Prometheus metrics, health and ready endpoints."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scaling and monitoring

## Tuning

```yaml
cache-batch-size: 25
cache-batch-timeout: "1s"
```

This is how ntfy.sh is tuned (defaults are 0, meaning synchronous writes). Batching is worth enabling if you see `database locked` messages in the logs. The same example sets `cache-startup-queries` with `pragma journal_mode = WAL;`, `pragma synchronous = normal;`, `pragma temp_store = memory;`, `pragma busy_timeout = 15000;` and `vacuum;`.

File descriptors: the systemd unit allows 10,000 by default. Override with `LimitNOFILE=20500`. Outside systemd use `ulimit -n` and `/etc/security/limits.conf`.

## Metrics

```yaml
enable-metrics: true
metrics-listen-http: "10.0.1.1:9090"
```

`metrics-listen-http` (a dedicated `[IP]:port`) implicitly enables metrics; when set, only that port serves `/metrics`, even with `enable-metrics`. Metrics may be sensitive, so secure the endpoint.

## Health

- `/v1/health` returns `{"healthy":true,"role":"active"}`; without clustering it is healthy whenever it answers.
- Load balancers should use `/v1/ready`, which returns `{"ready":true,"role":"active"}` and 200 only if the server should receive clients.

## Gotchas

- Watch `ntfy_db_pool_waits_total` and alert on `ntfy_db_up{role="primary"} == 0` with PostgreSQL.

## Checked

2026-11-04. Confirmed against the ntfy config page (Tuning for scale, Message cache, file descriptor limits, Health checks, Monitoring, db metrics). Removed: the one-writer claim and the Verify curls, not stated on the page.
Method: documentation only; no commands were run.

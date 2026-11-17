---
id: computing-software.database-administration.time-series-databases.prometheus-remote-write-receiver
name: prometheus-remote-write-receiver
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-prom-remote, prometheus-remote-write-receiver, prometheus]
level: practitioner
status: docs-checked
description: "Accept remote-written samples into a Prometheus server with the receiver flag, and use agent mode as the sender."
sources:
  - https://prometheus.io/docs/prometheus/latest/storage/
  - https://prometheus.io/docs/prometheus/latest/prometheus_agent/
  - https://prometheus.io/docs/prometheus/latest/command-line/prometheus/
  - https://prometheus.io/docs/prometheus/latest/configuration/configuration/
  - https://prometheus.io/docs/specs/prw/remote_write_spec/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remote write receiver

**Goal:** Accept remote-written samples into a Prometheus server (agent mode and receiver patterns).

## Steps
- Enable the receiver: start Prometheus with `--web.enable-remote-write-receiver` (default false); the endpoint is `/api/v1/write`.
- Message types: `--web.remote-write-receiver.accepted-protobuf-messages` lists the accepted messages (`prometheus.WriteRequest` by default, optionally `io.prometheus.write.v2.Request`).
- Agent mode (`--agent`) is a mode of the same binary that disables querying, alerting and local storage and keeps a customised WAL for remote write. Its data path is `--storage.agent.path` (default `data-agent/`). If the remote endpoint is unreachable it buffers on disk, limited to about two hours.
- A central Prometheus receiving from many agents stores everything it receives, so size it for the total series.
- Out-of-order samples are rejected unless `out_of_order_time_window` is set under `storage.tsdb` (default `0s`); with a window above zero, errors are combined into a single `too-old` error.
- The storage docs say local storage is not clustered or replicated, so a single receiver is a single point of failure for ingest.

**Gotcha:** The remote write spec says senders must retry on HTTP 5xx and must not retry on 4xx other than 429, so a receiver that wrongly returns 4xx for a temporary fault causes permanent data loss.

## Verify
- A test push returns a 2xx status (the spec requires 2xx on success).
- Pushed series are queryable on the receiver.

## Checked
2026-11-03. Confirmed against the storage page (receiver flag, `/api/v1/write`, not replicated), the command-line page (flag defaults, `--agent`, `--storage.agent.path`), the agent mode page (disabled features, two-hour buffer), the configuration reference (`out_of_order_time_window`) and the remote write 1.0 spec (2xx, 5xx/4xx retry rules). Resolved: `--enable-feature=agent` replaced by `--agent`. Removed: the "204" response, the Mimir/Thanos Receive/VictoriaMetrics recommendation, the reverse-proxy mTLS advice and "no multi-tenancy".
Method: documentation only; no commands were run.

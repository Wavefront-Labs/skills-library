---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-as-remote-write-receiver
name: prometheus-as-remote-write-receiver
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [enable-remote-write-receiver, prometheus-as-remote-write-receiver, remote-write, prometheus-agent, out-of-order-ingestion]
level: practitioner
status: verified
description: "Run Prometheus as a remote write target (--web.enable-remote-write-receiver) for agents and collectors: endpoint, protocol versions, auth and limits."
sources: ["https://prometheus.io/docs/prometheus/latest/feature_flags/", "https://prometheus.io/docs/prometheus/latest/querying/api/#remote-write-receiver", "https://prometheus.io/docs/specs/prw/remote_write_spec_2_0/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prometheus as a remote write receiver

## Enable
```bash
prometheus --web.enable-remote-write-receiver --config.file=prometheus.yml
```
Endpoint: `POST /api/v1/write` (snappy-compressed protobuf). Prometheus 3.15.1 accepted Remote Write 1.0 and 2.0 messages with just that flag (`--web.remote-write-receiver.accepted-protobuf-messages`, repeated once per message, restricts them).
Operator: `spec.enableRemoteWriteReceiver: true` (field present in the Prometheus Operator API reference).

## Sender side (agent or another Prometheus)
```yaml
remote_write:
  - url: https://central-prom.example.com/api/v1/write
    basic_auth: {username: edge, password_file: /etc/secrets/rw}
```
OTel Collector: the `prometheusremotewrite` exporter with the same URL (its README documents `translation_strategy`; `add_metric_suffixes` is deprecated there).

## What you do not get
- No relabeling on receive: samples are stored as sent (shape them on the sender with `write_relabel_configs`).
- No tenancy, no per-sender limits, no HA dedup: two senders writing the same series with different values at one timestamp conflict (`400 duplicate sample for timestamp ...; overrides not allowed`). Add a distinguishing external label on each sender.
- No auth by itself: put TLS/basic auth via `--web.config.file` or a proxy in front.

## Out-of-order
Pushed data can arrive late (sender retries). Set `storage: {tsdb: {out_of_order_time_window: 30m}}` in the config file (it is a config-file setting, not a flag) or rejected samples show as `prometheus_tsdb_out_of_order_samples_total` (`400 out of order sample`). See `tsdb-out-of-order-ingestion`.

## Monitoring the receiver
```promql
sum by (code) (rate(prometheus_http_requests_total{handler="/api/v1/write"}[5m]))
rate(prometheus_tsdb_head_samples_appended_total[5m])
```
4xx responses are permanent failures on the sender (a 415 was logged as `non-recoverable error` and the batch dropped); 5xx are retried.

## When to use something else
Many senders, multi-tenancy or HA pairs: use Mimir/Thanos Receive/Cortex instead of a single Prometheus receiver.

## Verify
- [ ] Sender's `prometheus_remote_storage_samples_failed_total` stays 0.
- [ ] Series from the sender are queryable with its external labels.

## Checked
Environment: Windows 11, Prometheus and promtool 3.15.1 (windows-amd64), Prometheus Operator API reference (main), jq 1.8.2.
- A scraping Prometheus with `remote_write` to a receiver started with only `--web.enable-remote-write-receiver`: 204 responses, `m1{sender="b"}` queryable on the receiver with the sender's external label; the receiver's `prometheus_http_requests_total{handler="/api/v1/write"}` counted `204`.
- A hand-built snappy-compressed protobuf write request (Python): in-order sample 204; older sample without an out-of-order window `400 out of order sample`; with `out_of_order_time_window: 30m` a 10-minute-old sample 204 and a 60-minute-old one `400 too old sample`; same timestamp and a different value `400 duplicate sample for timestamp ...; overrides not allowed`; same value 204.
- `prometheus_tsdb_head_samples_appended_total` exists on the receiver. The accepted-messages flag: `prometheus --help` and the error on a comma-separated value. The 415 case: see `remote-write-2-protocol`.
- `enableRemoteWriteReceiver` is a field in the Prometheus Operator API reference (not run, no cluster). The collector exporter name and `translation_strategy` note come from its README in opentelemetry-collector-contrib.

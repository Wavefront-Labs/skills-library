---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.troubleshooting-prometheus-remote-write
name: troubleshooting-prometheus-remote-write
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [remote-write-troubleshooting, remote-write-429, remote-write-lag, remote-write, queue-config-tuning, mimir]
level: advanced
status: docs-checked
description: "Diagnose remote write lag, 429/400 errors, dropped and retried samples, duplicate and out-of-order rejections using Prometheus remote storage metrics."
sources: ["https://prometheus.io/docs/practices/remote_write/", "https://prometheus.io/docs/prometheus/latest/configuration/configuration/#queue_config", "https://grafana.com/docs/mimir/latest/manage/mimir-runbooks/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting remote write

## Key metrics (per `remote_name`/`url`)
```promql
# lag in seconds: newest sample enqueued vs newest sent
# (prometheus_remote_storage_highest_timestamp_in_seconds is deprecated in favour of the queue_* metric)
prometheus_remote_storage_queue_highest_timestamp_seconds
  - prometheus_remote_storage_queue_highest_sent_timestamp_seconds
rate(prometheus_remote_storage_samples_failed_total[5m])     # non-recoverable errors (4xx other than 429): not retried
rate(prometheus_remote_storage_samples_retried_total[5m])    # recoverable errors (5xx, network; 429 only if retry_on_http_429): retried
prometheus_remote_storage_shards / prometheus_remote_storage_shards_max
prometheus_remote_storage_shards_desired
```

## Symptom table
| Symptom | Likely cause | Action |
|---|---|---|
| Lag growing, shards at max | receiver too slow or network bandwidth | check receiver latency; the docs say `max_shards` rarely needs to go above the default (50) unless the endpoint is very slow |
| Lag growing, shards low, retries high | receiver returning 5xx (or 429 with `retry_on_http_429: true`) | fix receiver; 429 means the receiver is rate limiting you |
| `samples_failed_total` rising | 400s: out of order, duplicate, too old, series/label limits | read Prometheus logs for the error body |
| Lag jumps after restart | WAL replay; queue resumes from WAL | expected; lag should drain |
| Lag > 2 hours | the WAL is compacted after 2 hours and unsent data is lost | fix quickly |

## Common 400/429 bodies from Mimir
`err-mimir-sample-out-of-order`, `err-mimir-sample-duplicate-timestamp`, `err-mimir-max-series-per-user`, `err-mimir-label-value-too-long`, `err-mimir-tenant-max-ingestion-rate`. Each has a runbook entry in the Mimir runbooks.

## 429 handling
Retry on HTTP 429 is controlled by `queue_config.retry_on_http_429`, documented as experimental with a default of `false`. The remote write 2.0 spec lets senders choose: they MUST retry 5xx, MAY retry 429, and MUST NOT retry other 4xx. Not retrying 429 means the throttled requests are lost.

## Gotchas
- Write relabeling that drops a label can create duplicates (two series collapse into one): out-of-order/duplicate errors follow.
- Large `batch_send_deadline` hides problems as lag; keep it at 5s default.

## Checked
2026-10-28. Confirmed in Prometheus source (`queue_manager.go`, `write.go`): metric names `queue_highest_timestamp_seconds`,
`queue_highest_sent_timestamp_seconds`, `samples_failed_total` (non-recoverable), `samples_retried_total` (recoverable),
`shards`, `shards_max`, `shards_desired`, and that `highest_timestamp_in_seconds` is deprecated. Configuration page:
`retry_on_http_429` default false, `batch_send_deadline` 5s, `max_shards` 50. Remote write tuning page: 2 hour WAL limit,
max_shards advice. Remote write 2.0 spec: 4xx/429/5xx retry rules. Mimir runbooks: error ids. Removed: the 2000-5000
batch advice, mixin alert name, `err-mimir-ingestion-rate-limited` (the runbook id is `err-mimir-tenant-max-ingestion-rate`),
HA-tracker explanation, agent-mode WAL claim, min_shards oscillation tip.
Method: documentation only; no commands were run.

## Verify
- [ ] Lag is near zero in steady state and you alert on sustained lag.
- [ ] `samples_failed_total` rate is 0.

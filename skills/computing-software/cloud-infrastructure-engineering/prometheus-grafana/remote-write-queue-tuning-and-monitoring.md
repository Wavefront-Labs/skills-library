---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.remote-write-queue-tuning-and-monitoring
name: remote-write-queue-tuning-and-monitoring
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, remote-write, queue-config-tuning, max-shards, batch-send-deadline, remote-write-metrics, remote-write-lag, mimir, thanos-receive]
level: advanced
status: docs-checked
description: "Tune remote_write queue_config (shards, capacity, max_samples_per_send, deadline, backoff) from the remote-storage metrics, and alert on lag and failed sends."
sources: ["https://prometheus.io/docs/practices/remote_write/", "https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remote write queue tuning and monitoring

## 1. How the queue works
Each `remote_write` entry tails the WAL and fans samples out to N **shards**; each shard buffers up to
`capacity` samples and sends a request when it has `max_samples_per_send` or `batch_send_deadline` expires.
Shard count autoscales between `min_shards` and `max_shards` from the observed send rate vs ingest rate.

```yaml
remote_write:
  - url: https://mimir.example.com/api/v1/push
    queue_config:
      capacity: 10000              # default 10000; per shard; docs recommend 3-10x max_samples_per_send
      max_shards: 50               # default 50; cap so the backend isn't stampeded
      min_shards: 1
      max_samples_per_send: 2000   # default 2000; raise only if the backend tolerates bigger batches
      batch_send_deadline: 5s      # flush partial batches after this
      min_backoff: 30ms            # default 30ms; doubles on every retry
      max_backoff: 5s              # default 5s; maximum retry delay
      retry_on_http_429: true      # default false (experimental); true also retries on 429
      sample_age_limit: 0s         # default 0s = send everything; >0 skips samples older than this
```
Shard memory is proportional to shards * (capacity + max_samples_per_send); the docs say the defaults keep it
under 2 MB per shard, and most users report about 25% more Prometheus memory after enabling remote write
(depends on series churn). Reduce `max_shards` when you raise `capacity` or `max_samples_per_send`.

## 2. Metrics to watch
```promql
# Lag: seconds between the newest enqueued sample and the newest sent sample
max by (remote_name, url) (
  prometheus_remote_storage_queue_highest_timestamp_seconds
  - prometheus_remote_storage_queue_highest_sent_timestamp_seconds)
# Desired vs max shards: pinned at max means the backend or network is the bottleneck
prometheus_remote_storage_shards_desired / prometheus_remote_storage_shards_max
# Failures and drops
rate(prometheus_remote_storage_samples_failed_total[5m])
rate(prometheus_remote_storage_samples_retried_total[5m])
rate(prometheus_remote_storage_samples_dropped_total[5m])
```

## 3. Tuning loop
| Symptom | Change |
|---|---|
| Lag grows, desired shards > max | raise `max_shards` if the backend has headroom; else fix backend latency |
| Lag grows, desired < max, high `sent_batch_duration_seconds` | raise `max_samples_per_send` (fewer, bigger requests) |
| Many 429s | backend tenant limit: raise ingestion_rate there, don't add shards |
| Memory spike | lower `capacity` or `max_shards` |
| Lag approaching 2 hours | after 2 hours the WAL is compacted and unsent data is lost |

## Gotchas
- Remote write reads from the WAL; if the endpoint stays down for more than 2 hours the unsent data is lost.
- Each `remote_write` destination starts its own queue, with its own shards and memory.
- If one shard backs up and fills its queue, Prometheus blocks reading from the WAL into any shard.

## Checked
2026-10-28. Confirmed on the Prometheus configuration page (`queue_config` fields and defaults: capacity 10000,
max_shards 50, min_shards 1, max_samples_per_send 2000, batch_send_deadline 5s, min_backoff 30ms, max_backoff 5s,
retry_on_http_429 default false and experimental, sample_age_limit 0s) and the Remote write tuning page (memory
formula, 2 MB per shard, ~25% memory, 3-10x capacity, 2 hour WAL limit, blocking behaviour). Metric names confirmed
in Prometheus source (`storage/remote/queue_manager.go`); `highest_timestamp_in_seconds` is deprecated there, so the lag
query uses `queue_highest_timestamp_seconds`. Fixed: `retry_on_http_429` default (was stated as true). Removed: 2000-5000
batch advice, 120 s and 60 s lag thresholds, the 2-3 h WAL window, the reload claim.
Method: documentation only; no commands were run.

## Verify
- [ ] Lag query stays near zero at peak.
- [ ] `samples_failed_total` and `samples_dropped_total` rates are 0.
- [ ] Desired shards stay below max with margin during peak ingest.

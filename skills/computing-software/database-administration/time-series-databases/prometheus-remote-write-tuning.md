---
id: computing-software.database-administration.time-series-databases.prometheus-remote-write-tuning
name: prometheus-remote-write-tuning
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-prom-remote, prometheus-remote-write-tuning, prometheus]
level: practitioner
status: docs-checked
description: "Tune remote_write queue_config (capacity, shards, batch size), drop series with write_relabel_configs and watch the 2-hour WAL limit."
sources:
  - https://prometheus.io/docs/practices/remote_write/
  - https://prometheus.io/docs/prometheus/latest/configuration/configuration/
  - https://prometheus.io/docs/specs/prw/remote_write_spec/
  - https://prometheus.io/docs/prometheus/latest/storage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remote write tuning

**Goal:** Ship samples to long-term storage reliably without overwhelming memory or network.

## Steps
```
remote_write:
  - url: https://remote-store.example.com/api/v1/push
    queue_config:
      capacity: 10000
      max_shards: 50
      max_samples_per_send: 2000
      batch_send_deadline: 5s
    write_relabel_configs:
      - source_labels: [__name__]
        regex: "go_.*"
        action: drop
```
- The values shown are the documented defaults. Each destination has a queue that reads from the WAL into shards, each of which sends requests to the endpoint.
- Failures are retried without data loss unless the endpoint stays down for more than 2 hours; after that the WAL is compacted and unsent data is lost.
- Set `capacity` to 3-10 times `max_samples_per_send`. Shard memory is proportional to shards * (capacity + `max_samples_per_send`); with the defaults it stays under 2 MB per shard. When raising capacity or batch size, consider lowering `max_shards`.
- Prometheus computes the number of shards automatically from incoming rate, unsent samples and send time, between `min_shards` (default 1) and `max_shards`.
- Remote write typically adds roughly 25 percent memory use per the tuning guide, and large series churn raises it further because of the per-series cache.
- Monitor `prometheus_remote_storage_samples_pending` to see if the server is falling behind; if so, check CPU and network saturation.
- Use `write_relabel_configs` to drop low-value series before sending (applied after external labels).
- Senders retry on HTTP 5xx with backoff (`min_backoff` 30ms doubling up to `max_backoff` 5s by default) and do not retry 4xx other than 429 (`retry_on_http_429` is experimental).
- The 2.0 protocol is selectable per destination with `protobuf_message: io.prometheus.write.v2.Request`; the default is `prometheus.WriteRequest`, and the 2.0 spec is documented as experimental in the storage docs.

**Gotcha:** If the remote end is down longer than 2 hours, unsent samples are lost to the remote even though they remain in local blocks.

## Verify
- `prometheus_remote_storage_samples_pending` stays low in normal operation.
- Receiver-side sample counts match what Prometheus ingested for the series you kept.

## Checked
2026-11-03. Confirmed against the Prometheus remote write tuning guide (queue flow, 2-hour limit, capacity advice, memory formula, 25 percent, pending metric), the configuration reference (queue_config defaults, write_relabel_configs, protobuf_message), the storage page (2.0 spec experimental) and the remote write 1.0 spec (retry rules). Resolved the "confirm" on protocol 2.0. Removed: other sample-lag metric names (`..._shards`, `..._failed_total`, highest-timestamp lag), the "under a minute" lag threshold, and the Mimir URL (now a placeholder).
Method: documentation only; no commands were run.

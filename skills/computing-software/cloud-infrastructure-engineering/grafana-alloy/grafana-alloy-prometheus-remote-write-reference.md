---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-prometheus-remote-write-reference
name: grafana-alloy-prometheus-remote-write-reference
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [prometheusremote-write, queue-config, wal, write-relabel-config, sigv4, out-of-order-samples, promtool-tsdb-dump]
level: advanced
status: docs-checked
description: "Tune prometheus.remote_write: WAL retention, endpoint defaults, queue_config sharding, metadata, native histograms, auth blocks, and diagnosing out-of-order samples."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/reference/components/prometheus/prometheus.remote_write.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# prometheus.remote_write reference

The component exports `receiver` and stores samples in a write-ahead log (WAL) before sending them.

## WAL
`truncate_frequency` 2h, `min_keepalive_time` 5m, `max_keepalive_time` 8h; segments are 128 MB. Data still in the WAL after an outage is replayed when the endpoint returns.

## endpoint defaults
- `remote_timeout` 30s, `send_exemplars` true, `send_native_histograms` false, `enable_http2` false.
- `protobuf_message` `"prometheus.WriteRequest"`; the experimental v2 value is `"io.prometheus.write.v2.Request"`.

## queue_config
```alloy
prometheus.remote_write "default" {
  external_labels = { cluster = "prod" }
  endpoint {
    url = "https://mimir.example.com/api/v1/push"
    queue_config {
      capacity             = 10000
      max_shards           = 50
      min_shards           = 1
      max_samples_per_send = 2000
      batch_send_deadline  = "5s"
    }
  }
}
```
Other defaults: `min_backoff` 30ms, `max_backoff` 5s, `retry_on_http_429` true, `sample_age_limit` 0s (disabled). `metadata_config` has `send` true, `send_interval` 1m, `max_samples_per_send` 2000.

## Blocks
`write_relabel_config` filters or rewrites series before sending; `sigv4`, `azuread` and `google_iam` authenticate to cloud backends; only one auth method per endpoint.

## Out-of-order errors
When the backend rejects samples as out of order, inspect the WAL with `promtool tsdb dump /path/to/wal-data` to look for the same series written by more than one Alloy instance scraping the same target, the most common cause on the page, and shut down instances that should not be running.

## Checked
2026-11-04: confirmed against the prometheus.remote_write reference page. Removed: the external_labels remedy for out-of-order errors (not on the page).
Method: documentation only; no commands were run.

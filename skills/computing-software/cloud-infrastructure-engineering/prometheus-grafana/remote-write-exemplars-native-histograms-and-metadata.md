---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.remote-write-exemplars-native-histograms-and-metadata
name: remote-write-exemplars-native-histograms-and-metadata
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [send-exemplars, metadata-config, remote-write, exemplar-storage, native-histograms, remote-write-2-protocol]
level: practitioner
status: docs-checked
description: "Send exemplars, native histograms and metric metadata over Prometheus remote write: per-endpoint flags, prerequisites and receiver support."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write", "https://prometheus.io/docs/prometheus/latest/feature_flags/#exemplars-storage", "https://grafana.com/docs/mimir/latest/send/native-histograms/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remote write: exemplars, native histograms, metadata

By default remote write sends only float samples. Each extra data type is opt-in per `remote_write` entry.

```yaml
remote_write:
  - url: https://mimir.example.com/api/v1/push
    send_exemplars: true              # default false; exemplar storage must be enabled (--enable-feature=exemplar-storage)
    send_native_histograms: true      # default false; a no-op (always true) with the 2.0 message
    metadata_config:
      send: true                      # RW 1.0 only; default true
      send_interval: 1m               # default 1m
      max_samples_per_send: 500       # default 2000
    protobuf_message: io.prometheus.write.v2.Request   # RW 2.0; default is prometheus.WriteRequest
```

## Prerequisites
- Exemplars: `--enable-feature=exemplar-storage` (experimental) and `max_exemplars` in the `exemplars` section under `storage` in the config file (default 100000, resizable at runtime). Targets must expose exemplars, which OpenMetrics supports.
- Native histograms: set `scrape_native_histograms: true` (default false, global or per scrape config) and use a receiver that stores them; Mimir documents this in its native histograms guide.
- Receivers: check your receiver's documentation for exemplar and native histogram support and any per-tenant limits.

## RW 1.0 vs 2.0
- 1.0 sends metadata in separate periodic requests controlled by `metadata_config`; 2.0 improves efficiency and sends metadata, start timestamp and native histograms by default. `metadata_config.send` is ignored with 2.0, where metadata is sent when `--enable-feature=metadata-wal-records` or `--enable-feature=type-and-unit-labels` is enabled.
- Consult your remote storage provider (or test) before switching `protobuf_message`; a receiver without 2.0 support may answer 415 (Unsupported Request Content).

## Monitoring
`prometheus_remote_storage_exemplars_total`, `prometheus_remote_storage_histograms_total`, the matching `*_failed_total` and `*_retried_total` counters per type, and `prometheus_remote_storage_metadata_total` (metadata counters apply to remote write 1.0 only).

## Gotchas
- Test against staging first: a 4xx reply is not retried, so a receiver that rejects exemplars or histograms can cost you the whole request.

## Checked
2026-10-28. Confirmed on the Prometheus configuration page (`send_exemplars`, `send_native_histograms`, `protobuf_message`,
`metadata_config` fields and defaults, `storage.exemplars.max_exemplars`, `scrape_native_histograms`), the exemplar-storage feature
flag page, the remote write 2.0 spec (4xx not retried) and Prometheus source (`queue_manager.go`: metric names, the
metadata-with-2.0 log message). Removed: Mimir `max_global_exemplars_per_user` and default-on claims, bandwidth/interning claim,
payload-size claim.
Method: documentation only; no commands were run.

## Verify
- [ ] Grafana panel with Exemplars toggled on shows exemplar dots from the remote store.
- [ ] Native histogram query (`histogram_count(rate(x[5m]))`) works on the receiver.

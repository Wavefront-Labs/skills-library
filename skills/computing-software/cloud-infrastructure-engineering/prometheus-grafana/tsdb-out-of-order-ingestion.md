---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.tsdb-out-of-order-ingestion
name: tsdb-out-of-order-ingestion
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, tsdb, out-of-order-ingestion, out-of-order-time-window, wbl, remote-write-receiver, otlp]
level: advanced
status: verified
description: "Accept late or out-of-order samples in Prometheus with tsdb.out_of_order_time_window: when it is needed, the cost, and how to confirm samples are no longer dropped."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/configuration/#tsdb", "https://prometheus.io/docs/prometheus/latest/storage/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Out-of-order ingestion

## When you need it
Ordinary scraping rarely produces out-of-order samples. You need it when Prometheus *receives* data:
`--web.enable-remote-write-receiver`, `--web.enable-otlp-receiver`, several agents writing the same series,
or edge devices that buffer and replay. Symptom without it:
`prometheus_tsdb_out_of_order_samples_total` rising and `err="out of order sample"` in logs or 400s to clients.

## Config
```yaml
storage:
  tsdb:
    out_of_order_time_window: 30m     # accept samples up to 30 min older than the newest in the head
```
Reload with SIGHUP or `/-/reload`; no restart needed. Samples older than (head max time - window) are still
rejected (`prometheus_tsdb_too_old_samples_total`).

## How it works
- OOO samples go to a separate in-memory chunk set backed by a write-behind log (`wbl/` in the data directory, created when the
  window is set; listed on the 3.15 storage page).
- The counters carry a `type` label (`float`, `histogram`): `prometheus_tsdb_out_of_order_samples_total{type="float"}` and the
  `histogram` variant exist in 3.15.1.

## Cost and sizing
- Keep the window as small as the real lateness: 10-30 min for agents with retry buffers; hours only for
  replays (prefer backfill with promtool for anything older).

## Gotchas
- Duplicate samples with the same timestamp and different values still fail (`duplicate sample for timestamp`).
- Recording rules evaluated before late data arrives will not be re-evaluated; their results stay wrong.
- Mimir uses the per-tenant `out_of_order_time_window` limit instead of this setting.

## Verify
- [ ] `rate(prometheus_tsdb_out_of_order_samples_total[5m])` is 0 after the change.
- [ ] `prometheus_tsdb_head_out_of_order_samples_appended_total` increases when late data arrives.
- [ ] Head memory (`process_resident_memory_bytes`) stays within budget for a day (not measured here).

## Checked
Environment: Windows 11, Prometheus and promtool 3.15.1 (windows-amd64), jq 1.8.2, Git Bash tar.
- Two receivers (`--web.enable-remote-write-receiver`), one with `storage.tsdb.out_of_order_time_window: 30m` and one without; samples sent as snappy protobuf from a Python script. Without the window: a sample older than the newest answered `400 out of order sample` and `prometheus_tsdb_out_of_order_samples_total{type="float"}` went to 2. With the window: a 10-minute-old sample was accepted (`prometheus_tsdb_head_out_of_order_samples_appended_total{type="float"}` 1, a `wbl/` directory appeared in the data path) and a 60-minute-old sample answered `400 too old sample` (`prometheus_tsdb_too_old_samples_total{type="float"}` 1). A same-timestamp different-value sample answered `400 duplicate sample for timestamp ...; overrides not allowed`. Reload without restart: `/-/reload` was used for other config changes; the setting sits under the runtime-reloadable `storage` block in the 3.15 configuration page.
- `--web.enable-otlp-receiver` and `--web.enable-remote-write-receiver` are listed by `prometheus --help`. Mimir's per-tenant `out_of_order_time_window` limit: Mimir configuration reference (`limits` block, default 0s).
- Removed unconfirmed statements about vertical compaction, Thanos compactor flags and memory scaling.

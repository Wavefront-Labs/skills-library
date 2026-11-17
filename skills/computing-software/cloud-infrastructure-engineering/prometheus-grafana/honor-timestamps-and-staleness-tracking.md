---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.honor-timestamps-and-staleness-tracking
name: honor-timestamps-and-staleness-tracking
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, scrape-config, timestamp-handling, track-timestamps-staleness, honor-timestamps, explicit-timestamps, staleness-markers, out-of-order, too-old-sample, cadvisor-timestamps, federation-timestamps, pca]
level: advanced
status: verified
description: "Handle targets that expose their own sample timestamps (cAdvisor, federation): honor_timestamps, track_timestamps_staleness so stale series vanish, and the out-of-order errors."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/configuration/#scrape_config", "https://prometheus.io/docs/instrumenting/exposition_formats/", "https://prometheus.io/docs/prometheus/latest/storage/#out-of-order-samples"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# honor_timestamps and staleness tracking

**Goal:** understand what happens when a scraped line carries its own timestamp
(`metric 42 1760522400000`) and choose the two flags that control it, so series neither
vanish early nor linger forever.

## 1. Who sends timestamps
Normal exporters don't; Prometheus stamps each sample with the scrape time. Sources that **do**: `/federate`
(original scrape times: `m0{...} 1 1792641710438` in a 3.15.1 response), exporters that expose their own collection time, the
Pushgateway only if clients push timestamps (it refuses them by default), and proxies that re-expose cached scrapes.

## 2. honor_timestamps
```yaml
scrape_configs:
  - job_name: federate
    honor_labels: true
    honor_timestamps: true      # default true: keep the exposed timestamp
```
- `true`: the sample is stored at the exposed time. Needed for federation to keep data aligned.
- `false`: the exposed timestamp is ignored and the scrape time used. Use this for a proxy that re-serves one old page
  repeatedly, otherwise every scrape writes the same (timestamp, value) pair and different values at one timestamp are
  rejected (`Error on ingesting samples with different value but same timestamp`, counter
  `prometheus_target_scrapes_sample_duplicate_timestamp_total`).

## 3. Staleness problem with explicit timestamps
Staleness markers (the thing that makes a series disappear soon after it stops being exposed) are not written for samples that
carried their own timestamp. Consequence in a test: a target that served `tsd 1 <now>` five times and then an empty page kept
`tsd` answering instant queries, while the same target with the option below returned nothing as soon as the page was empty.
```yaml
    track_timestamps_staleness: true   # default false; emit staleness markers even for timestamped samples
```
Added in Prometheus 2.48.0 (changelog: "Add configuration option for tracking staleness of scraped timestamps"). Set it on
federation jobs and any other job whose targets expose timestamps.

## 4. Errors you will see
Values observed on 3.15.1 (the counters are on the Prometheus server's own `/metrics`):
| Situation | Log / counter |
|---|---|
| exposed timestamp 3 h in the past | `Error on ingesting samples that are too old or are too far into the future`; `prometheus_target_scrapes_sample_out_of_bounds_total` rises |
| exposed timestamp 30 min ahead | same message and counter (5 and 15 minutes ahead were accepted) |
| older than the series' last sample, within the head | `out of order sample`; `prometheus_target_scrapes_sample_out_of_order_total` (an `out_of_order_time_window` combines this with out-of-bounds into `too old`) |
| same timestamp, different value | `Error on ingesting samples with different value but same timestamp`; `prometheus_target_scrapes_sample_duplicate_timestamp_total` rises |
Fixes: correct the source clock (NTP), use `honor_timestamps: false` for caching proxies, or enable out-of-order ingestion for
legitimately late data (`tsdb-out-of-order-ingestion`).

## Gotchas
- Pushgateway rejects pushed timestamps by default: `400 ... pushed metrics must not have timestamps`. Use a gauge holding the
  time as its value instead.
- A series whose last sample is timestamped keeps answering instant queries after it vanishes, until the 5 minute lookback ends,
  unless `track_timestamps_staleness` is on.

## Verify
- [ ] Federation jobs have `track_timestamps_staleness: true`.
- [ ] Removing a target's series makes it disappear within one scrape interval.
- [ ] The three `prometheus_target_scrapes_sample_*_total` counters are flat.

## Checked
Environment: Windows 11, Prometheus and promtool 3.15.1 (windows-amd64), client_golang 1.25.0 on Go 1.26, Pushgateway 1.11.4.
- A local server served: five timestamped samples then an empty page (two jobs, `track_timestamps_staleness` false and true), a sample 3 h old, samples 5, 15 and 30 minutes ahead, and a fixed timestamp with changing values. Results: with the option false `tsd` stayed queryable after the page went empty, with true it returned nothing; 3 h old and 30 min ahead were dropped with the log line above and `prometheus_target_scrapes_sample_out_of_bounds_total` 67 after about 30 s of scraping; 5 and 15 minutes ahead were stored; the fixed-timestamp job incremented `prometheus_target_scrapes_sample_duplicate_timestamp_total`. The counter names exist on a 3.15.1 server (the out-of-order one stayed 0).
- Out-of-order ingest sends: `400 out of order sample` without a window and `400 too old sample` beyond it (see `tsdb-out-of-order-ingestion`); the 3.15 configuration page says a window combines the two errors into `too-old`.
- Pushgateway 1.11.4 answered a pushed timestamped sample with `400` and `pushed metrics must not have timestamps`. `/federate` output carried explicit timestamps.
- `track_timestamps_staleness` default and meaning: 3.15 configuration page; the 2.48.0 changelog entry (prometheus CHANGELOG.md).
- Removed unconfirmed statements about cAdvisor, kube-prometheus defaults and a 10-minute future bound; cAdvisor itself was not run.

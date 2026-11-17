---
id: computing-software.cloud-infrastructure-engineering.observability.scrape-interval-and-resolution-cost-tradeoff
name: scrape-interval-and-resolution-cost-tradeoff
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [scrape-interval-cost, resolution-cost-tradeoff, observability-cost, scrape-interval, downsampling, prometheus]
level: practitioner
status: draft
description: "Choose scrape and evaluation intervals per job by weighing sample cost against alert latency and rate() window needs, with the arithmetic."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/configuration/#scrape_config", "https://prometheus.io/docs/prometheus/latest/querying/basics/#staleness", "https://grafana.com/docs/grafana-cloud/cost-management-and-billing/reduce-costs/metrics-costs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scrape interval vs cost

Samples per day per series = 86,400 / interval. Halving the interval doubles samples (ingest, storage, DPM billing), not series.

| Interval | Samples/series/day | Relative cost | Smallest safe rate() window |
|---|---|---|---|
| 10s | 8,640 | 3x | 40s |
| 15s | 5,760 | 2x | 1m |
| 30s | 2,880 | 1x | 2m |
| 60s | 1,440 | 0.5x | 4m |

Rule of thumb: rate windows need at least 4x the scrape interval (Grafana `$__rate_interval` does this).

## Choosing per job
- User-facing request metrics feeding fast-burn alerts: 15-30s.
- Node/infra and capacity metrics: 30-60s.
- Slow-moving inventory, cost, batch results: 60s-5m (stay at or under ~2m to avoid staleness gaps; the 5m lookback makes > 2m intervals fragile).
- Keep one interval per job; mixed intervals in one rule expression complicate windows.

## Configuration
```yaml
global: {scrape_interval: 30s, evaluation_interval: 30s}
scrape_configs:
  - job_name: api
    scrape_interval: 15s
  - job_name: kube-state-metrics
    scrape_interval: 60s
```
Long-term: downsample (Thanos 5m/1h) rather than scraping slowly.

## Gotchas
- Scrape interval > 2m: series go stale between scrapes (5m lookback with jitter) and graphs gap.
- Lowering the interval on a high-cardinality exporter can overload the target; check `scrape_duration_seconds`.
- Vendors billing per DPM charge directly by interval; billing per active series does not.

## Verify
- [ ] A per-job cost table (`sum by (job) (scrape_samples_scraped)` x samples per day) has been reviewed.
- [ ] Alert rules use windows >= 4x the job's interval.

---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.recovering-an-oom-looping-prometheus
name: recovering-an-oom-looping-prometheus
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus-oom-recovery, oom-loop, prometheus-memory, cardinality, wal-replay-recovery, prometheus-troubleshooting]
level: advanced
status: docs-checked
description: "Recover a Prometheus that OOMs during WAL replay after a cardinality explosion: raise limits temporarily, find the offender, cap it, and drop the WAL only as a last resort."
sources: ["https://prometheus.io/docs/prometheus/latest/storage/", "https://prometheus.io/docs/prometheus/latest/configuration/configuration/#scrape_config", "https://prometheus.io/docs/prometheus/latest/command-line/promtool/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recovering an OOM-looping Prometheus

Pattern: a target suddenly exposes millions of series, Prometheus OOMs, restarts, replays the WAL containing those series, and OOMs again.

## Steps
1. Stop the loop: temporarily raise the memory limit (pod limit / host) to let replay finish. Remove liveness probes that kill it during replay (use a startup probe).
2. Once up (even slowly), find the offender:
```promql
topk(10, count by (__name__) ({__name__=~".+"}))     # expensive; or:
topk(10, scrape_series_added)                          # targets adding series
```
or `curl -s localhost:9090/api/v1/status/tsdb | jq .data.seriesCountByMetricName`.
3. Cap it at the scrape:
```yaml
- job_name: offender
  sample_limit: 50000          # scrape fails (up=0) instead of ingesting the explosion
  metric_relabel_configs:
    - {source_labels: [__name__], regex: "bad_metric_.*", action: drop}
```
Reload. Fix the exporter/app (unbounded label).
4. Memory falls back after the next head compaction (every 2h) once the series stop receiving samples.

## If it cannot start at all
- Offline analysis of blocks: `promtool tsdb analyze /prometheus` (blocks only, not the WAL).
- Last resort: move `wal/` (and `chunks_head/`) aside and start. You lose up to ~2-3h of not-yet-compacted data. Keep the directory until you are sure.
- Agent/HA pair: the other replica has the data; restore from it via Thanos/Mimir.

## Prevention
- `sample_limit` and `label_limit` on every job; `target_limit`.
- `--auto-gomemlimit` (default true) sets `GOMEMLIMIT` from the container or system limit; `--auto-gomemlimit.ratio` defaults to 0.9. If the flag is unavailable, set `GOMEMLIMIT` yourself.
- Alert on `scrape_series_added` spikes per target.

## Checked
2026-10-31. Confirmed in the Prometheus docs: `sample_limit`, `label_limit` and `target_limit` (default 0 = no limit; an over-limit scrape fails), `scrape_series_added` and `scrape_sample_limit`, `/api/v1/status/tsdb` fields `headStats.numSeries` and `seriesCountByMetricName`, `promtool tsdb analyze`, blocks every two hours, `--auto-gomemlimit` and its 0.9 ratio. Removed: the head-series-created rate alert (metric not in the docs).
Method: documentation only; no commands were run.

## Verify
- [ ] `headStats.numSeries` from `/api/v1/status/tsdb` is back to baseline after the next compaction.
- [ ] Every job has a `sample_limit`.

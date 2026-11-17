---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.tsdb-backfilling-with-promtool
name: tsdb-backfilling-with-promtool
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, tsdb, backfilling, create-blocks-from-openmetrics, promtool-backfill, recording-rules-backfill, promtool]
level: advanced
status: gated
description: "Backfill historical data into Prometheus with promtool tsdb create-blocks-from openmetrics and create-blocks-from rules, then move blocks in safely."
sources: ["https://prometheus.io/docs/prometheus/latest/storage/#backfilling-from-openmetrics-format", "https://prometheus.io/docs/prometheus/latest/storage/#backfilling-for-recording-rules", "https://prometheus.io/docs/prometheus/latest/command-line/promtool/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backfilling the TSDB with promtool

## 1. From OpenMetrics text
Input must be OpenMetrics with explicit timestamps (seconds) and end with `# EOF` (a file without it fails: `data does not end with # EOF`, run). Use LF line endings: a CRLF file fails with `invalid metric type "gauge\r"` (run, hit when Python wrote the file on Windows). Native histograms and staleness markers cannot be backfilled this way (storage docs). The storage docs warn that data from the last 3 hours (the head block) is not safe to backfill.
```
# HELP legacy_orders_total Orders from the old system.
# TYPE legacy_orders_total counter
legacy_orders_total{shop="eu"} 1520 1696118400
legacy_orders_total{shop="eu"} 1544 1696118460
# EOF
```
```bash
promtool tsdb create-blocks-from openmetrics orders.om ./backfill-out \
  --max-block-duration=24h      # bigger blocks = fewer blocks, but each must fit in memory while building
promtool tsdb list ./backfill-out
```
- Samples must be sorted per series. Run: the tool does NOT fail on an out-of-order or duplicate-timestamp sample; it exits 0 and silently writes a block without it (input `5 @ t+60` then `4 @ t` gave one sample, `5 @ t` then `4 @ t` gave one sample, the first), so compare the `NUM SAMPLES` column of `promtool tsdb list` with your input count.
- Default block duration is 2 h (72 h of data gave 36 blocks, run), which can produce thousands of tiny blocks for a year of data; `--max-block-duration` is documented in the storage docs and accepted by the subcommand (it is not shown in `--help`): with `24h` the same data gave 5 blocks of 5.5 h, 17.5 h x 3 and 11.5 h, not day-aligned. Larger blocks have a retention cost: time-based retention keeps the whole block until its last sample expires (storage docs), and the docs advise against few large blocks on production instances.
- `--label=name=value` (repeatable) attaches labels to every imported series.

## 2. From recording rules (new rule, history needed)
```bash
promtool tsdb create-blocks-from rules \
  --start 2026-07-01T00:00:00Z --end 2026-10-15T00:00:00Z \
  --url http://prometheus:9090 \
  --eval-interval 60s \
  --output-dir ./rules-backfill \
  rules/slo.rules.yml
```
- Queries the live server over the range and writes the results as blocks (run against a local 3.15.1 server). `--end` defaults to 3 hours ago (`--help`).
- Rules that depend on other recording rules will NOT see backfilled values of those rules: run with `bf:up:sum` and `bf:up:dep: bf:up:sum * 2` in one group, only `bf:up:sum` got data (12 samples per job) and `bf:up:dep` was empty. The docs' workaround: backfill the base rules, move those blocks into the server's data dir so the API can see them, then backfill the dependent rules.
- Alerting rules: `--help` and the docs say they are ignored, but on 3.15.1 an `alert: BfAlert` / `expr: up == 1` rule in the file was imported like a recording rule, producing a series named `BfAlert` (value 1, 12 samples per job) in the blocks; no `ALERTS` series were written. Keep alerting rules out of the file you backfill.

## 3. Loading the blocks
1. Ensure the target server allows overlap (storage docs: the `--storage.tsdb.allow-overlapping-blocks` flag was only needed on v2.38 and below) or that ranges don't overlap existing blocks.
2. Copy or move `./backfill-out/*` into the data dir (same filesystem). Run: blocks copied into the data dir of a running 3.15.1 server were loaded within about a minute (the `storage.tsdb.block-reload-interval` default is `1m`), `prometheus_tsdb_blocks_loaded` changed, and the server logged `Overlapping blocks found during reloadBlocks` as a WARN, then compacted them (`Found overlapping blocks during compaction`). Or stop, move, start.
3. Backfilled data is subject to retention: a 2023 block placed in a server with the default 15d retention was logged `Deleting obsolete block` at startup and the data was gone; with `--storage.tsdb.retention.time=5y` it stayed and `count_over_time(legacy_orders_total[1d] @ 1696118460)` returned 2. Extend retention first.
4. Overlapping blocks are vertically compacted; expect a CPU/disk spike (not measured).

## Gotchas
- Backfilled blocks carry only the labels in the input (add `--label` for any external labels you rely on); that they are not remote-written, and the Mimir/Thanos routes (`mimirtool backfill`, `thanos tools bucket upload-blocks`), were not run here (gated: unconfirmed, source is paywalled or blocked).
- Don't backfill into a Prometheus sidecar-shipped to object storage without also uploading those blocks (gated: unconfirmed, source is paywalled or blocked; Thanos not run).

## Verify
- [ ] `promtool tsdb list` on the output shows the expected time range and sample count.
- [ ] After loading, `count_over_time(legacy_orders_total[1d] @ <old timestamp>)` returns data.
- [ ] `prometheus_tsdb_blocks_loaded` increased and no `overlapping blocks` error in logs.

## Checked
promtool and Prometheus 3.15.1 (windows-amd64) run locally: `create-blocks-from openmetrics` on the skill's sample (two samples, `promtool tsdb list`, `-r` human-readable), missing `# EOF`, CRLF input, out-of-order and duplicate-timestamp input (silently dropped), a 72 h file with default and `--max-block-duration=24h` (36 blocks vs 5), `create-blocks-from rules` against a live server (dependent rule empty, alert rule imported as a series), copying blocks into a running server (loaded in about a minute, overlap warning, vertical compaction), retention deleting a 2023 block at default 15d, and keeping it with 5y plus the `@` query. Docs read: storage.md and `--help` at 3.15.1. Not run: Mimir, Thanos, remote write, a year of data.

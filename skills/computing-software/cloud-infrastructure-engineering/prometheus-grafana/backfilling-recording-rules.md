---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.backfilling-recording-rules
name: backfilling-recording-rules
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [create-blocks-from-rules, rule-backfill, recording-rules, backfilling, promtool-backfill, tsdb]
level: advanced
status: gated
description: "Backfill history for new recording rules with promtool tsdb create-blocks-from rules, then move the blocks into Prometheus safely; limitations and checks."
sources: ["https://prometheus.io/docs/prometheus/latest/storage/#backfilling-for-recording-rules", "https://prometheus.io/docs/prometheus/latest/command-line/promtool/", "https://prometheus.io/docs/prometheus/latest/storage/#backfilling-from-openmetrics-format"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backfilling recording rules

A new recording rule only has data from when it was deployed. promtool can evaluate it over past data and write TSDB blocks.

## Steps
```bash
promtool tsdb create-blocks-from rules \
  --start 2026-09-01T00:00:00Z --end 2026-10-01T00:00:00Z \
  --url http://prometheus:9090 \
  --eval-interval 60s \
  --output-dir ./backfill \
  rules/new-rules.yml
```
- Queries the running Prometheus at `--url` for the source data over the range (run against a local 3.15.1 server; `--end` defaults to 3 hours ago, `--eval-interval` defaults to 60s, both per `--help`).
- Writes blocks to `--output-dir` (default `data/`).
Then move the blocks into the Prometheus data directory (`mv backfill/* /prometheus/`). Run: blocks copied into a running server were loaded within about a minute, overlap logged a WARN (`Overlapping blocks found during reloadBlocks`) and was vertically compacted. Overlapping blocks are allowed in current versions (the allow-overlap flag was only needed on v2.38 and below, storage docs).

## Limitations (docs)
- Alerting rules: the docs and `--help` say they are ignored, but on 3.15.1 an `alert:` rule in the file was imported like a recording rule and wrote a series named after the alert (value of its expression, 12 samples per job in the test), with no `ALERTS` series. Keep alerting rules out of the file.
- Rules depending on other recording rules being backfilled in the same run are not evaluated against the backfilled outputs (run: `bf:up:dep: bf:up:sum * 2` produced no data while `bf:up:sum` did); run them in separate passes, base rules first, moving the base blocks into the server's data dir so the API can see them (storage docs).
- Running the backfiller twice over overlapping ranges creates blocks with the same data each time, and an `interval` set in the rule group overrides `--eval-interval` (storage docs; not run).
- Blocks older than retention are deleted: a 2023 block in a default-retention server was logged `Deleting obsolete block` at startup (run).

## Safety
- Run against a replica, not the busiest server: the backfill issues range queries against `--url` (load not measured).
- Test on a copy first; keep the output until verified.
- A Thanos sidecar does not ship backfilled blocks by default; `--shipper.upload-compacted` or copying the blocks to the bucket yourself is the usual route (gated: unconfirmed, source is paywalled or blocked; Thanos not run).

## Verify
- [ ] Querying the rule over the backfilled range returns data with the expected eval interval spacing.
- [ ] Values match running the rule expression directly for a sample timestamp.

## Checked
promtool and Prometheus 3.15.1 (windows-amd64) run locally: `promtool tsdb create-blocks-from rules` against a live local server over a 13-minute window with a base rule, a dependent rule and an alerting rule in one group (log lines, `tsdb list`, queries on a server loaded with the blocks), copying blocks into a running server, retention deletion. Docs read: storage.md at v3.15.1 (backfilling for recording rules, limitations), `--help` for the flags. Not run: Thanos shipper, multiple overlapping backfill runs, `interval` precedence.

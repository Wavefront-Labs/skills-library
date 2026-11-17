---
id: computing-software.cloud-infrastructure-engineering.victoriametrics.victoriametrics-troubleshooting-ingestion-and-queries
name: victoriametrics-troubleshooting-ingestion-and-queries
category: computing-software
field: cloud-infrastructure-engineering
product: victoriametrics
tags: [troubleshooting, slow-inserts, high-churn, slow-queries, oom, query-tracing, zfs]
level: advanced
status: docs-checked
description: "Diagnose slow inserts, high churn, slow queries, out-of-memory errors, cluster instability and ZFS read corruption in VictoriaMetrics."
sources: ["https://docs.victoriametrics.com/victoriametrics/troubleshooting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Victoriametrics troubleshooting ingestion and queries

General: run a current release, remove flags you do not understand, check logs.

Unexpected results: simplify the query, check raw samples in vmui Raw Query or `/api/v1/export`, and run with query tracing. Gaps in plots: use `-search.minStalenessInterval=5m`. Stale results after backfilling: disable the cache (`-search.disableCache`, `nocache=1`). Partial cluster responses: `-search.denyPartialResponse` or `deny_partial_response=1`, and remove `-replicationFactor` from vmselect.

Slow inserts: if the `storage/tsid` cache miss rate stays above 5% for over 10 minutes, add memory or cut active series. Keep label order consistent, or fall back to `-sortLabels=true`. If churn exceeds active series, remove frequently changing labels like timestamp or session_id. For the `TooHighSlowInsertsRate` alert raise `-cacheExpireDuration` above the scrape interval. High GC CPU: try `GOGC=100` (default 30).

Slow queries: slow query log threshold is `-search.logSlowQueryDuration` (5s). Find them in vmui top queries, shorten lookbehind windows, avoid accidental subqueries and prefer `sum(rate(...))` over `rate(sum(...))`.

Out of memory: remove tuning flags, limit heavy queries, keep 50% free memory.

Cluster instability: rolling restarts raise load by about `100%/(N-1)`; use at least 8 vmstorage nodes; consider `-vmstorageDialTimeout`, `-rpc.handshakeTimeout` and `-search.maxQueueDuration` cautiously.

Disk usage: delete old snapshots; if `vm_data_size_bytes` shows indexdb above 0.5 of data, churn is high.

ZFS: mixing mmap reads with `mincore()` can corrupt reads; run with `--fs.disableMincore`.

## Checked

2026-11-03. Flags, endpoints, HTTP paths, defaults, limits and version gates were checked against the official VictoriaMetrics documentation pages cited in `sources` (docs.victoriametrics.com, fetched this batch) with a phrase-by-phrase comparison. No wrong claims were found; no claims were removed.

Method: documentation only; no commands were run.

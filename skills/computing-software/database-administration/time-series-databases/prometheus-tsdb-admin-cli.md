---
id: computing-software.database-administration.time-series-databases.prometheus-tsdb-admin-cli
name: prometheus-tsdb-admin-cli
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-prom-backup, prometheus-tsdb-admin-cli, prometheus]
level: practitioner
status: docs-checked
description: "Use the admin API and promtool tsdb for series deletion, OpenMetrics and rule backfill, dump, analyze and list."
sources:
  - https://prometheus.io/docs/prometheus/latest/querying/api/
  - https://prometheus.io/docs/prometheus/latest/command-line/promtool/
  - https://prometheus.io/docs/prometheus/latest/storage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# promtool tsdb admin

**Goal:** Use promtool and admin API for deletion, backfill and analysis.

## Steps
- Admin API (needs `--web.enable-admin-api`): delete series with `POST /api/v1/admin/tsdb/delete_series` (at least one `match[]`; optional `start` and `end`; omitting both clears all data for the matched series), for example `curl -X POST -g 'http://localhost:9090/api/v1/admin/tsdb/delete_series?match[]=up{job="old"}'`.
- Then `POST /api/v1/admin/tsdb/clean_tombstones` removes the deleted data from disk and cleans up tombstones, freeing space (returns 204 on success).
- Backfill from OpenMetrics: `promtool tsdb create-blocks-from openmetrics <input file> [<output directory>]` (default output `data/`), then move the blocks into the Prometheus data directory. Do not backfill the last 3 hours (the current head block). Native histograms and staleness markers are not supported.
- Rule backfill: `promtool tsdb create-blocks-from rules --start <time> --url http://localhost:9090 rules.yaml` (`--end` defaults to 3 hours ago; `--eval-interval` defaults to 60s). Alerting rules are ignored.
- Overlap with existing blocks needs `--storage.tsdb.allow-overlapping-blocks` only on Prometheus v2.38 and below. Backfilled data is subject to the server's retention.
- `promtool tsdb dump <db path>` dumps series and samples (`--format prom|seriesjson`, `--min-time`, `--max-time`, `--match`).
- `promtool tsdb analyze <db path>` analyzes churn, label pair cardinality and compaction efficiency.
- `promtool tsdb list -r <db path>` lists blocks with human-readable values. `create-blocks-from` is marked experimental.

**Gotcha:** Deletion marks data with tombstones and the data stays on disk until `clean_tombstones` runs; the delete endpoint also does not necessarily remove series metadata from metadata queries.

## Verify
- Deleted series no longer return in queries.
- Backfilled data appears once and is not duplicated (re-running the rule backfiller over overlapping times creates duplicate blocks).

## Checked
2026-11-03. Confirmed against the HTTP API page (admin endpoints, parameters, 204, metadata note), the promtool page (subcommands, flags, defaults, experimental marking) and the storage page (backfill limits, overlapping-blocks flag, tombstones). Removed: the "use block sizes under the compaction limit" advice and `tsdb bench` mention (replaced by exact list/dump/analyze), and the bare `/data` paths (replaced by `<db path>`).
Method: documentation only; no commands were run.

---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.tsdb-deleting-series-and-tombstones
name: tsdb-deleting-series-and-tombstones
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, tsdb, delete-series-api, tombstone-cleanup, admin-api, pii-removal, cardinality]
level: practitioner
status: verified
description: "Delete series from Prometheus with the admin delete_series API and reclaim disk with clean_tombstones; scope matchers safely and know what it does not remove."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/api/#delete-series", "https://prometheus.io/docs/prometheus/latest/querying/api/#clean-tombstones"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deleting series and cleaning tombstones

Use cases: a label leaked PII or a secret, a cardinality explosion bloated the TSDB, or a bad backfill.

## 1. Dry run the selector
```bash
curl -sG localhost:9090/api/v1/series --data-urlencode 'match[]={__name__="http_requests_total",user_email!=""}' \
  --data-urlencode start=2026-10-01T00:00:00Z | jq '.data|length'
```
Make sure the count is what you expect; deletion has no undo. (`/api/v1/series` answers from the index: a deleted series that
is still in the head kept being listed in 3.15.1 after deletion even though queries returned no samples.)

## 2. Delete
Requires `--web.enable-admin-api`.
```bash
curl -s -XPOST -g 'localhost:9090/api/v1/admin/tsdb/delete_series?match[]={__name__="http_requests_total",user_email!=""}&start=2026-10-01T00:00:00Z&end=2026-10-16T00:00:00Z'
# HTTP 204 on success
```
- Without `start`/`end` it deletes across all time.
- Multiple `match[]` params are ORed.
- Data is hidden immediately (tombstones), not removed from disk.
- With `out_of_order_time_window` > 0, samples that were ingested out of order and still sit in the head were not removed in a
  3.15.1 test (4 samples, `delete_series` without a time range, 3 remained queryable): check with `count_over_time` afterwards.

## 3. Reclaim disk
```bash
curl -s -XPOST localhost:9090/api/v1/admin/tsdb/clean_tombstones
```
Returns `204`. Per the API reference it removes the deleted data from disk and cleans the tombstones, which means rewriting blocks
that have them (free space and IO). Otherwise compaction applies tombstones eventually.

## What it does not do
- Does not stop new data: fix the instrumentation or add a `metric_relabel_configs` drop first.
- Does not remove data already remote-written to another system (use that system's own deletion mechanism).
- Does not touch snapshots or backups.
- Prometheus Operator: enable with `spec.enableAdminAPI: true` (a field in its API reference; switch it off afterwards).

## Verify
- [ ] An instant query and `count_over_time(<metric>[<range>])` over the deleted range return nothing.
- [ ] After `clean_tombstones`, disk usage (`prometheus_tsdb_storage_blocks_bytes`) decreases when blocks were affected.

## Checked
Environment: Windows 11, Prometheus and promtool 3.15.1 (windows-amd64), jq 1.8.2, Git Bash tar.
- A server with `--web.enable-admin-api`: `POST /api/v1/admin/tsdb/delete_series?match[]=...` returned `204`; with two `match[]` parameters both metrics were deleted (`ooo_test` and `dup_t` returned no samples); a scraped series with `end=<20 s ago>` lost its older samples (143 to 12 samples in `count_over_time`) and kept being scraped; `clean_tombstones` returned `204`.
- Not as the skill claimed: after deletion `/api/v1/series` still listed the series; with `out_of_order_time_window: 30m` remote-written samples that were out of order stayed queryable (4 before, 3 after an all-time delete of that series).
- Endpoint behaviour, the `start`/`end`/`match[]` parameters and the clean-tombstones description: 3.15 API reference. `prometheus_tsdb_storage_blocks_bytes` exists (0 on this fresh server, so the decrease was not observed). `enableAdminAPI` is a field of the Prometheus resource in the Operator API reference (not run).

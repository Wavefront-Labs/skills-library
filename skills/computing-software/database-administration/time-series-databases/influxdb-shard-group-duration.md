---
id: computing-software.database-administration.time-series-databases.influxdb-shard-group-duration
name: influxdb-shard-group-duration
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-influx-buckets-retention, influxdb-shard-group-duration, influxdb, flux]
level: practitioner
status: docs-checked
description: "Pick a shard group duration that matches retention so deletion is cheap and queries touch few shards."
sources:
  - https://docs.influxdata.com/influxdb/v2/reference/internals/shards/
  - https://docs.influxdata.com/influxdb/v2/reference/cli/influx/bucket/create/
  - https://docs.influxdata.com/influxdb/v2/reference/cli/influx/bucket/update/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shard group duration

**Goal:** Pick a shard group duration that matches retention so deletion is cheap and queries touch few shards.

## Steps
- Defaults: retention under 2 days gives 1h; between 2 days and 6 months gives 1d; over 6 months gives 7d.
- Set explicitly (OSS only): `influx bucket create -n b -r 365d --shard-group-duration 7d`, or change it with `influx bucket update`. It must be shorter than the retention period.
- Longer shard groups reduce shard count and file overhead for long retention; shorter ones speed up deletes and compaction of recent data.
- Aim for a shard group well under retention.
- Backfilling creates shards for past time ranges as needed, with temporarily lower write throughput; writes go to older shards that must first be uncompacted and are recompacted afterwards.

**Gotcha:** Data is deleted only when a whole shard group is past retention, so data can persist up to retention plus the shard group duration.

## Verify
- `influx bucket list` shows the retention period and shard group duration.

## Checked

2026-11-03. Confirmed in the shards internals page (default duration table, `--shard-group-duration` on create and update, must be shorter than retention, backfill behaviour) and the bucket create/update CLI pages (OSS only). Removed: the megabyte-per-shard guidance, the claim that a change affects only new shards, the open-file-handle claim and the shard-count verification.
Method: documentation only; no commands were run.


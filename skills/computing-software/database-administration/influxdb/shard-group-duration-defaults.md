---
id: computing-software.database-administration.influxdb.shard-group-duration-defaults
name: shard-group-duration-defaults
category: computing-software
field: database-administration
product: influxdb
tags: [shard, shard-group-duration, retention, precreation, compaction]
level: advanced
status: docs-checked
description: "Default shard group duration by retention period, the --shard-group-duration flag, shard precreation settings and why backfilling old data writes more slowly."
sources:
  - https://docs.influxdata.com/influxdb/v2/reference/internals/shards/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Shards hold encoded, compressed series data for a time range set by the shard group duration. In OSS a shard group typically contains a single shard.

Defaults from the bucket retention period:

| Retention | Shard group duration |
|---|---|
| less than 2 days | 1h |
| 2 days to 6 months | 1d |
| greater than 6 months | 7d |

Override with `--shard-group-duration` on `influx bucket create` or `influx bucket update`. It must be shorter than the bucket retention period. View it with `influx bucket list`.

Shard precreation: a service pre-creates shards for future time ranges only. Related options: `storage-shard-precreator-advance-period` and `storage-shard-precreator-check-interval`. When you backfill historical data, InfluxDB creates shards for past ranges on demand, which temporarily lowers write throughput.

Hot shards receive writes; once a shard stops receiving writes it is compacted into a cold shard.

## Checked

2026-11-08: confirmed against the Markdown source of the cited page in the InfluxData docs repository (read in full): default duration table, `--shard-group-duration` on create and update, the shorter-than-retention rule, precreation behaviour and both option names, hot and cold shards. Nothing removed.
Method: documentation only; no commands were run.

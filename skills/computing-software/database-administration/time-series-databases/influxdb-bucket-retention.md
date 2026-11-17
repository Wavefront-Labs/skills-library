---
id: computing-software.database-administration.time-series-databases.influxdb-bucket-retention
name: influxdb-bucket-retention
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-influx-buckets-retention, influxdb-bucket-retention, influxdb, flux]
level: practitioner
status: docs-checked
description: "Create and adjust buckets with a retention period so expired data is dropped automatically."
sources:
  - https://docs.influxdata.com/influxdb/v2/reference/cli/influx/bucket/create/
  - https://docs.influxdata.com/influxdb/v2/reference/cli/influx/bucket/update/
  - https://docs.influxdata.com/influxdb/v2/reference/internals/data-retention/
  - https://docs.influxdata.com/influxdb/v2/reference/cli/influx/delete/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bucket retention periods

**Goal:** Create and adjust buckets with a retention period so expired data is dropped automatically.

## Steps
- Create: `influx bucket create -n sensors -o myorg -r 30d`. Retention 0 keeps data forever.
- Update: `influx bucket update -i <bucket-id> -r 90d`. Data older than the new retention becomes eligible for deletion; the retention enforcement service runs every 30 minutes by default (`storage-retention-check-interval`). The minimum retention is one hour.
- List: `influx bucket list`.
- Data is deleted by whole shard group, once the group's entire time range is older than retention, and stays queryable until then. Data can therefore live up to retention plus the shard group duration.
- Use one bucket per retention need (raw 7d, hourly rollups 1y) rather than one bucket with delete calls.
- Delete by predicate exists (`influx delete --bucket b --start ... --stop ... -p 'host="x"'`; `--start` and `--stop` are required) but is not a substitute for retention.

**Gotcha:** The shard group duration must be shorter than the bucket retention, and data is only deleted when a whole shard group is past retention; check both numbers together.

## Verify
- `influx bucket list` shows the new retention.
- After the retention window plus one shard group duration, the oldest timestamp returned by a wide-range query advances.

## Checked

2026-11-03. Confirmed in the `influx bucket create`/`update` CLI pages (flags `-n`, `-o`, `-r`, `-i`, 0 is infinite, one-hour minimum), the data-retention internals page (30-minute check, whole-shard-group deletion, queryable until deleted, maximum persistence = retention + shard group duration) and the `influx delete` page. Removed: the claim that shortening retention drops data with no undo on a stated schedule, and the tombstone-cost claim.
Method: documentation only; no commands were run.


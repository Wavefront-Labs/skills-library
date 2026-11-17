---
id: computing-software.database-administration.influxdb.retention-enforcement-service
name: retention-enforcement-service
category: computing-software
field: database-administration
product: influxdb
tags: [retention, shard-group, retention-enforcement, storage-retention-check-interval]
level: advanced
status: docs-checked
description: "How the retention enforcement service deletes whole shard groups every 30 minutes, why expired data stays queryable, and how to compute how long data really persists."
sources:
  - https://docs.influxdata.com/influxdb/v2/reference/internals/data-retention/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The retention enforcement service removes data whose timestamps are older than the bucket retention period. By default it runs every 30 minutes; change the interval with the `storage-retention-check-interval` configuration option.

It deletes shard groups, not individual points, and only when the entire time range of the shard group is beyond the retention period. Consequences:

- Expired data stays queryable until the service removes the shard group.
- Persistence window: minimum `bucket-retention-period`, maximum `bucket-retention-period + shard-group-duration`.
- Example: retention `3d` with shard group duration `1d` deletes shard groups three to four days old on the next run.

Retention can be infinite or as short as one hour. Shard group duration defaults from retention (see the shard group skill) but can be set when creating or updating a bucket. View both values with `influx bucket list`.

## Checked

2026-11-08: confirmed against the Markdown source of the cited page in the InfluxData docs repository (read in full): 30-minute default and `storage-retention-check-interval`, shard-group deletion rule, queryable-until-deleted note, min/max persistence formula, the 3d/1d example, infinite or one-hour retention. Nothing removed.
Method: documentation only; no commands were run.

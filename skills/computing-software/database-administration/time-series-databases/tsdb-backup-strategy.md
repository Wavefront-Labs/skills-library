---
id: computing-software.database-administration.time-series-databases.tsdb-backup-strategy
name: tsdb-backup-strategy
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-gen-backup-ha, tsdb-backup-strategy]
level: practitioner
status: draft
description: "Define what you back up and how fast you can restore time-series data."
sources:
  - https://prometheus.io/docs/prometheus/latest/storage/
  - https://docs.timescale.com/
  - https://docs.influxdata.com/influxdb/v2/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Backup strategy

**Goal:** Define what you back up and how fast you can restore time-series data.

## Steps
- Decide RPO and RTO per data tier: raw telemetry may tolerate loss of a few hours; billing meters may not.
- Logical vs physical: logical (`pg_dump`, `influx backup`, `clickhouse-backup`) vs physical (snapshots, WAL archiving, volume snapshots).
- Metrics stores often rely on replication instead: dual writes, remote write to a durable store.
- Always back up configuration, dashboards, rules, and tokens separately.
- Keep an off-site copy in different failure domain; encrypt.
- Run restore drills quarterly into scratch instances and compare row counts.
- Back up rollups preferentially; raw can often be regenerated from the source.

**Gotcha:** Backups that have never been restored are assumed working; they often fail on version mismatch or missing extension.

## Verify
- Last successful restore test date is recorded.
- Backup age alert fires beyond the RPO.

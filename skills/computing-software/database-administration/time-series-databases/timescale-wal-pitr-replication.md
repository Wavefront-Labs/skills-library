---
id: computing-software.database-administration.time-series-databases.timescale-wal-pitr-replication
name: timescale-wal-pitr-replication
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-timescale-backup, timescale-wal-pitr-replication, timescaledb, postgresql]
level: practitioner
status: draft
description: "Use physical backups and streaming replicas for Timescale HA and point-in-time recovery."
sources:
  - https://docs.timescale.com/
  - https://www.postgresql.org/docs/current/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# WAL archiving and replicas

**Goal:** Use physical backups and streaming replicas for Timescale HA and point-in-time recovery.

## Steps
- Timescale works with standard PostgreSQL tools: `pg_basebackup`, pgBackRest, WAL-G, Barman.
- Enable `archive_mode = on` and `archive_command` (or pgBackRest) with `wal_level = replica`.
- Restore to a point in time with `recovery_target_time` in `postgresql.conf` plus `recovery.signal`.
- Streaming replicas serve read queries; use Patroni for automatic failover.
- Keep extension and server versions identical on replicas.
- Compressed data replicates as ordinary table data, so replica size matches primary.
- Test restores on a schedule and monitor archive lag.

**Gotcha:** A replica on a different timescaledb minor version can fail to replay WAL; upgrade replicas first and primary last.

## Verify
- A PITR restore to a chosen timestamp returns the expected last row.
- Replica `pg_stat_replication` lag is small.

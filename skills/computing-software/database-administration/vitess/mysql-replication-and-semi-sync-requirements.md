---
id: computing-software.database-administration.vitess.mysql-replication-and-semi-sync-requirements
name: mysql-replication-and-semi-sync-requirements
category: computing-software
field: database-administration
product: vitess
tags: [replication, semi-sync, gtid, row-based-replication, binlog-row-image, durability]
level: practitioner
status: docs-checked
description: "State the MySQL replication settings Vitess requires (RBR, GTID, binlog_row_image FULL) and how semi-sync with unlimited timeout protects against split brain."
sources:
  - https://vitess.io/docs/25.0/reference/features/mysql-replication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vitess requires row-based replication with GTIDs: `--binlog-row-format=ROW` and `--gtid-mode=ON`. Only `binlog_row_image=FULL` is supported by default; `NOBLOB` has been experimental since v17, and `--binlog-row-value-options=PARTIAL_JSON` is fully supported from v22 with MySQL 8.0 and later.

Semi-sync is strongly recommended for high availability and is governed by the keyspace durability policy. Vitess sets the semi-sync timeout effectively unlimited, so replication never falls back to asynchronous; this prevents split brain in a network partition, because if all replicas are verified stopped the old primary cannot be accepting writes. The pre-configured policies do not let `rdonly` tablets send ACKs, since rdonly tablets cannot be promoted.

The guarantee: on primary failure at least one other replica has every transaction reported to clients as completed, and from MySQL 5.7 every committed one. Recover by waiting for VTOrc or by manually promoting the replica farthest ahead with EmergencyReparentShard. So each shard needs at least 2 `replica` tablets plus the primary (3 initially of type replica), leaving an acker when one replica is down for an upgrade or reboot. Semi-sync does not guarantee a fresh read from replicas, since the relay log may be unapplied; only the primary gives up-to-date reads.

Schema rules: replicas must have the same schema and column order as the primary; `FLOAT` or `DOUBLE` in a primary key is unsupported; avoid schema changes during resharding.

## Checked

2026-11-04. Replication format, GTID and row-image requirements, semi-sync behaviour, replica minimum and schema considerations confirmed on the MySQL Replication page.

Method: documentation only; no commands were run.

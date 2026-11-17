---
id: computing-software.database-administration.replication-high-availability.replication-log-types
name: replication-log-types
category: computing-software
field: database-administration
product: replication-high-availability
tags: [database-administration, replication-high-availability, replication-log-types, statement-based-replication, wal-shipping, logical-replication, trigger-based-replication]
level: practitioner
status: draft
description: "Compare replication log types (statement-based, physical WAL shipping, logical row-based, trigger-based) by determinism, version coupling, filtering and overhead."
sources:
  - https://dataintensive.net/
  - https://www.postgresql.org/docs/current/different-replication-solutions.html
  - https://dev.mysql.com/doc/refman/8.4/en/replication-formats.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Replication log types

How a leader's changes are described to followers determines what can go wrong (Kleppmann, DDIA ch.5).

## Statement-based
Ships SQL statements (MySQL `binlog_format=STATEMENT`, legacy).
- Small logs for bulk updates.
- Non-deterministic functions (`NOW()`, `RAND()`, `UUID()`), auto-increment races, triggers and `LIMIT` without `ORDER BY` diverge replicas. MySQL marks unsafe statements and warns.
- Statements must run in the same order with the same effects; concurrency on the leader must be serialised on replay.

## Physical / WAL shipping
Ships storage-engine log records (PostgreSQL streaming replication, Oracle redo for Data Guard physical standby, SQL Server log shipping/AGs).
- Exact byte-level copy; replicates everything, including indexes and system catalogs.
- Tightly coupled to version and platform: replicas must run the same major version (blocks zero-downtime major upgrades).
- Cannot filter tables or replicate to a different schema.

## Logical (row-based)
Ships row images: inserted values, changed columns with keys, deleted keys (MySQL `binlog_format=ROW`, PostgreSQL logical replication/decoding, Debezium CDC, Oracle GoldenGate).
- Deterministic; decoupled from storage format, so cross-version (upgrades) and heterogeneous targets (warehouse, Kafka) work.
- Larger logs for bulk updates (one record per row; MySQL `binlog_row_image=MINIMAL` reduces).
- Needs primary keys / replica identity to locate rows; DDL often not replicated (PostgreSQL) and must be coordinated.

## Trigger-based
Triggers write changes to a log table that an external process ships (Slony, Bucardo, older pglogical-era tools, custom audit queues).
- Very flexible (filtering, transformation, multi-master conflict code).
- Highest overhead on the leader (write amplification) and more failure modes.

## Choosing
| Need | Type |
|---|---|
| HA standby, exact copy | Physical |
| Major-version upgrade, partial replication, CDC | Logical |
| Legacy MySQL with mostly deterministic workload | Mixed / row preferred |
| Custom transformation in-database | Trigger-based (last resort) |

## Verify
Check the format in use (`SHOW VARIABLES LIKE 'binlog_format'`, `wal_level`, `SELECT * FROM pg_publication`) and run a determinism test (statements with `NOW()`/`UUID()`) comparing leader and replica contents.

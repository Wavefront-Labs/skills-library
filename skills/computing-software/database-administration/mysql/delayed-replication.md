---
id: computing-software.database-administration.mysql.delayed-replication
name: delayed-replication
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, delayed-replication, source-delay, sql-delay, logical-corruption-protection, recovery-from-drop, start-replica-until]
level: practitioner
status: docs-checked
description: "Keep a MySQL replica deliberately hours behind with SOURCE_DELAY to recover from accidental DROP/DELETE, and roll it forward to just before the mistake."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/replication-delayed.html
  - https://dev.mysql.com/doc/refman/8.4/en/start-replica.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Delayed replication

**Goal:** a replica that is always N hours behind, so a fat-fingered `DROP TABLE` can be recovered in minutes instead of a full restore + PITR.

## Configure
```sql
STOP REPLICA SQL_THREAD;
CHANGE REPLICATION SOURCE TO SOURCE_DELAY = 3600 * 4;   -- seconds (4 h)
START REPLICA SQL_THREAD;
```
The IO thread still downloads events immediately (relay logs fill up: size disk accordingly); only the SQL thread waits: a transaction is not executed until at least the delay after its commit on the immediate source (the delay applies per transaction, not per event). `START REPLICA`/`STOP REPLICA` take effect immediately and ignore the delay; `RESET REPLICA` resets the delay to 0.

## Monitor
```sql
SHOW REPLICA STATUS\G
-- SQL_Delay: 14400
-- SQL_Remaining_Delay: seconds until the next event is applied (NULL when not waiting)
-- Replica_SQL_Running_State: Waiting until SOURCE_DELAY seconds after master executed event
```
The manual recommends the Performance Schema tables `replication_connection_status`, `replication_applier_status_by_coordinator` and `replication_applier_status_by_worker` for measuring lag (they carry `original_commit_timestamp` and `immediate_commit_timestamp`); `replication_applier_configuration.DESIRED_DELAY` and `replication_applier_status.REMAINING_DELAY` show the configured and remaining delay. Alert on lag well beyond the configured delay.

## Recovering from a mistake
1. Immediately `STOP REPLICA SQL_THREAD;` on the delayed replica (before the bad event's delay expires).
2. Find the bad transaction in the relay or source binlog (`mysqlbinlog` on relay logs or source binlogs) and get its GTID.
3. Apply up to just before it:
   ```sql
   START REPLICA SQL_THREAD UNTIL SQL_BEFORE_GTIDS = '3E11FA47-...:9811';
   ```
   (or `UNTIL RELAY_LOG_FILE='...', RELAY_LOG_POS=...`). Remove the delay temporarily for speed: `CHANGE REPLICATION SOURCE TO SOURCE_DELAY=0` with the SQL thread stopped.
4. Dump the affected table from the replica and load it into the source, or promote the replica.

## Gotchas
- Not a backup: delayed replicas share the source's corruption beyond the delay and do not cover hardware loss. Keep real backups.
- Never route reads to it or include it in failover candidates; exclude it explicitly in your failover tooling.
- Large delays with high write rates need relay-log space of (write rate x delay).

## Verify
Create and drop a test table on the source; it exists on the delayed replica until the delay passes, and `UNTIL SQL_BEFORE_GTIDS` stops exactly before the drop.

## Checked
Date 2026-11-01. Documentation release: MySQL 8.4 Reference Manual, Delayed Replication and START REPLICA.
Confirmed: SOURCE_DELAY semantics, per-transaction delay, START/STOP/RESET REPLICA behaviour, SQL_Delay, SQL_Remaining_Delay, Replica_SQL_Running_State text, DESIRED_DELAY and REMAINING_DELAY columns, UNTIL SQL_BEFORE_GTIDS and RELAY_LOG_FILE/RELAY_LOG_POS. Corrected the running-state string and the delay basis. Removed unconfirmed claims: Seconds_Behind_Source alert rule and the Orchestrator setting.
Method: documentation only; no commands were run.

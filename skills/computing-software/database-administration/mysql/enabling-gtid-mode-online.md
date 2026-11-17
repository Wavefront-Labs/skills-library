---
id: computing-software.database-administration.mysql.enabling-gtid-mode-online
name: enabling-gtid-mode-online
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, gtid-mode-online, gtid-mode, enforce-gtid-consistency, gtid, replication, online-migration]
level: practitioner
status: docs-checked
description: "Switch a running MySQL replication topology from file/position to GTIDs with no downtime: the OFF_PERMISSIVE/ON_PERMISSIVE steps, checks between them and rollback."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/replication-mode-change-online-enable-gtids.html
  - https://dev.mysql.com/doc/refman/8.4/en/replication-options-gtids.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enabling GTID mode online

Start with `gtid_mode` OFF on every server. It must move one step at a time on **every** server: `OFF -> OFF_PERMISSIVE -> ON_PERMISSIVE -> ON`. Each step is a `SET @@GLOBAL` (no restart). Add the final values to my.cnf.

## Step 0: find statements that break GTID consistency
On every server:
```sql
SET @@GLOBAL.enforce_gtid_consistency = WARN;
```
Run normal traffic (including batch jobs) for a full cycle; check the logs for GTID consistency warnings (for example `CREATE TEMPORARY TABLE` / `DROP TEMPORARY TABLE` inside transactions, or one transaction updating both transactional and nontransactional tables). Fix the application until no warnings appear.

## Steps
```sql
-- 1. every server
SET @@GLOBAL.enforce_gtid_consistency = ON;
-- 2. every server
SET @@GLOBAL.gtid_mode = OFF_PERMISSIVE;
-- 3. every server
SET @@GLOBAL.gtid_mode = ON_PERMISSIVE;
-- 4. every server: wait until no anonymous transactions remain in flight
SHOW GLOBAL STATUS LIKE 'Ongoing_anonymous_transaction_count';   -- must be 0, and replicas must have applied everything anonymous
-- 5. every server
SET @@GLOBAL.gtid_mode = ON;
```
Order within a step does not matter, but complete a step on all servers before starting the next. Before step 5, make sure all transactions generated up to step 4 have replicated to all servers, and wait until you no longer need old binary logs containing anonymous transactions (for example for point-in-time recovery): they cannot be used once `gtid_mode` is `ON`.

## Switch replication to auto-positioning
```sql
STOP REPLICA;             -- add FOR CHANNEL 'name' per channel on multi-source replicas
CHANGE REPLICATION SOURCE TO SOURCE_AUTO_POSITION = 1;
START REPLICA;
SHOW REPLICA STATUS\G     -- Auto_Position: 1, Retrieved/Executed_Gtid_Set advancing
```

## Make it permanent
```ini
[mysqld]
gtid_mode = ON
enforce_gtid_consistency = ON
```

## Backups and PITR afterwards
Take a new full backup after the change: older binlogs contain transactions without GTIDs and cannot be used after `gtid_mode = ON`.

## Rolling back
The procedure can be paused and resumed, or reversed by jumping to the matching step of the manual's "Disabling GTID Transactions Online" procedure.

## Gotchas
- Changes of `gtid_mode` can only be one step at a time (OFF_PERMISSIVE can go to OFF or ON_PERMISSIVE, not ON).
- Assigning GTIDs on the replica to anonymous transactions from a source that cannot enable GTIDs is a separate feature; use this procedure when you can enable GTIDs on the source.

## Checked
2026-11-01. Confirmed against the MySQL 8.4 pages "Enabling GTID Transactions Online" and "Global Transaction ID System Variables": step order, one-step rule, Ongoing_anonymous_transaction_count, binary-log note, auto-position statements with FOR CHANNEL, GTID-unsafe statement list. Removed: the 8.0.21 version note, the error message text, mysqlbinlog --skip-gtids, SET PERSIST advice and the hand-written rollback steps.
Method: documentation only; no commands were run.


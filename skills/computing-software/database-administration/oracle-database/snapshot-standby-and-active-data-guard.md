---
id: computing-software.database-administration.oracle-database.snapshot-standby-and-active-data-guard
name: snapshot-standby-and-active-data-guard
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle, oracle-database, data-guard, snapshot-standby, active-data-guard, read-only-standby, dml-redirection, test-on-standby, licensing]
level: advanced
status: docs-checked
description: "Use an Oracle physical standby for testing (snapshot standby) or read offload (Active Data Guard real-time query), with conversion commands, guarantees and licensing notes."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sbydb/managing-oracle-data-guard-physical-standby-databases.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/dgbkr/using-data-guard-broker-to-manage-switchovers-failovers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snapshot standby and Active Data Guard

**Goal:** get value from the standby (realistic test runs, read offload) without
losing its protection role.

## Snapshot standby: read-write test copy, then discard
The standby keeps **receiving** redo but stops applying it; you can write to it
freely; converting back flashes back all local changes and applies the
accumulated redo.
```
DGMGRL> CONVERT DATABASE 'orcl_stby' TO SNAPSHOT STANDBY;
-- run the release rehearsal / load test on orcl_stby
DGMGRL> CONVERT DATABASE 'orcl_stby' TO PHYSICAL STANDBY;
```
Without the broker: `ALTER DATABASE CONVERT TO SNAPSHOT STANDBY;`.
While it is a snapshot standby, **failover takes longer** (must convert and
apply all redo) and protection is reduced: keep a second standby if RTO matters.

## Active Data Guard: open read-only while applying
```sql
-- on the standby
ALTER DATABASE RECOVER MANAGED STANDBY DATABASE CANCEL;
ALTER DATABASE OPEN READ ONLY;
ALTER DATABASE RECOVER MANAGED STANDBY DATABASE DISCONNECT;
SELECT open_mode FROM v$database;   -- READ ONLY WITH APPLY
```
Real-time query for reports, plus DML redirection (`ADG_REDIRECT_DML=TRUE` sends
occasional writes to the primary).
Requires the **Active Data Guard option license** for every standby and primary
using it (see the Licensing Information guide).

## Gotchas
- Read consistency on the standby lags the primary: use `STANDBY_MAX_DATA_DELAY`
  per session to refuse queries on stale data.
- Services: create role-based services (`srvctl add service ... -role PHYSICAL_STANDBY`)
  so report connections follow the standby role after switchovers.

## Verify
`SELECT database_role, open_mode FROM v$database;` shows `SNAPSHOT STANDBY / READ WRITE`
or `PHYSICAL STANDBY / READ ONLY WITH APPLY`; `DGMGRL> SHOW CONFIGURATION` is SUCCESS
after converting back.

## Checked

2026-10-28. Confirmed against the cited Oracle documentation: ALTER DATABASE CONVERT TO SNAPSHOT STANDBY, READ ONLY WITH APPLY, ADG_REDIRECT_DML, STANDBY_MAX_DATA_DELAY, an Active Data Guard licence for real-time query features (Data Guard Concepts and Administration).

Removed or corrected: fast-recovery-area/restore-point side note, EE licensing statement, far sync / block repair / BCT feature list and the dba_feature_usage_statistics hint (not found in the cited pages).

Method: documentation only; no commands were run.

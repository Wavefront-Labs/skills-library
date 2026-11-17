---
id: computing-software.database-administration.oracle-database.resumable-space-allocation
name: resumable-space-allocation
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, resumable-space-allocation, resumable-timeout, dba-resumable, after-suspend-trigger]
level: practitioner
status: docs-checked
description: "Enable Oracle resumable space allocation so long loads suspend instead of failing on space errors, then monitor DBA_RESUMABLE, fix space and resume."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/managing-space-for-schema-objects.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/RESUMABLE_TIMEOUT.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resumable space allocation

A long load that dies on an out-of-space error rolls back everything. With resumable mode the statement
**suspends** on space errors, waits for you to fix the cause, then continues.

## What suspends a statement
An out of space condition, a maximum-extents condition, or a space quota exceeded condition: the conditions
that would signal an error for a non-resumable statement.

## Enable
A statement runs in resumable mode only if its session was enabled in one of two ways:
```sql
-- needs RESUMABLE_TIMEOUT set to a nonzero value system-wide
ALTER SESSION ENABLE RESUMABLE;
-- or give the timeout (seconds, nonzero) in the statement
ALTER SESSION ENABLE RESUMABLE TIMEOUT 7200;
```
`RESUMABLE_TIMEOUT` enables or disables resumable statements at system level (default 0). A database-level LOGON
trigger can also enable resumable and set the timeout for users' sessions.

## Monitor
When a statement suspends: the error is reported in the alert log, the Resumable Session Suspended alert is issued,
and any `AFTER SUSPEND` system-event trigger runs. A PL/SQL procedure can read the error data through the
`DBMS_RESUMABLE` package and the `DBA_RESUMABLE` / `USER_RESUMABLE` views.
```sql
SELECT * FROM dba_resumable;
```

## Fix and resume
Fix the error condition (add space, raise the quota). The suspended statement resumes automatically and the alert
is cleared. A suspended statement can be forced to throw its exception with `DBMS_RESUMABLE.ABORT()`, callable by a
DBA or by the user who issued the statement.

## Gotchas
- Suspending a statement suspends the transaction, so all transactional resources (locks included) are held
  through the suspend: alert quickly.
- If the error is not resolved within the timeout interval, the statement wakes up and returns the exception.
- A statement can be suspended and resumed multiple times.
- Resumable cannot be enabled remotely: over a database link, only the local instance is affected.

## Verify
Fill a small test tablespace with a resumable session: it suspends, appears in `dba_resumable`, and completes after
you add space.

## Checked
2026-11-01. Confirmed against the Oracle 19c Administrator's Guide (Resumable Space Allocation) and the
RESUMABLE_TIMEOUT reference: enabling forms, suspend conditions, suspend actions, auto-resume, ABORT, timeout
behaviour, locks held, no remote enabling, default 0. Removed as unconfirmed: specific ORA numbers, SQL*Loader and
Data Pump options, the RESUMABLE privilege, per-PDB setting, the alert-log message text, the DBMS_SYSTEM trigger
example and the DBA_RESUMABLE column list.
Method: documentation only; no commands were run.

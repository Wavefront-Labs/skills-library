---
id: computing-software.database-administration.oracle-database.undo-management-and-ora-01555
name: undo-management-and-ora-01555
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, oracle-tablespaces, undo-tablespace, undo-retention, ora-01555, snapshot-too-old, retention-guarantee, v-undostat, flashback-query]
level: advanced
status: docs-checked
description: "Size Oracle undo tablespaces and UNDO_RETENTION from V$UNDOSTAT, diagnose ORA-01555 snapshot too old, and decide when to guarantee retention."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/managing-undo.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/V-UNDOSTAT.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Undo management and ORA-01555

## How undo is used
Undo holds before-images for rollback, read consistency and Flashback Query.
`UNDO_RETENTION` (seconds) is a best-effort **minimum** target, enforced by the
auto-tuning algorithm; changing it matters mainly for Flashback features and Active Data Guard.
- Undo tablespace with **AUTOEXTEND**: the database tunes retention to somewhat longer than the longest-running
  active query. That may not be enough for Flashback operations; set `UNDO_RETENTION` to the longest expected
  Flashback operation or use a fixed-size undo tablespace.
- **Fixed-size** undo tablespace: the database tunes for the best retention the size and load allow, typically much
  longer than the longest query. Too small a size means DML failures and snapshot too old errors. Tuning uses 70% of
  the tablespace size, or the warning alert threshold (default 70%) if lower.
- Auto-tuning is not supported for LOBs: LOB undo lives in the segment, and unexpired LOB undo can be overwritten.

## ORA-01555 snapshot too old
A query needed an older version of a block whose undo was already overwritten. Causes:
1. Query runs longer than the effective retention (`V$UNDOSTAT.MAXQUERYLEN` vs `TUNED_UNDORETENTION`).
2. Undo too small for the change rate, so unexpired undo is stolen (`UNXPSTEALCNT`, `SSOLDERRCNT`).
3. Fetch-across-commit: a cursor loop that commits every N rows while reading the
   same table (the classic self-inflicted case).
```sql
SELECT begin_time, end_time, undoblks, maxquerylen, maxqueryid, tuned_undoretention,
       activeblks, unexpiredblks, expiredblks, unxpstealcnt, ssolderrcnt, nospaceerrcnt
FROM v$undostat ORDER BY begin_time DESC FETCH FIRST 48 ROWS ONLY;
```
`V$UNDOSTAT` has one row per 10-minute interval, 576 rows (4 days); older data is in `DBA_HIST_UNDOSTAT`.
`SSOLDERRCNT` counts ORA-01555 occurrences; `NOSPACEERRCNT` counts requests that found no free undo space
(fix: add space). `MAXQUERYLEN` is the longest query in seconds, used to estimate `UNDO_RETENTION`.
Fixes: make the query faster; stop committing inside the fetch loop; raise
`UNDO_RETENTION` above `MAXQUERYLEN` and size undo for it.

## Sizing
Use `UNDOBLKS` (undo blocks consumed per interval) to get the consumption rate and estimate the size needed:
```sql
SELECT MAX(undoblks / ((end_time - begin_time) * 86400)) AS peak_blks_per_s FROM v$undostat;
-- needed bytes = retention_seconds * peak_blks_per_s * db_block_size
```
```sql
ALTER SYSTEM SET undo_retention = 3600 SCOPE = BOTH;
```

## Retention guarantee
`ALTER TABLESPACE undotbs1 RETENTION GUARANTEE;` means the database never overwrites unexpired undo, even if
transactions fail for lack of space (the docs warn it can make multiple DML operations fail). Disabled by default;
`RETENTION NOGUARANTEE` turns it off. Check `DBA_TABLESPACES.RETENTION` (GUARANTEE, NOGUARANTEE or NOT APPLY).
Use only for Flashback Query / long-query requirements with ample space.

## Switching undo tablespace
`UNDO_TABLESPACE` is dynamic, so assign a new undo tablespace with `ALTER SYSTEM SET`:
```sql
CREATE UNDO TABLESPACE undotbs2 DATAFILE SIZE 20G AUTOEXTEND ON MAXSIZE 64G;
ALTER SYSTEM SET undo_tablespace = undotbs2 SCOPE = BOTH;
```

## Verify
- [ ] `SSOLDERRCNT` and `NOSPACEERRCNT` = 0 over the last week.
- [ ] `TUNED_UNDORETENTION` > longest query (`MAXQUERYLEN`) at peak.
- [ ] No batch code commits inside a cursor loop over the table it reads.

## Checked
2026-11-01. Confirmed against the Oracle 19c Administrator's Guide (Managing Undo) and V$UNDOSTAT reference:
UNDO_RETENTION as best-effort minimum, autoextend vs fixed-size tuning, the 70% rule, LOB limitation, retention
guarantee semantics and DBA_TABLESPACES.RETENTION values, V$UNDOSTAT columns, 10-minute rows, 576 rows over 4 days,
DBA_HIST_UNDOSTAT, UNDO_TABLESPACE being dynamic. Removed as unconfirmed: the 900-second default, 20% headroom,
DBMS_UNDO_ADV, ORA-30036 section and active-transaction query, alert log detail, rollback-segment drop check, RAC and
local-undo remarks, and the datafile resize example.
Method: documentation only; no commands were run.

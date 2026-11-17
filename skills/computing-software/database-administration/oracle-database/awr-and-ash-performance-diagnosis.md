---
id: computing-software.database-administration.oracle-database.awr-and-ash-performance-diagnosis
name: awr-and-ash-performance-diagnosis
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle, awr, ash, statspack, performance-tuning, wait-events, addm, v$active_session_history, dba_hist_snapshot, top-sql, licensing]
level: advanced
status: docs-checked
description: "Use AWR/ASH wait-event and top-SQL data to diagnose an Oracle performance regression against a real baseline, not a guess."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/tgdba/gathering-database-statistics.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/dblic/Licensing-Information.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Oracle AWR/ASH performance diagnosis — compare, don't guess

**Goal:** turn "the database feels slow" into a specific wait event and SQL
statement, by comparing two time windows instead of staring at one snapshot.

## 1. Licensing gate — check this first
AWR, ADDM, and ASH are part of the **Diagnostics Pack**, a separately licensed
Enterprise Edition option (19c Licensing Information: `DBA_HIST_*` views, `V$ACTIVE_SESSION_HISTORY` and `DBA_ADDM_*` views
are part of the pack, except `DBA_HIST_SNAPSHOT`, `DBA_HIST_DATABASE_INSTANCE`, `DBA_HIST_SNAP_ERROR`, `DBA_HIST_SEG_STAT`,
`DBA_HIST_SEG_STAT_OBJ`, `DBA_HIST_UNDOSTAT`). Running AWR reports or querying those views without the license is a
compliance issue, not just a technical one: confirm licensing before relying on AWR as your primary tool.
`CONTROL_MANAGEMENT_PACK_ACCESS` (`DIAGNOSTIC+TUNING`, `DIAGNOSTIC`, `NONE`) controls access. Statspack is the older
alternative for sites without the pack; confirm its licensing and installation steps in the Statspack documentation.

## 2. AWR: compare two periods, always
A single AWR report tells you what happened, not whether it's abnormal. Pull a
report for the bad window and a report for a known-good baseline (same workload
phase — compare Tuesday 2pm to Tuesday 2pm last week, not to 3am):
```sql
EXEC DBMS_WORKLOAD_REPOSITORY.CREATE_SNAPSHOT;
-- then
@?/rdbms/admin/awrrpt.sql     -- single instance
@?/rdbms/admin/awrrpti.sql    -- specific database instance (prompts for DBID and instance number)
@?/rdbms/admin/awrgrpt.sql    -- RAC global report for the local database
```
Or `awrddrpt.sql` for a direct diff report between two snapshot ranges — this is
the fastest path to "what changed" and is underused compared to running two
separate reports and eyeballing the diff.

## 3. Reading the Top 5 Timed Events / wait class section
This is where the actual bottleneck shows, not CPU%. Common signatures:
- **`db file sequential read`** dominant → single-block I/O, usually index lookups;
  high average wait time points at storage latency, not just volume.
- **`db file scattered read` / `direct path read`** → full scans or large multi-block
  reads; check if a plan regressed from an index scan to a full table scan.
- **`log file sync`** high → commit-time redo write latency; check log file
  placement/storage, or an app committing too frequently (commit batching helps).
- **`enq: TX - row lock contention`** → application-level blocking, not Oracle
  internals; find the blocking session via ASH, not AWR aggregates.
- **CPU time dominant with low wait** → the SQL itself needs tuning (bad plan,
  missing index), not infrastructure.

## 4. ASH for the "right now" / recent-minutes picture
```sql
SELECT sql_id, event, COUNT(*) 
FROM v$active_session_history
WHERE sample_time > SYSDATE - 10/1440
GROUP BY sql_id, event ORDER BY 3 DESC;
```
ASH keeps the history of recent session activity in memory; AWR collects ASH statistics into
`DBA_HIST_ACTIVE_SESS_HISTORY` (dropping a snapshot range purges the ASH data captured in it). It is much finer than
AWR's snapshot-interval aggregates. Use it to catch a short spike
that an hourly AWR snapshot would average away.

## 5. ADDM and its real value
ADDM analyses the AWR snapshots and generates findings ("SQL statement
consuming significant time", "I/O capacity issue") from the same AWR data, ranked
by estimated benefit. Useful as a triage starting point, but verify its
recommendations against the actual Top 5 events and SQL — ADDM sometimes
recommends infrastructure (more I/O capacity) when the real fix is a missing index
or a changed execution plan.

## 6. Plan changes without code changes
The single most common "it was fine yesterday" cause: a stats refresh or bind-peek
changed the plan for the same SQL text. Check `DBA_HIST_SQL_PLAN` /
`V$SQL_PLAN` for `plan_hash_value` changes on the suspect `sql_id` across the
window — a differing hash with no code deploy is the smoking gun. SQL Plan
Baselines or `DBMS_SPM` can pin a known-good plan while the stats issue is fixed
properly.

## Verify
- [ ] Diagnostics Pack licensing was confirmed (or another approach used instead).
- [ ] The report compares the bad window against a matching-workload baseline, not an arbitrary one.
- [ ] The Top 5 Timed Events wait class, not just CPU%, drove the diagnosis.
- [ ] A suspected SQL regression was checked for a `plan_hash_value` change over time.
- [ ] ADDM findings (if used) were cross-checked against the raw AWR/ASH data before acting.

## Checked
Date 2026-10-22. Oracle Database 19c Database Performance Tuning Guide (gathering database statistics),
Licensing Information User Manual, PL/SQL Packages Reference. Confirmed: Diagnostics Pack scope and the exempt
DBA_HIST views, awrrpt/awrrpti/awrgrpt/awrsqrpt descriptions, ADDM works from AWR snapshots, ASH data is collected by AWR,
CREATE_SNAPSHOT. Corrected: `awrrpti.sql` is the single-instance report for a named instance (RAC global is `awrgrpt.sql`).
Removed unconfirmed: Statspack "free/unlicensed" and `spcreate.sql`, ASH once-per-second sampling and flush detail.
Method: documentation only; no commands were run.

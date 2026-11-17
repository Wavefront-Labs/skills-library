---
id: computing-software.data-engineering.dbt.repairing-a-broken-snapshot
name: repairing-a-broken-snapshot
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, dbt-snapshots, snapshot-repair, duplicate-current-rows, snapshot-backup, time-travel, zero-copy-clone, scd-type-2, incident-recovery]
level: advanced
status: docs-checked
description: "Recover a corrupted dbt snapshot: diagnose duplicate current rows or mass invalidations, back up first, restore via time travel/clone, or dedupe and re-close versions with SQL."
sources:
  - https://docs.getdbt.com/docs/build/snapshots
  - https://docs.snowflake.com/en/user-guide/data-time-travel
  - https://docs.databricks.com/en/delta/history.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Repairing a broken snapshot

**Goal:** fix snapshot history after a bad run without losing the irreplaceable parts. Snapshots cannot be rebuilt from source: history only exists in the snapshot table.

## Typical breakages
| Symptom | Cause |
|---|---|
| Several current rows per key | Duplicate keys in source at snapshot time; concurrent snapshot runs |
| Every row closed at one timestamp | Hard-delete invalidation after an empty/partial source load |
| Burst of versions with no real change | `check_cols: all` with a noisy column; type/format change in source |
| Versions with `valid_from` in the future/past | Timezone change in `updated_at` |

## Step 0: stop and back up
Pause the job that runs `dbt snapshot`. Then copy the table:
```sql
create table snapshots.customers_snapshot_bak_20261016 clone snapshots.customers_snapshot;   -- Snowflake zero-copy clone; other platforms differ
create table snapshots.customers_snapshot_bak as select * from snapshots.customers_snapshot;  -- generic
```

## Option A: restore to before the bad run (fastest)
Snowflake: `create or replace table snapshots.customers_snapshot clone snapshots.customers_snapshot at (timestamp => '2026-10-15 23:00'::timestamp_ltz);`
Delta: `RESTORE TABLE snapshots.customers_snapshot TO TIMESTAMP AS OF '2026-10-15 23:00'`.
Then fix the cause and rerun the snapshot: changes since are recaptured as one version per key (intermediate changes are lost).

## Option B: surgical SQL repair
Remove versions created by the bad run and reopen the rows they closed:
```sql
-- 1. delete rows inserted by the bad run
delete from snapshots.customers_snapshot where dbt_valid_from = '<bad run ts>' and dbt_updated_at = '<bad run ts>';
-- 2. reopen versions the bad run closed
update snapshots.customers_snapshot set dbt_valid_to = null where dbt_valid_to = '<bad run ts>';
```
For duplicate current rows: keep the latest by `dbt_valid_from`, close the others with the next version's `valid_from` using a window (`lead(dbt_valid_from) over (partition by key order by dbt_valid_from)`).
Run in a transaction; compare row counts and current-row counts before committing.

## Prevent recurrence
- Uniqueness test on the source key before snapshotting (`dbt build` order: source tests then snapshot).
- Row-count guard against partial loads when using hard-delete handling.
- Never run two snapshot jobs concurrently on the same table (orchestrator concurrency 1).

## Verify
- [ ] One current row per key; no versions from the bad run remain.
- [ ] Backup table retained until the next successful snapshot run is validated.

## Checked

2026-10-28. Confirmed against: snapshots page (dbt_valid_from, dbt_updated_at), Snowflake Time Travel page (AT | BEFORE with CLONE), Databricks table history page (RESTORE TABLE ... TO TIMESTAMP AS OF, 7-day default retention). Removed (not confirmable in the fetched pages): BigQuery time-travel line, Databricks clone wording.

Method: documentation only; no commands were run.

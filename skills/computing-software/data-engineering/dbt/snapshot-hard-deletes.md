---
id: computing-software.data-engineering.dbt.snapshot-hard-deletes
name: snapshot-hard-deletes
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, dbt-snapshots, hard-deletes, invalidate-hard-deletes, new-record, dbt-is-deleted, deleted-records, scd-type-2]
level: advanced
status: verified
description: "Track rows deleted from a dbt snapshot source: hard_deletes ignore/invalidate/new_record, the dbt_is_deleted column, legacy invalidate_hard_deletes, partial-extract traps."
sources:
  - https://docs.getdbt.com/reference/resource-configs/hard-deletes
  - https://docs.getdbt.com/docs/build/snapshots
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Handling hard deletes in snapshots

**Goal:** when a record disappears from the source, history shows it ended (and optionally when it was deleted), instead of staying "current" forever.

## Options (dbt 1.9+ `hard_deletes`)
```yaml
snapshots:
  - name: customers_snapshot
    relation: source('crm', 'customers')
    config:
      unique_key: customer_id
      strategy: timestamp
      updated_at: updated_at
      hard_deletes: new_record          # ignore (default) | invalidate | new_record
```
| Value | Effect |
|---|---|
| `ignore` | Deleted rows stay current forever (default) |
| `invalidate` | Current version gets `dbt_valid_to` = snapshot time; no current row remains |
| `new_record` | Closes the current version and inserts a new row with `dbt_is_deleted = 'True'` (the string `'True'`/`'False'` on dbt-duckdb) that stays open (`dbt_valid_to` NULL or `dbt_valid_to_current`); if the key reappears, the marker row is closed and a new active version is added (checked) |
Before 1.9: `invalidate_hard_deletes: true` = `invalidate`; it still ran on 1.12.6 for existing snapshots, but cannot be combined with `hard_deletes` on one snapshot. The docs list dbt-postgres, bigquery, snowflake and redshift as supported adapters; all three modes also ran on dbt-duckdb. dbt does not migrate an existing snapshot when you switch options.

`new_record` is best for analytics: you can count deletions and see when they happened, and "current" queries filter `dbt_valid_to is null and dbt_is_deleted = 'False'`.

## The partial-extract trap
Delete detection compares the **whole** source relation to the snapshot. If the source only contains a recent subset (incremental extract, filtered view, a failed partial load), every missing key is treated as deleted. Before enabling:
- Snapshot only full-copy sources (complete table each load).
- Guard with a pre-check: fail the run if source row count drops more than X% versus the previous load (a singular test on the source or a `pre_hook` assertion).

## Soft deletes
If the source marks deletion with a flag (`is_deleted`, `deleted_at`), keep `hard_deletes: ignore` and include the flag in `check_cols`/timestamp updates: the deletion becomes an ordinary versioned change.

## Verify
- [ ] Delete a row from the dev source and snapshot: the current version is closed and (new_record) a deleted marker row exists.
- [ ] Simulate a truncated source load: the guard fails the run before the snapshot invalidates everything.

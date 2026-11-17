---
id: computing-software.data-engineering.dbt.choosing-what-to-snapshot
name: choosing-what-to-snapshot
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, snapshot-source-selection, snapshots, scd2, raw-layer]
level: practitioner
status: docs-checked
description: "Decide what to snapshot in dbt: snapshot raw sources early, avoid snapshotting marts, handle transformations upstream, and choose tables worth the history."
sources:
  - https://docs.getdbt.com/docs/build/snapshots
  - https://docs.getdbt.com/reference/snapshot-configs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# What to snapshot

**Goal:** capture history that cannot be recreated, with snapshots that do not break when logic changes.

## Rules
1. **Point snapshots at a source by default.** The snapshot `relation` can be a `source()` or a `ref()`; the documented example snapshots a source directly.
2. **Run snapshots frequently.** Snapshots are only useful if run regularly: schedule `dbt snapshot`, at least as often as the changes you care about.
3. Configure `snapshot_meta_column_names` or `dbt_valid_to_current` (v1.9+) rather than reshaping the output columns.
4. If you need a transformation (such as filtering or deduplication), define it in an ephemeral model and reference it in `relation`.



## Strategy choice
- `timestamp` is the recommended strategy: it needs one `updated_at` column and copes with columns being added or removed.
- `check` (with `check_cols`) when no reliable `updated_at` exists; the check columns must be kept in step with the source schema.
- `hard_deletes` accepts `ignore` (default), `invalidate` or `new_record`.

## Gotchas
- `unique_key` is how dbt matches rows, so it must really be unique; add a uniqueness test on the snapshotted source.
- Missed changes between snapshot runs are not captured, so schedule `dbt snapshot` regularly.

## Verify
Uniqueness test on `dbt_scd_id`, and at most one row per key with `dbt_valid_to` null (or the current sentinel).

## Checked

2026-10-25: dbt docs, current branch of dbt-labs/docs.getdbt.com (last commit 2026-10-23). Confirmed: Snapshot docs: `relation` may be a source or ref, ephemeral model for transformations, run snapshots regularly, timestamp strategy recommended, `check_cols` for check, `hard_deletes` values `ignore` (default), `invalidate`, `new_record`, `dbt_valid_to_current` and `snapshot_meta_column_names` (v1.9+), unique key must be unique, `dbt_scd_id` and `dbt_valid_to` meta columns. Removed unconfirmed rules about never snapshotting marts or event tables and about spurious history.

Method: documentation only; no commands were run.

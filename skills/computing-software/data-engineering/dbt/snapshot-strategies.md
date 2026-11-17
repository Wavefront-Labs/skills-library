---
id: computing-software.data-engineering.dbt.snapshot-strategies
name: snapshot-strategies
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, dbt-snapshots, snapshot-strategy, timestamp-strategy, check-strategy, check-cols, updated-at, scd-type-2, change-capture]
level: practitioner
status: verified
description: "Choose the dbt snapshot strategy: timestamp (updated_at) vs check (check_cols), their failure modes, snapshot cadence vs change frequency, and snapshotting sources not models."
sources:
  - https://docs.getdbt.com/docs/build/snapshots
  - https://docs.getdbt.com/reference/resource-configs/strategy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snapshot strategies

**Goal:** record the history of a mutable source table (type 2 SCD) without missing or inventing changes.

## Timestamp strategy (preferred when available)
```yaml
snapshots:
  - name: customers_snapshot
    relation: source('crm', 'customers')
    config:
      schema: snapshots
      unique_key: customer_id
      strategy: timestamp
      updated_at: updated_at
```
A row is a new version when `updated_at` is newer than the stored one. Cheap and precise **if** the source reliably bumps `updated_at` on every change.
Failure modes: source updates without bumping the timestamp (missed changes: a changed `segment` with the same `updated_at` created no new version when run); timestamps that move backwards or time-zone shifts.

## Check strategy
```yaml
    config:
      unique_key: customer_id
      strategy: check
      check_cols: ['email', 'segment', 'status']      # or 'all'
```
Compares column values to the current version. Use when there is no trustworthy `updated_at`. `dbt_valid_from` is the snapshot run time, not a source time (checked).
Failure modes: `check_cols: all` versions on irrelevant churn (`last_login_at`, sync metadata columns) -> table bloat; expensive comparison on wide tables; floating values or reformatting creating spurious versions. List the columns that matter.

## Cadence matters
A snapshot captures state **at run time**. Changes that happen and revert between runs are invisible; several changes collapse into one. If you need every change, use CDC (log-based) instead of snapshots, and model SCD2 from the change stream.

## Snapshot sources, not models
Snapshot raw/staging data close to the source; snapshotting a downstream model bakes current business logic into history and changes when logic changes. Clean up in a model built on top of the snapshot.

## Unique key
Must be truly unique in the source at snapshot time; duplicates create multiple current rows and corrupt history. Add a uniqueness test on the source key; composite keys worked as a list (`unique_key: [customer_id, email]`, run on dbt 1.12.6; version of introduction unconfirmed) or as a concatenated surrogate.

## Verify
- [ ] Update one row in dev source and run `dbt snapshot`: exactly one new version, old row closed (`dbt_valid_to` set).
- [ ] Run twice with no source change: no new versions.
- [ ] Test: one row per key where `dbt_valid_to is null`.

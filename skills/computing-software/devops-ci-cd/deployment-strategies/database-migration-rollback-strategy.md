---
id: computing-software.devops-ci-cd.deployment-strategies.database-migration-rollback-strategy
name: database-migration-rollback-strategy
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, database-change-management, rollback-migrations, roll-forward, down-migrations, expand-contract, liquibase-rollback, flyway-undo, point-in-time-recovery, backward-compatible-schema, destructive-changes]
level: advanced
status: docs-checked
description: "Plan database rollback: why roll-forward plus expand/contract beats down-migrations, when Liquibase rollback or Flyway undo is safe, and snapshots/PITR for destructive changes."
sources: ["https://docs.liquibase.com/commands/rollback/rollback-by-tag.html", "https://documentation.red-gate.com/fd/undo-184127450.html", "https://martinfowler.com/bliki/ParallelChange.html", "https://dora.dev/capabilities/database-change-management/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migration rollback strategy

## The core rule
**Make the app rollback-safe instead of making the schema rollback-able.** If every
migration is backward compatible with the previous app version, an incident is fixed by
rolling back the *app* only; the schema stays (it's a superset). Down-migrations are a
last resort.

## Expand / contract
| Release | Schema | App |
|---|---|---|
| N | add `email_normalized` (nullable), backfill | writes both, reads old |
| N+1 | - | reads new, writes both |
| N+2 | add NOT NULL / constraints | reads/writes new only |
| N+3 | drop old `email` column (contract) | - |
Rolling back from any release to the previous works because each schema state supports
both adjacent app versions. Destructive steps (drop/rename/type change) happen only once
the old code is fully gone and the rollback window has passed.

## When down-migrations are acceptable
- Pure additive changes nobody depends on yet (dropping a just-added empty column).
- Liquibase: changeSets can declare rollback logic, and Liquibase recommends writing it for every changeSet.
  ```bash
  liquibase tag release-1.41            # before update
  liquibase rollback-sql release-1.41   # review first
  liquibase rollback release-1.41
  ```
- Flyway: the `undo` command is a Flyway Teams feature (see its undo reference page); otherwise write a new forward migration.
- A down migration that drops a column the new code already wrote to **destroys data**.
  Roll forward instead: new migration fixing the problem.

## Destructive changes need a data plan
- Snapshot or verify point-in-time recovery (point-in-time recovery or a tested backup) before
  dropping columns/tables or mass updates; record the timestamp in the deploy log.
- Soft-delete first: rename table to `_deprecated_orders_20261016` or revoke grants for a
  week, then drop.
- Data backfills: keep a copy (`CREATE TABLE orders_backup_42 AS SELECT id, old_col ...`)
  for the affected rows.

## In the pipeline
- PR check: test that the **previous app version's** test suite passes against the new
  schema (run old image tests vs migrated DB). This mechanically enforces compatibility.
- Lint for dangerous statements (`DROP`, `RENAME`, `ALTER ... TYPE`, `NOT NULL` without
  default) with squawk (Postgres) or custom rules; require a label/approval to bypass.
- Rollback runbook states: app rollback command, whether schema needs anything, and the
  restore procedure + expected data loss window.

## Verify
In staging: deploy N+1, roll back the app to N with the schema left at N+1; smoke tests
pass. Practise a PITR restore quarterly and time it.

## Checked

2026-10-28. Confirmed: Liquibase docs (`liquibase rollback` to a tag, `rollback-sql` to review first, recommendation to write rollback logic for every changeset), Flyway undo reference (Flyway Teams feature), Fowler's Parallel Change page (expand and contract), DORA database change management page (application rollback without a database rollback), and squawk docs for linting. Removed: the Liquibase auto-generated rollback detail, the Flyway `U<version>` file naming and data-loss warning, and the RDS and `pg_basebackup` references.

Method: documentation only; no commands were run.

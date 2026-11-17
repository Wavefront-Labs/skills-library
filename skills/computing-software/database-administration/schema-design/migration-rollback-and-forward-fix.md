---
id: computing-software.database-administration.schema-design.migration-rollback-and-forward-fix
name: migration-rollback-and-forward-fix
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, schema-migration, expand-contract, migration-rollback, forward-fix, down-migration, transactional-ddl, irreversible-migration, deploy-safety]
level: advanced
status: draft
description: "Plan how to undo a schema migration: when down-migrations are safe, why destructive steps are made irreversible by design, transactional DDL, and forward-fix runbooks."
sources:
  - https://databaserefactoring.com/
  - https://martinfowler.com/articles/evodb.html
  - https://www.postgresql.org/docs/current/ddl-alter.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Migration rollback and forward-fix

**Goal:** every migration has a known recovery path before it runs, and no
rollback loses data.

## Classify each migration
| Kind | Example | Rollback |
|---|---|---|
| Additive | add nullable column, new table, new index | Down migration drops it: safe (data in it is new) |
| Data transform | backfill, split column | Reversible only if the old data still exists |
| Destructive | drop column/table, narrow type | **Not reversible**: data is gone; restore = backup/PITR |
Expand/contract makes destructive steps late and separate: by the time you drop
the old column, nothing has read it for a release, so you never need to roll it back.

## Transactional DDL
- PostgreSQL and SQL Server run most DDL in transactions: a failed migration
  rolls back atomically (except `CREATE INDEX CONCURRENTLY`, `ALTER TYPE ... ADD VALUE` before PG12, etc.).
- MySQL and Oracle auto-commit each DDL statement: a migration failing halfway
  leaves a half-applied schema. Keep one DDL per migration there, and make each
  idempotent (`IF NOT EXISTS` / check catalog first).

## Down migrations
Write them for additive steps and test them in CI (`up → down → up`). Don't
pretend: for destructive steps, make the down migration raise an error with a
pointer to the restore runbook rather than recreating an empty column.

## Prefer forward-fix in production
Rolling back a migration usually also means rolling back the app version; if new
code already wrote data in the new shape, the down migration can lose it. The
default incident response is a new migration that corrects the problem, deployed
through the same pipeline. Keep "roll back the app, leave the schema" possible by
keeping schema changes backward-compatible with the previous app version (N-1 compatibility).

## Before running a risky step
- Snapshot/backup or note the PITR timestamp (`pg_create_restore_point`).
- Rehearse on a production-sized copy to learn lock duration and runtime.
- Set `lock_timeout` / `lock_wait_timeout` so a blocked migration fails rather than queueing traffic.

## Verify
CI runs up/down/up on every additive migration; destructive migrations carry a
ticket reference to the restore runbook and the contract-phase date.

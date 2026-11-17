---
id: computing-software.database-administration.schema-design.zero-downtime-schema-migrations
name: zero-downtime-schema-migrations
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-migration, zero-downtime, expand-contract, backward-compatible, online-ddl, blue-green-deploy, column-rename, data-backfill, lock-contention]
level: advanced
status: draft
description: "Run schema migrations on a live, highly-available database without locking out writes, using the expand-contract pattern so old and new code can both run during rollout."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Zero-downtime schema migrations — expand/contract, and the deploy-overlap problem

**Goal:** change a live schema without a maintenance window, in a way that
survives the reality that old and new application code run simultaneously during
any rolling deploy.

## 1. The core constraint: two code versions run at once
During any rolling deploy, some instances run old code against the database at
the same moment others run new code — this is true even for a "fast" deploy. A
migration that changes a column's meaning or removes something the old code still
references **will** break requests served by the old instances, for the whole
deploy window, every time. The design must assume this overlap exists, not treat
it as an edge case.

## 2. Expand-contract (parallel change), the general pattern
1. **Expand**: add the new structure alongside the old (new column, new table)
   without touching/removing anything old code depends on. Deploy this alone;
   nothing breaks because nothing old changed.
2. **Migrate/backfill**: populate the new structure from existing data, and
   deploy application code that writes to **both** old and new (or reads from
   new, falls back to old) — this is the step most often skipped, causing data
   written during the overlap window to exist in only one place.
3. **Contract**: once all code reads/writes only the new structure and a backfill
   confirms no gaps, remove the old structure in a separate deploy. Never
   combine contract with expand in the same release — contract must only ship
   after 100% of traffic is confirmed on new code.

## 3. Applying the pattern: renaming a column, concretely
Never `ALTER TABLE ... RENAME COLUMN` directly on a live system with old code
still deployed — it breaks every old-code reference instantly. Instead: add the
new column, write a dual-write path (old code still writes old column; new code
writes both, or a trigger/application layer keeps them in sync), backfill
historical rows, deploy readers to use the new column, confirm, then drop the old
column in a later release. The "renamed" column effectively never gets an atomic
rename — it's an add, a sync period, and a drop.

## 4. Backfills on large tables: batch, don't lock
A single `UPDATE` touching every row of a large table holds locks and generates
massive WAL/undo/redo/binlog volume, can run for hours, and can bloat tables
(Postgres MVCC) or blow out a transaction log. Batch it: update in chunks (by
primary-key range, with a brief pause/sleep between batches) so each transaction
is small, replication lag stays bounded, and a stuck batch can be killed without
losing all progress. Tools exist per engine (`pt-online-schema-change`/`gh-ost` for
MySQL, `pg_repack`-style online rebuilds for Postgres) that automate exactly this
batching plus the lock-avoidance tricks.

## 5. Online DDL support varies a lot by engine and operation — check first
Not every DDL operation is actually online even on engines with "online DDL"
features: adding a NOT NULL constraint that must validate existing rows, adding a
unique constraint, or certain column type changes can still take a long-held lock
or rewrite the whole table under the hood even when the syntax looks identical to
an instant operation. Check the specific operation against the specific engine
version's documented behavior (see the postgres/mysql/sql-server locking skills
for engine-specific lock types) before assuming "it's just DDL" is cheap.

## 6. Rollback needs the same discipline
A migration rollback plan that only reverses the schema change, while forgetting
that application code (already rolled back) now expects the old shape, causes the
same overlap problem in reverse. Every migration needs a rollback story reviewed
with the same expand-contract thinking — not just "run the DOWN migration" as an
afterthought.

## Verify
- [ ] The migration is split into expand / migrate-backfill / contract as separate deploys, never combined.
- [ ] A dual-write or fallback-read path exists during the overlap window so no data is written to only one location.
- [ ] Backfills on large tables run in small batches with monitored lag, not one unbounded UPDATE/transaction.
- [ ] The specific DDL operation's lock behavior was checked against the engine/version in use, not assumed online.
- [ ] A rollback plan exists that accounts for old-code/new-schema and new-code/old-schema overlap, not just a reversed migration script.

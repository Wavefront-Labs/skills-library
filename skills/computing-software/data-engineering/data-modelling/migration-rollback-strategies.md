---
id: computing-software.data-engineering.data-modelling.migration-rollback-strategies
name: migration-rollback-strategies
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, migration-rollback, schema-migrations, expand-contract, backups]
level: advanced
status: draft
description: "Plan rollback for schema and data migrations: reversible down migrations, expand-contract so rollback is code-only, backups and clones, and when roll-forward is safer."
sources:
  - https://martinfowler.com/bliki/ParallelChange.html
  - https://docs.snowflake.com/en/user-guide/object-clone
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migration rollback strategies

**Goal:** every schema/data change has a tested way back, or a deliberate decision to roll forward only.

## Strategies
1. **Expand-contract (parallel change)**: add new structures alongside old, migrate readers/writers, remove old later. Rollback = redeploy previous application code; the database still supports it. Preferred for anything non-trivial.
2. **Down migrations**: each migration has an inverse script (`V12__add_col.sql` / `U12__add_col.sql` in Flyway Teams, `down` in Alembic/Rails). Only reliable for schema-only, lossless changes.
3. **Snapshot / clone before change**: warehouse zero-copy clone (Snowflake `CREATE TABLE t_bak CLONE t`, Delta `DEEP/SHALLOW CLONE`, Time Travel) or DB backup; rollback = swap back. Loses writes made after the change unless replayed.
4. **Roll forward**: fix with a new migration. Often safest when data has already been transformed and writes continued.

## What is not reversible
- Dropping columns/tables (data gone; only backups help).
- Lossy type changes (`varchar(100)` -> `varchar(50)`, float -> int).
- Data rewrites without a copy of before-values.
Do these only in the contract phase, after the new path has been stable.

## Rollback plan template
- Trigger conditions (errors, reconciliation failures, latency).
- Exact commands and owner; expected duration.
- Data written after the change: how it is preserved/replayed.
- Tested in staging with production-like data volume.

## Warehouse specifics
```sql
CREATE TABLE core.orders_pre_v12 CLONE core.orders;   -- Snowflake, instant
-- rollback
ALTER TABLE core.orders SWAP WITH core.orders_pre_v12;
```
Delta: `RESTORE TABLE main.core.orders TO VERSION AS OF 412`.

## Verify
Rehearse the rollback in staging: run migration, write some data, roll back, confirm the app works and data loss (if any) matches the plan.

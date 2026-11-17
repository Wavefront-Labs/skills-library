---
id: computing-software.qa-testing-engineering.test-automation.schema-migration-script-testing
name: schema-migration-script-testing
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [schema-migration-testing, database-migrations, flyway, liquibase, alembic, rollback-testing]
level: advanced
status: gated
description: "Test database schema migrations: apply on a production-like copy, verify up/down, data preservation, lock duration, backward compatibility and repeatable CI runs."
sources:
  - https://documentation.red-gate.com/fd
  - https://alembic.sqlalchemy.org/en/latest/
  - https://docs.liquibase.com/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Database schema migration script testing

**Goal:** every migration applies cleanly, keeps data correct, does not lock production tables for too long, and works with the app versions running before and after it.

## In CI on every change
- Start an empty DB of the production engine and version (Testcontainers or a service container), run all migrations from zero: `flyway migrate`, `liquibase update`, `alembic upgrade head`.
- Check schema drift: compare the migrated schema with the ORM model (`alembic check`: run, it prints `No new upgrade operations detected.` when in sync and fails with `New upgrade operations detected: [('add_column', ...)]` after a model change, and it requires `target_metadata` in `env.py`; Hibernate `validate` (gated: unconfirmed, source is paywalled or blocked); `prisma migrate diff` is documented in the Prisma CLI reference, not run).
- **Down/rollback** if supported: `alembic downgrade -1` then upgrade again (run on SQLite: upgrade, downgrade, upgrade all worked); Liquibase `rollback-count 1`. Flyway Community has no undo (Redgate: undo requires Teams or Enterprise, confirmed via search results rather than the docs page): test the forward fix script instead.
- **Checksums:** never edit an applied migration; Flyway `validate` fails on checksum mismatch (gated: unconfirmed, source is paywalled or blocked).

## On a production-like data copy (masked)
- Time each migration and observe locks (`pg_locks`, `SHOW PROCESSLIST`). On Postgres: `ALTER TABLE ... ADD COLUMN ... DEFAULT` with a non-volatile default stores the default in metadata and avoids a rewrite (PostgreSQL docs, ALTER TABLE notes; the exact version cut-over was not rechecked), but changes that rewrite the table, or `CREATE INDEX` without `CONCURRENTLY`, block writes (the CONCURRENTLY option is documented on the CREATE INDEX page; the blocking behaviour itself was not run, no Postgres server).
- Data checks: row counts before/after, backfilled columns populated, no truncation in type changes, constraints valid.
- Set `lock_timeout` in migrations so they fail rather than queue behind long transactions (PostgreSQL docs: it aborts a statement that waits too long for a lock).

## Compatibility (expand and contract)
During rolling deploys old and new app versions run together. Test: old app against the new schema (expand step), new app against the new schema; drop old columns only in a later release.

## Verify
Migrations run from zero and from the current production version in CI, timings on the data copy are within the maintenance budget, and old-app-on-new-schema smoke tests pass.

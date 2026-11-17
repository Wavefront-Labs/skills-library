---
id: computing-software.data-engineering.data-modelling.postgres-migrations-without-locking
name: postgres-migrations-without-locking
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, schema-migration, postgres-migration-locks, create-index-concurrently, not-valid-constraint, access-exclusive-lock, zero-downtime]
level: advanced
status: docs-checked
description: "Run Postgres schema migrations without blocking traffic: lock modes, CREATE INDEX CONCURRENTLY, NOT VALID constraints and safe column changes."
sources:
  - https://www.postgresql.org/docs/current/explicit-locking.html
  - https://www.postgresql.org/docs/current/sql-createindex.html
  - https://www.postgresql.org/docs/current/sql-altertable.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Postgres migrations without locking

**Goal:** DDL on busy tables never holds a heavy lock for long or waits indefinitely behind a long-running transaction.

## Lock facts (documented)
- ACCESS EXCLUSIVE conflicts with every lock mode and is the only mode that blocks a plain SELECT. Many forms of ALTER TABLE and ALTER INDEX take it, as do DROP TABLE, TRUNCATE, REINDEX, CLUSTER and VACUUM FULL.
- A transaction seeking a table-level or row-level lock waits indefinitely for conflicting locks (barring deadlock), so keep transactions short and bound how long a migration will wait. Retry the migration if it gives up.
- SHARE UPDATE EXCLUSIVE protects against concurrent schema changes and VACUUM but still allows reads and writes. CREATE INDEX CONCURRENTLY, VALIDATE CONSTRAINT and some ALTER TABLE forms use it.

## Safe patterns
| Change | Approach (as documented) |
|---|---|
| Add nullable column | `ADD COLUMN`: with no default or a non-volatile DEFAULT the value sits in table metadata and no table rewrite happens |
| Add column with volatile default (e.g. clock_timestamp()), stored generated or identity column | rewrites the whole table and indexes: avoid on big tables |
| Add NOT NULL | `SET NOT NULL` scans the whole table, unless a valid CHECK constraint proves no NULLs exist: add `CHECK (x IS NOT NULL) NOT VALID`, `VALIDATE CONSTRAINT`, then `SET NOT NULL` (scan skipped), then drop the check |
| Add index | `CREATE INDEX CONCURRENTLY`: cannot run inside a transaction block; only one concurrent build per table at a time; on failure it leaves an INVALID index (psql `\d` shows it) that still adds update overhead, so drop it and retry |
| Add foreign key or CHECK | `ADD CONSTRAINT ... NOT VALID`, then `VALIDATE CONSTRAINT` (takes SHARE UPDATE EXCLUSIVE) |
| Add unique constraint | build a unique index concurrently, then `ADD CONSTRAINT ... UNIQUE USING INDEX idx`; a unique concurrent build enforces uniqueness against others before it is ready |
| Rename column or table | RENAME only changes the name, no stored-data effect, but running app code that uses the old name breaks |
| Drop column | quick: the column is made invisible, not physically removed, and space is reclaimed gradually as rows update |
| Change column type | `ALTER COLUMN ... TYPE` may rewrite the table; rewriting forms are not MVCC-safe for concurrent snapshots, so prefer a new column and an expand-contract rollout |

Several ALTER TABLE actions in one statement combine scans or rewrites into one pass.

## Batched backfill
Update in bounded batches, committing per batch and watching replication lag, rather than one giant UPDATE (large transactions bloat the table and delay replication). The pages do not give a specific batch query.

## Verify
- [ ] Migration rehearsed in staging under load, watching for lock waits.
- [ ] No INVALID indexes left behind after a failed concurrent build (`\d` shows INVALID).

## Checked
Method: docs-only read on 2026-11-09 of explicit-locking, sql-createindex and sql-altertable via text extraction, using targeted searches of lock modes, ADD COLUMN, SET NOT NULL, NOT VALID/VALIDATE, USING INDEX, RENAME, DROP COLUMN and CONCURRENTLY sections (partial reads of three long pages). Removed because the pages do not state them: lock_timeout/statement_timeout settings, "new queries queue behind the ALTER", PG version numbers (11, 12), SKIP LOCKED backfill SQL, tool names (Flyway, Liquibase, squawk), and the logical replication/Debezium DDL notes. Dropped the lock_timeout and zero-downtime tags only where unsupported (kept others).

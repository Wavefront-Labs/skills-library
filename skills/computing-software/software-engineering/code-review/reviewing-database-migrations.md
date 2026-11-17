---
id: computing-software.software-engineering.code-review.reviewing-database-migrations
name: reviewing-database-migrations
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, specialised-review, migration-review, schema-changes, zero-downtime-migrations, table-locks, backfill, expand-contract, postgresql, mysql]
level: advanced
status: draft
description: "Review schema migrations for production safety: lock-taking DDL, compatibility with running code, backfill strategy, rollback, and engine-specific traps in PostgreSQL and MySQL."
sources: ["https://www.postgresql.org/docs/current/sql-altertable.html", "https://www.postgresql.org/docs/current/sql-createindex.html#SQL-CREATEINDEX-CONCURRENTLY", "https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-operations.html", "https://martinfowler.com/bliki/ParallelChange.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reviewing database migrations

**Goal:** catch the migration that locks a hot table for ten minutes or breaks the
currently deployed app version, before it reaches production.

## Questions for every migration
1. **Compatible with the code running during deploy?** Old and new app versions overlap.
   Dropping/renaming a column the old code reads, or adding NOT NULL without default
   that old code doesn't write, breaks it. Require expand/migrate/contract across releases.
2. **What locks does it take, for how long, on how big a table?**
3. **Is data backfill separated and batched?**
4. **Is it reversible, or is the down-path "restore from backup"?** Say which.
5. **Does it run in a transaction** (and can it - some DDL can't)?

## PostgreSQL traps
| Operation | Risk | Safer |
|---|---|---|
| `CREATE INDEX` | blocks writes for the build | `CREATE INDEX CONCURRENTLY` (outside a transaction; check for INVALID index on failure) |
| `ADD COLUMN ... DEFAULT x` | fine on PG 11+ (no rewrite) for non-volatile defaults | volatile defaults (`now()` is stable - ok; `random()`) rewrite |
| `ALTER COLUMN TYPE` | table rewrite + ACCESS EXCLUSIVE | new column + backfill + swap |
| `ADD CONSTRAINT ... FOREIGN KEY / CHECK` | validates under heavy lock | `NOT VALID` then `VALIDATE CONSTRAINT` separately |
| `SET NOT NULL` | full scan under lock | add `CHECK (col IS NOT NULL) NOT VALID`, validate, then SET NOT NULL (PG 12+ uses the check) |
| Any DDL | waits for ACCESS EXCLUSIVE behind long queries, blocking everyone queued after it | `SET lock_timeout = '3s'` and retry |

## MySQL / InnoDB traps
Check `ALGORITHM=INSTANT/INPLACE, LOCK=NONE` is possible for the operation (state it
explicitly so it fails instead of silently copying). Large table changes: gh-ost or
pt-online-schema-change. Watch replica lag during backfills.

## Backfills
- Batched (e.g. 1-10k rows per transaction) with throttling, resumable, idempotent.
- Not inside the schema migration transaction.
- Measure on a production-sized copy: time and lock behaviour.

## Also check
- Indexes for new foreign keys and new query patterns in the same PR.
- ORM-generated migrations doing unintended drops/recreates (renames detected as drop+add).
- Data migrations touching PII comply with retention/privacy rules.

## Verify
- [ ] Migration tested against a production-sized dataset with timings recorded in the PR.
- [ ] Each step is compatible with both the old and new application versions.

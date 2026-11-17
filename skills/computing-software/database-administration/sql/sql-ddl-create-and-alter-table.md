---
id: computing-software.database-administration.sql.sql-ddl-create-and-alter-table
name: sql-ddl-create-and-alter-table
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-ddl, create-table, alter-table, safe-schema-change, add-column]
level: practitioner
status: docs-checked
description: "Create and alter tables and indexes safely, including lock-aware ADD COLUMN and rename strategies."
sources: ["https://www.postgresql.org/docs/current/sql-altertable.html", "https://www.postgresql.org/docs/current/sql-createindex.html", "https://www.postgresql.org/docs/current/runtime-config-client.html", "https://www.sqlite.org/lang_altertable.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DDL

- `CREATE TABLE t (id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, name TEXT NOT NULL, created_at TIMESTAMPTZ NOT NULL DEFAULT now());` (PostgreSQL form; adapt types per engine).
- PostgreSQL `ALTER TABLE` takes an `ACCESS EXCLUSIVE` lock unless a form says otherwise; with several subcommands the strictest lock applies. Combining changes in one `ALTER TABLE` lets multiple scans or rewrites share one pass.
- `ADD COLUMN` with a non-volatile `DEFAULT` (or none) stores the default in metadata and does not rewrite the table, so it is very fast on large tables. A volatile default (such as `clock_timestamp()`), a stored generated column, an identity column, or a domain type with constraints rewrites the whole table and its indexes.
- `ADD CHECK` or `SET NOT NULL` scans the table but does not rewrite it. `SET NOT NULL` skips the scan if a valid `CHECK` constraint already proves no NULLs exist. For large tables add the constraint `NOT VALID` (no scan; new writes are checked), then `VALIDATE CONSTRAINT`, which takes only a `SHARE UPDATE EXCLUSIVE` lock.
- Changing a column type normally rewrites the table and indexes (exception: a binary-coercible change with an unchanged `USING` result, where only some index rebuilds remain). Rebuilds can take a long time and need up to double the disk space temporarily. Use expand/contract: add the new column, dual write, backfill in batches, switch reads, drop the old one.
- Create indexes without blocking writes: PostgreSQL `CREATE INDEX CONCURRENTLY` builds without locks that prevent inserts, updates or deletes, whereas a standard build blocks writes (not reads). It has caveats; a failed concurrent build leaves an invalid index, to be dropped and retried (or rebuilt with `REINDEX INDEX CONCURRENTLY`). To add a unique constraint without long blocking, build `CREATE UNIQUE INDEX CONCURRENTLY` first and then convert it with `ADD CONSTRAINT ... USING INDEX`.
- Set `lock_timeout` in the session that runs DDL: it aborts a statement that waits too long for a lock (default 0 = off, units default to milliseconds). The PostgreSQL docs advise against setting it globally in `postgresql.conf`.
- Renames break clients; add a view or do expand/contract.
- Keep migrations in version control and apply them in order with a migration tool; do not hand-edit production.
- SQLite supports a limited `ALTER TABLE`: rename table, rename column, add column, drop column. `ADD COLUMN` cannot add a PRIMARY KEY or UNIQUE column, cannot default to `CURRENT_TIMESTAMP` or a parenthesised expression, a NOT NULL column needs a non-NULL default, and a stored generated column is not allowed (virtual is). Renames and plain column additions only edit the stored schema text, so they take the same time on any table size. Anything else needs a table rebuild (see twelve-step-table-rebuild).

## Checked

2026-11-08. Read: PostgreSQL `ALTER TABLE` (description, `ADD COLUMN`/`SET NOT NULL`/`ADD CONSTRAINT`/`VALIDATE CONSTRAINT`, Notes on rewrites and `NOT VALID`), `CREATE INDEX` `CONCURRENTLY` text, `lock_timeout` entry in client connection defaults, SQLite ALTER TABLE page sections 1-5. Removed unconfirmed claims: PostgreSQL 11 and MySQL 8 INSTANT version statements, SQL Server `ONLINE = ON`, MySQL online DDL, the claim that a queued ALTER blocks sessions behind it, and the named migration tools.
Method: documentation only; no commands were run.

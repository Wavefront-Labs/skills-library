---
id: computing-software.database-administration.sql.bulk-load-speed-tuning
name: bulk-load-speed-tuning
category: computing-software
field: database-administration
product: sql
tags: [sql, bulk-load-speed-tuning]
level: advanced
status: docs-checked
description: "Speed up a large PostgreSQL load with one transaction, COPY, deferred indexes, larger maintenance_work_mem and max_wal_size, and a final ANALYZE."
sources: ["https://www.postgresql.org/docs/current/populate.html", "https://www.postgresql.org/docs/current/sql-createtable.html", "https://www.sqlite.org/pragma.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bulk load speed tuning

- Turn off autocommit and load in one transaction (or use `COPY`, which is a single command). Per-row commits cost a lot of work per row.
- `COPY` is almost always faster than INSERT, even with prepared statements and batching.
- Create the table, `COPY` the data, then create indexes: building an index on existing data is quicker than updating it per row. When adding to an existing table, consider dropping and recreating indexes, but a dropped unique index loses its checking.
- Foreign keys can be dropped and re-added for the same reason; loading millions of rows into a table with foreign keys can overflow the trigger event queue.
- Temporarily raise `maintenance_work_mem` (helps CREATE INDEX and ADD FOREIGN KEY, not COPY) and `max_wal_size` (fewer checkpoints).
- COPY in the same transaction as the CREATE TABLE or TRUNCATE writes no WAL, but only when `wal_level` is `minimal`. Changing `wal_level`, `archive_mode` or `max_wal_senders` needs a restart.
- An `UNLOGGED` table is not written to WAL; it is truncated after a crash and is not replicated.
- Run `ANALYZE` after the load.
- SQLite: `PRAGMA synchronous = OFF` is documented as a good option when creating a new database from scratch, but the database may be corrupted by an operating system crash or power loss.

## Checked

Date: 2026-11-07
Method: documentation only; no commands were run.
Read: the whole Populating a Database page; the UNLOGGED entry on CREATE TABLE and the synchronous entry on the PRAGMA page (searched for those entries, not read end to end).
Trimmed: the "10k to 100k rows" batch size and the WAL journal-mode advice for loads (not in the docs), and the self-check.

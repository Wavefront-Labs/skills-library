---
id: computing-software.database-administration.sqlite.attach-database-and-cross-database-queries
name: attach-database-and-cross-database-queries
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, sqlite3-cli, attach-database, cross-database-query, data-migration, schema-names]
level: practitioner
status: verified
description: "Use SQLite ATTACH DATABASE to query and copy across several database files in one connection, with transaction, WAL and limit caveats."
sources:
  - https://www.sqlite.org/lang_attach.html
  - https://www.sqlite.org/limits.html
  - https://www.sqlite.org/atomiccommit.html#multifile
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ATTACH DATABASE and cross-database queries

## Attach and query
```sql
ATTACH DATABASE 'archive-2025.db' AS arc;
ATTACH DATABASE ':memory:' AS scratch;
ATTACH DATABASE 'file:ref.db?mode=ro' AS ref;        -- read-only; URI filenames are off by default and must be enabled on the connection
SELECT name, file FROM pragma_database_list;          -- main, temp, arc, scratch, ref

SELECT o.id, o.total, c.name
FROM main.orders o JOIN ref.customers c ON c.id = o.customer_id;

INSERT INTO arc.orders SELECT * FROM main.orders WHERE created_at < '2026-01-01';
DELETE FROM main.orders WHERE created_at < '2026-01-01';
DETACH DATABASE arc;
```
If an unqualified name exists in several schemas, the docs say the least recently attached database wins; in a test on 3.50.4 `temp` also shadowed `main`. Qualify names to avoid surprises.

## Transactions across files
Per the docs, a transaction spanning several attached databases is atomic across them only if the main database is not `:memory:` and journal_mode is not WAL. Otherwise each file is atomic but a crash during COMMIT can leave some files updated and others not: a crash can leave one file
committed and the other not. For the archive-move example in WAL mode, make the operation
idempotent (insert first, verify, then delete).

## Limits and settings
- Default maximum of 10 attached databases (`SQLITE_MAX_ATTACHED`; cannot be raised above 125; lower it at run time with `SQLITE_LIMIT_ATTACHED`). Confirmed: the 11th ATTACH failed with `too many attached databases - max 10`.
- Pragmas are per schema: `PRAGMA arc.journal_mode = WAL;`, `PRAGMA arc.integrity_check;`.
- Each attached file has its own page cache and locks; a write transaction locks every file it
  writes to.
- ATTACH is not transactional: in a test on SQLite 3.50.4 an ATTACH inside `BEGIN` succeeded and survived the ROLLBACK, so DETACH explicitly.

## Common uses
- Migrating schema: `ATTACH 'new.db' AS n; CREATE TABLE n.t AS SELECT ... FROM main.t;`
- Splitting a large database into hot and archive files.
- Joining reference data shipped as a separate read-only file.
- Copying a whole database: `VACUUM INTO` is simpler than attach + insert.

## Security
Never let untrusted input choose the ATTACH path: it can create or read arbitrary files.
Applications embedding SQLite can block it with an authorizer callback (`SQLITE_ATTACH`) or
`SQLITE_LIMIT_ATTACHED = 0`; the CLI `--safe` mode disables ATTACH.

## Verify
`SELECT * FROM pragma_database_list;` shows the attached schemas, and row counts in source and
destination tables match after a copy.

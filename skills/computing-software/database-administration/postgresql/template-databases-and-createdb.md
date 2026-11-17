---
id: computing-software.database-administration.postgresql.template-databases-and-createdb
name: template-databases-and-createdb
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, managing-databases, template-databases, createdb, template0, template1, create-database, strategy-file-copy, database-cloning]
level: practitioner
status: verified
description: "Create PostgreSQL databases from template0/template1 correctly, use custom templates for fast clones, and fix 'source database is being accessed by other users'."
sources:
  - https://www.postgresql.org/docs/current/manage-ag-templatedbs.html
  - https://www.postgresql.org/docs/current/sql-createdatabase.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Template databases and CREATE DATABASE

**Goal:** new databases start with the right encoding, locale and baseline
objects, and cloning a database is a deliberate, fast operation.

## How templates work
`CREATE DATABASE x` copies `template1` by default. Anything installed there
(extensions, functions, tables) appears in every new database. `template0` is
the pristine copy: never modify it, and use it whenever you need a different
encoding/locale or are restoring a dump.
```sql
CREATE DATABASE app
  TEMPLATE template0
  ENCODING 'UTF8'
  LOCALE_PROVIDER icu ICU_LOCALE 'und'   -- or LC_COLLATE/LC_CTYPE for libc
  OWNER app_owner;
```
Shell equivalent: `createdb -T template0 -E UTF8 -O app_owner app`.

## Cloning a database
```sql
CREATE DATABASE app_copy TEMPLATE app STRATEGY file_copy;   -- PG15+
```
- `STRATEGY wal_log` (PG15+ default) copies block by block and writes each block to WAL: the most efficient choice when the template is small.
- `file_copy` writes only a small WAL record per tablespace, so it produces far less WAL for a large template, but it forces a checkpoint before and after.
The docs say **no other session** may be connected to the source. Observed on 17.6: `file_copy` waited about 5 seconds and then failed with
`ERROR: source database "app" is being accessed by other users`, while a `wal_log` clone succeeded with another session connected, so do not rely on either behaviour. Find and end sessions:
```sql
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='app' AND pid<>pg_backend_pid();
```
and block reconnects with `ALTER DATABASE app ALLOW_CONNECTIONS false;` meanwhile.
Mark a dedicated template with `ALTER DATABASE golden IS_TEMPLATE true;` so
non-superusers with CREATEDB can clone it and nobody can drop it accidentally.

## Gotchas
- Restoring a `pg_dump` into a database cloned from a polluted template1 gives
  duplicate-object errors (checked: `relation "pollute" already exists`); restore into a `template0` copy.
- `DROP DATABASE` also fails with connected users (after waiting about 5 seconds: `database "app" is being accessed by other users`); PG13+ has
  `DROP DATABASE app WITH (FORCE);`, which terminates them (they see `terminating connection due to administrator command`).
- Cloning is a point-in-time file copy, not transactional across databases.

## Verify
```sql
SELECT datname, datistemplate, datallowconn, pg_encoding_to_char(encoding), datlocprovider
FROM pg_database ORDER BY 1;
```
`\l+` in psql shows owner, encoding, collation and size.

## Checked
PostgreSQL 17.6: `CREATE DATABASE ... TEMPLATE template0 ENCODING 'UTF8' LOCALE_PROVIDER icu ICU_LOCALE 'und' OWNER ...` works (`datlocprovider = i`, `datlocale = und`; the column is `daticulocale` before PG17); `ALTER DATABASE ... ALLOW_CONNECTIONS false` makes logins fail with `database "lab" is not currently accepting connections`; `DROP` of a template fails with `cannot drop a template database`; a CREATEDB role could `createdb -T` a database marked `IS_TEMPLATE` and got `permission denied to create database` without CREATEDB; the `pg_database` Verify query runs. Docs: sql-createdatabase (strategies, the checkpoint note) and manage-ag-templatedbs.

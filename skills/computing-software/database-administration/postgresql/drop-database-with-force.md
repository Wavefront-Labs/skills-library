---
id: computing-software.database-administration.postgresql.drop-database-with-force
name: drop-database-with-force
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, managing-databases, drop-database-force, dropdb, active-connections, rename-database]
level: practitioner
status: verified
description: "Drop or rename a PostgreSQL database that still has sessions: block new connections, terminate backends, or use DROP DATABASE ... WITH (FORCE)."
sources:
  - https://www.postgresql.org/docs/current/sql-dropdatabase.html
  - https://www.postgresql.org/docs/current/manage-ag-dropdb.html
  - https://www.postgresql.org/docs/current/app-dropdb.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dropping a database with active connections

```
ERROR:  database "staging" is being accessed by other users
DETAIL:  There are 4 other sessions using the database.
```

## PG13+: one statement
```sql
DROP DATABASE staging WITH (FORCE);      -- terminates sessions, then drops
```
```bash
dropdb --force staging
```
FORCE will still fail if the database has **prepared transactions**, **active logical
replication slots**, or subscriptions; and you cannot drop the database you are connected
to (connect to `postgres`).

## Older versions or when you want control
```sql
-- 1. Stop reconnects (apps with retry loops race you otherwise)
ALTER DATABASE staging WITH ALLOW_CONNECTIONS false;
-- or: REVOKE CONNECT ON DATABASE staging FROM PUBLIC;  (superusers still get in)
-- 2. Kick existing sessions
SELECT pg_terminate_backend(pid) FROM pg_stat_activity
WHERE datname = 'staging' AND pid <> pg_backend_pid();
-- 3. Drop
DROP DATABASE staging;
```

## Blockers to clear first
```sql
SELECT gid, database FROM pg_prepared_xacts WHERE database = 'staging';   -- ROLLBACK PREPARED 'gid'
SELECT slot_name, active FROM pg_replication_slots WHERE database = 'staging'; -- pg_drop_replication_slot()
```
Subscriptions in the database: `ALTER SUBSCRIPTION s DISABLE; ALTER SUBSCRIPTION s SET (slot_name = NONE); DROP SUBSCRIPTION s;`
if the publisher is gone.

## Renaming has the same requirement
`ALTER DATABASE old RENAME TO new;` needs zero other sessions; use the same
`ALLOW_CONNECTIONS false` + terminate sequence, rename, then
`ALTER DATABASE new WITH ALLOW_CONNECTIONS true;`.

## Gotchas
- `DROP DATABASE` cannot run inside a transaction block (migration tools wrapping
  everything in BEGIN fail).
- It is irreversible and not WAL-recoverable except from a backup/PITR; take a `pg_dump` of
  anything you might want.
- PgBouncer keeps server connections open; `PAUSE staging;` or `KILL staging;` on the
  PgBouncer console first, or it reconnects immediately.
- Dropping a database interrupted mid-way leaves it marked invalid (recent minor releases of 14 and later); you can only
  drop it again (`datconnlimit = -2` in pg_database).

## Verify
`SELECT datname FROM pg_database WHERE datname = 'staging';` returns no row; disk space
returns once the directory under `base/` is removed.

## Checked
- PostgreSQL 17.6: plain `DROP DATABASE` and `ALTER DATABASE ... RENAME` fail with `is being accessed by other users`; `DROP DATABASE` inside a transaction block is refused; `WITH (FORCE)` and `dropdb --force` terminate sessions and drop; `ALLOW_CONNECTIONS false` plus terminating sessions lets a rename succeed and new connections get `not currently accepting connections`; `REVOKE CONNECT ... FROM PUBLIC` still lets a superuser in; a prepared transaction blocks `FORCE` (`is being used by prepared transactions`) until rolled back; an inactive logical slot did not block and was dropped with the database. The 14-17 `pg_database` docs state `datconnlimit` -2 marks an invalid database (interrupted drop).

---
id: computing-software.database-administration.postgresql.per-database-and-per-role-settings
name: per-database-and-per-role-settings
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, managing-databases, alter-database-set, alter-role-set, pg-db-role-setting, configuration-precedence]
level: practitioner
status: verified
description: "Scope settings to one database, one role, or a role in one database with ALTER DATABASE/ROLE SET, and know the precedence order and how to audit them."
sources:
  - https://www.postgresql.org/docs/current/manage-ag-config.html
  - https://www.postgresql.org/docs/current/sql-alterrole.html
  - https://www.postgresql.org/docs/current/config-setting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Per-database and per-role settings

## Commands
```sql
ALTER DATABASE app SET statement_timeout = '30s';
ALTER ROLE reporting SET work_mem = '256MB';
ALTER ROLE reporting IN DATABASE app SET search_path = analytics, public;
ALTER ROLE app SET idle_in_transaction_session_timeout = '60s';
ALTER ROLE ALL SET log_min_duration_statement = '2s';    -- every role, can be overridden

ALTER DATABASE app RESET statement_timeout;
ALTER ROLE reporting RESET ALL;
```
These are stored in `pg_db_role_setting` and applied **at session start**; existing sessions
keep their old values until they reconnect (poolers keep server connections for a long time:
`RECONNECT` in PgBouncer, or wait for `server_lifetime`).

## Precedence (later wins)
1. postgresql.conf / postgresql.auto.conf (ALTER SYSTEM) / command line
2. `ALTER DATABASE x SET`
3. `ALTER ROLE r SET`
4. `ALTER ROLE r IN DATABASE x SET`
5. Client connection options (`options=-c work_mem=64MB` in the connection string, `PGOPTIONS`)
6. `SET` / `SET LOCAL` inside the session

## Good uses
- Guardrails per app: `statement_timeout`, `idle_in_transaction_session_timeout`,
  `lock_timeout` for the migration role.
- Memory per workload: large `work_mem` only for the reporting role.
- `search_path` per database/role instead of in application code.
- `default_transaction_read_only = on` for a read-only role (defence in depth, not security:
  a user can `SET` it back).

## Audit
```sql
SELECT coalesce(r.rolname, 'ALL') AS role, coalesce(d.datname, 'ALL') AS db, s.setconfig
FROM pg_db_role_setting s
LEFT JOIN pg_roles r ON r.oid = s.setrole
LEFT JOIN pg_database d ON d.oid = s.setdatabase;
```
psql shortcut: `\drds`. To see where the current value came from:
`SELECT name, setting, source FROM pg_settings WHERE name = 'work_mem';`
(`source` = `database`, `user`, `database user`, `global` for `ALTER ROLE ALL`, `client` for connection options, `session`, `configuration file`).
The most specific entry wins: `ALTER ROLE r IN DATABASE d` over `ALTER ROLE r` over `ALTER DATABASE d`, and `ALTER ROLE ALL` is the weakest of the catalog entries.

## Gotchas
- Only settings with context `user` or `superuser` can be set this way; `postmaster`-context
  parameters (shared_buffers) cannot (`parameter "shared_buffers" cannot be changed without restarting the server`).
- A role setting overrides a database setting even when the database one is stricter; put
  hard limits on the role if roles span databases.
- `pg_dumpall --globals-only` exports `ALTER ROLE ... SET`, but `ALTER ROLE ... IN DATABASE` and `ALTER DATABASE ... SET` only appear in a full `pg_dumpall`; `pg_dump` of a single database includes its `ALTER DATABASE ... SET` only with `--create`.

## Verify
Open a new session as the role in the database and `SHOW statement_timeout;`, checking
`pg_settings.source` points at the expected level.

## Checked
PostgreSQL 17.6: all the `ALTER DATABASE/ROLE` statements run; `\drds` and the audit query list `ALL`/role/database combinations; for role `reporting` in database `pd`, `pg_settings.source` was `user` for `work_mem` and `statement_timeout` (the role's 99s beat the database's 30s), `database user` for `search_path`, `global` for `log_min_duration_statement` from `ALTER ROLE ALL`, `session` after `SET`, and `client` (64MB) with `PGOPTIONS="-c work_mem=64MB"` overriding the role's 256MB; `RESET` removed entries; `pg_dump -s` printed no `ALTER DATABASE`, `pg_dump -C` printed `ALTER DATABASE pd SET statement_timeout TO '30s';`, `pg_dumpall --globals-only` printed `ALTER ROLE reporting SET work_mem` and a full `pg_dumpall` printed the `IN DATABASE` entry.

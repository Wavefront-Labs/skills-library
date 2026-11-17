---
id: computing-software.database-administration.postgresql.parameter-contexts-reload-vs-restart
name: parameter-contexts-reload-vs-restart
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, postgresql-conf, alter-system, pending-restart, pg-reload-conf, parameter-context, pg-settings, pg-file-settings, configuration-precedence]
level: practitioner
status: verified
description: "Know whether a PostgreSQL setting needs a restart, reload or just SET: pg_settings context, pending_restart, pg_file_settings errors, and which file wins."
sources:
  - https://www.postgresql.org/docs/current/config-setting.html
  - https://www.postgresql.org/docs/current/view-pg-settings.html
  - https://www.postgresql.org/docs/current/view-pg-file-settings.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Parameter contexts: reload vs restart

**Goal:** apply a configuration change with the least disruption, and prove it
actually took effect.

## Context column decides
```sql
SELECT name, setting, unit, context, source, sourcefile, pending_restart
FROM pg_settings WHERE name IN ('shared_buffers','work_mem','max_connections','log_min_duration_statement');
```
| context | How to apply |
|---|---|
| `internal` | Fixed at build/initdb |
| `postmaster` | Restart (shared_buffers, max_connections, wal_level, shared_preload_libraries) |
| `sighup` | Reload: `SELECT pg_reload_conf();` / `pg_ctl reload` / `systemctl reload` |
| `superuser-backend` / `backend` | Reload, but only new sessions pick it up |
| `superuser` | Reload, or `SET` by superusers (or roles granted SET privilege, PG15) |
| `user` | Reload, or any user `SET` / `ALTER ROLE ... SET` / `ALTER DATABASE ... SET` |

## Where values come from (later wins)
postgresql.conf → included files (`include_dir 'conf.d'`) → `postgresql.auto.conf`
(written by `ALTER SYSTEM`) → per-database → per-role → per-role-in-database →
session `SET` → `SET LOCAL` in a transaction. `source` and `sourcefile` show the winner.

## Safe change procedure
```sql
ALTER SYSTEM SET log_min_duration_statement = '250ms';   -- or edit postgresql.conf
SELECT name, error, applied FROM pg_file_settings WHERE error IS NOT NULL OR NOT applied;
SELECT pg_reload_conf();
SELECT name, setting, pending_restart FROM pg_settings WHERE pending_restart;
```
`pg_file_settings` shows parse errors **before** you reload or restart (`syntax error`, `unrecognized
configuration parameter`, `setting could not be applied`). On a reload a syntax error or an unrecognized
parameter makes PostgreSQL ignore the whole file (`contains errors; no changes were applied`), while an invalid value
for a known parameter skips only that setting (`unaffected changes were applied`); both are logged (tested on 18.6).
A restart fails on either.
`pending_restart = true` after reload means a postmaster-context value changed
and is waiting for a restart.

## Gotchas
- `ALTER SYSTEM` values in postgresql.auto.conf override postgresql.conf
  silently: config management that edits postgresql.conf seems to "not work".
  `ALTER SYSTEM RESET name;` removes the override. PG17 can disable ALTER SYSTEM (`allow_alter_system = off`).
- Per-role settings (`ALTER ROLE app SET work_mem`) override the server value for that role: check `pg_db_role_setting` when behaviour differs per user.
- Units: `'250ms'`, `'4GB'`; bare numbers use the parameter's base unit (kB, 8kB blocks, ms).

## Verify
`SHOW <name>;` in a **new** session shows the intended value and
`pg_settings.source` is the expected file; no rows with `pending_restart` unless a restart is scheduled.

## Checked
- PostgreSQL 18.6: `pg_settings` contexts: `block_size` internal, `shared_buffers`/`max_connections`/`wal_level`/`shared_preload_libraries` postmaster, `log_min_duration_statement`/`deadlock_timeout` superuser, `log_connections` superuser-backend, `work_mem` user; counts per context listed (backend 2, internal 20, postmaster 69, sighup 104, superuser 62, superuser-backend 4, user 151). `ALTER SYSTEM SET max_connections = 120` + reload showed it in `pending_restart`; `ALTER SYSTEM RESET` + reload cleared it. A role granted `SET ON PARAMETER deadlock_timeout` could set it; the same role got `permission denied to set parameter "log_min_duration_statement"`. Precedence test with `work_mem`: database 6MB < role 7MB < role-in-database 8MB (`source` showed `database user`) < session `SET` 9MB < `SET LOCAL` 10MB inside the transaction, and the session value returned after COMMIT. Reload with an unknown parameter in an included file: `contains errors; no changes were applied`; with `work_mem = 'abc'`: `invalid value for parameter "work_mem"` then `contains errors; unaffected changes were applied`; with a syntax error: `syntax error ... near token "MB"` and the whole file ignored; `pg_file_settings` showed `setting could not be applied` / `syntax error` rows. `pg_db_role_setting` lists role and database settings; `allow_alter_system` exists (on).
- Release notes: `allow_alter_system` in 17; `GRANT ... ON PARAMETER` (SET/ALTER SYSTEM privileges) in 15.

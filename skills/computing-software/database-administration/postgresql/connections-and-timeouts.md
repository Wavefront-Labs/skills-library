---
id: computing-software.database-administration.postgresql.connections-and-timeouts
name: connections-and-timeouts
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, postgresql-conf, max-connections, statement-timeout, idle-session-timeout, idle-in-transaction-session-timeout, reserved-connections, tcp-keepalives, too-many-clients]
level: practitioner
status: verified
description: "Size PostgreSQL max_connections realistically and set statement, lock, idle and idle-in-transaction timeouts plus TCP keepalives so stuck clients cannot exhaust the server."
sources:
  - https://www.postgresql.org/docs/current/runtime-config-connection.html
  - https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-STATEMENT-TIMEOUT
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Connections and timeouts

**Goal:** no "FATAL: sorry, too many clients already" and no forgotten sessions
holding locks or snapshots for hours.

## max_connections
Each connection is a backend process, and lock/snapshot overhead grows with connection
count. The sizing figures below are rules of thumb, not documented limits:
- Keep `max_connections` in the low hundreds; put PgBouncer in front for apps that
  open thousands.
- Active connections of roughly 2-4 per core is a common starting point; measure.
- Reserve slots: `superuser_reserved_connections = 3`, and (PG16)
  `reserved_connections = 5` for roles granted `pg_use_reserved_connections` (monitoring).
- Changing it needs a restart; standbys must have >= the primary's value.

## Timeouts (set per role or database, not only globally)
```sql
ALTER ROLE app SET statement_timeout = '30s';                     -- any single statement
ALTER ROLE app SET lock_timeout = '5s';                           -- waiting for a lock
ALTER ROLE app SET idle_in_transaction_session_timeout = '60s';   -- BEGIN then nothing: kills session
ALTER ROLE app SET idle_session_timeout = '30min';                -- PG14: idle outside transaction (not behind a pooler!)
ALTER ROLE reporting SET statement_timeout = '15min';
ALTER DATABASE appdb SET transaction_timeout = '5min';            -- PG17: whole transaction
```
Idle-in-transaction sessions are the dangerous ones: they hold locks and the
xmin horizon (blocking vacuum cleanup everywhere).

## Dead clients
Without keepalives, a client that vanished (network cut) leaves a backend waiting
forever on a socket:
```conf
tcp_keepalives_idle = 60
tcp_keepalives_interval = 10
tcp_keepalives_count = 6
client_connection_check_interval = '10s'   # PG14: abort long queries whose client disconnected
```
Platform notes from the docs: `client_connection_check_interval` relies on kernel socket events (it must be 0 where unsupported) and is ignored on Unix-socket sessions; `tcp_keepalives_*` read `-1`/OS defaults on some platforms (Windows showed `-1`, `-1`, `10`).

## Find offenders
```sql
SELECT pid, usename, application_name, state, now() - state_change AS in_state, now() - xact_start AS xact_age, query
FROM pg_stat_activity WHERE state <> 'active' AND xact_start IS NOT NULL ORDER BY xact_age DESC;
SELECT count(*), state FROM pg_stat_activity GROUP BY state;
```

## Gotchas
- A global `statement_timeout` also hits pg_dump, VACUUM jobs and migrations; set it per role.
- `idle_session_timeout` with a pooler kills pooled server connections and causes errors; use the pooler's own idle settings.

## Verify
`SELECT rolname, rolconfig FROM pg_roles WHERE rolconfig IS NOT NULL;` shows the
timeouts; a test `BEGIN; SELECT 1;` left idle is terminated after the configured time,
logged as `FATAL: terminating connection due to idle-in-transaction timeout`
(`idle-session timeout` for `idle_session_timeout`).

## Checked
- PostgreSQL 18.6: every `ALTER ROLE ... SET` / `ALTER DATABASE ... SET` in the block was accepted (including `transaction_timeout`) and `pg_roles.rolconfig` listed them; the pg_stat_activity offender queries ran. With `idle_in_transaction_session_timeout = '1s'` an idle `BEGIN; SELECT 1;` session was terminated, and with `idle_session_timeout = '1s'` an idle session was; the server log showed `terminating connection due to idle-in-transaction timeout` / `idle-session timeout`. `reserved_connections` (0 default), `superuser_reserved_connections` (3) and role `pg_use_reserved_connections` exist; `SHOW tcp_keepalives_*` on Windows returned -1/-1/10.
- Release notes: `idle_session_timeout` is in 14, `transaction_timeout` in 17, `reserved_connections` / `pg_use_reserved_connections` in 16. Docs: standby values must be equal or higher than the primary for max_connections and the related list; `client_connection_check_interval` platform text.

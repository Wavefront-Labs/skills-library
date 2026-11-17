---
id: computing-software.database-administration.postgresql.pgbouncer-admin-console-show-pools
name: pgbouncer-admin-console-show-pools
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, pgbouncer, pgbouncer-admin-console, pgbouncer-show-pools, cl-waiting, monitoring, connection-pooling]
level: practitioner
status: docs-checked
description: "Use the PgBouncer admin console to see pool saturation: SHOW POOLS (cl_waiting, maxwait), SHOW STATS, SHOW CLIENTS/SERVERS, and RELOAD after config changes."
sources:
  - https://www.pgbouncer.org/usage.html#admin-console
  - https://www.pgbouncer.org/config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PgBouncer admin console

## Connect
```bash
psql -h 127.0.0.1 -p 6432 -U pgbouncer pgbouncer
```
Only users listed in `admin_users` or `stats_users` can log in to the console.

## SHOW POOLS: the saturation view
```
 database | user | cl_active | cl_waiting | sv_active | sv_idle | sv_used | maxwait | maxwait_us | pool_mode
```
- `cl_waiting` > 0 means clients are queued for a server connection. Sustained non-zero =
  pool too small, or server connections held too long (long transactions, session mode).
- `maxwait` (seconds) / `maxwait_us` (microsecond part): how long the oldest queued client has waited; if it keeps rising, the pool is too small or the server is overloaded. Choose your own alert threshold.
- `sv_active` = server connections linked to clients; `sv_idle` = ready; `sv_used` = idle longer than
  `server_check_delay`, so `server_check_query` runs before reuse.
- If `sv_active` == `pool_size` and `cl_waiting` grows: saturated. Check Postgres for slow
  queries before simply raising `default_pool_size`.

## SHOW STATS / STATS_TOTALS / STATS_AVERAGES
Per database: `total_xact_count`, `total_query_count`, `avg_xact_time` (us),
`avg_query_time`, `avg_wait_time` (time clients waited for a server). Rising `avg_wait_time`
is the user-visible symptom of pool starvation.

## Other views
```sql
SHOW CLIENTS;      -- each client: addr, state (active/waiting/idle), connect_time, link
SHOW SERVERS;      -- each server conn: state, connect_time, request_time, link
SHOW DATABASES;    -- pool_size, reserve_pool_size, max_connections, current_connections, paused
SHOW CONFIG;       -- effective settings (changeable column)
SHOW LISTS; SHOW MEM; SHOW DNS_HOSTS;
SHOW VERSION;
```

## Control commands
```sql
RELOAD;                 -- re-read pgbouncer.ini, auth_file and auth_hba_file (changeable settings)
PAUSE app; RESUME app;  -- drain and hold (see the PAUSE/RESUME skill)
DISABLE app; ENABLE app;  -- reject new client connections to db
KILL app;               -- drop all client and server connections to db
RECONNECT app;          -- close server connections after they are released (a RELOAD that changes the connection string or a DNS change does this automatically)
SHUTDOWN;               -- the PgBouncer process exits
```

## Monitoring integration
Exporters can scrape these views; alert on `cl_waiting`, `maxwait`,
and `sv_login` spikes (server connections being established repeatedly).

## Verify
Under load, `SHOW POOLS` shows `cl_waiting = 0` most of the time and `maxwait` near zero;
after editing the ini file, `RELOAD` then `SHOW CONFIG` reflects the change.

## Checked
2026-10-31. Confirmed on pgbouncer.org usage.html: SHOW POOLS columns (cl_active, cl_waiting, sv_active, sv_idle, sv_used, sv_login, maxwait, maxwait_us, pool_mode), SHOW STATS columns (avg_xact_time and avg_wait_time in microseconds), SHOW CLIENTS states, SHOW DATABASES columns, RELOAD, PAUSE, RESUME, DISABLE, ENABLE, KILL, RECONNECT, SHUTDOWN, admin_users and stats_users. Removed: SUSPEND (not in the usage page), the peer-auth sentence, the pgbouncer_exporter name, the 1 s alert figure and the 'read-only' wording for stats_users.
Method: documentation only; no commands were run.

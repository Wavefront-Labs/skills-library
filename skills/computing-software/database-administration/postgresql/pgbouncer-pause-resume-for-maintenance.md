---
id: computing-software.database-administration.postgresql.pgbouncer-pause-resume-for-maintenance
name: pgbouncer-pause-resume-for-maintenance
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, pgbouncer, pgbouncer-pause, switchover, maintenance, zero-downtime, failover]
level: practitioner
status: docs-checked
description: "Use PgBouncer PAUSE/RESUME to hold client traffic during a restart or primary switchover so applications see a short delay instead of connection errors."
sources:
  - https://www.pgbouncer.org/usage.html#process-controlling-commands
  - https://www.pgbouncer.org/config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PgBouncer PAUSE / RESUME for maintenance

## What PAUSE does
`PAUSE [db];` disconnects from the servers, waiting for each server connection to be released: the
transaction must complete in transaction mode, the statement in statement mode, and the client must
disconnect in session mode. It does not return until all are disconnected. New client connections to a
paused database wait until `RESUME [db];`.
Clients only see added latency, as long as the pause is shorter than their timeouts and
PgBouncer's `query_wait_timeout` (default 120 s).

## Switchover runbook (primary moves to a new host)
```sql
-- on PgBouncer admin console
PAUSE app;                    -- returns when all server conns are released
```
```bash
# promote standby / repoint DNS or edit [databases] host=
# promote the standby with your HA tooling
sed -i 's/host=pg1/host=pg2/' /etc/pgbouncer/pgbouncer.ini
```
```sql
RELOAD;                       -- pick up new host
RESUME app;
```
Timing: aim for under 10-20 s total. Measure your promotion time in rehearsals.

## Restarting PostgreSQL for a config change
```sql
PAUSE;          -- all databases
```
`systemctl restart postgresql` then `RESUME;`.

## Gotchas
- `PAUSE` blocks until in-flight transactions end. A long-running transaction (or session
  in session pool mode) stalls the pause indefinitely. Check `SHOW SERVERS;` for
  `active` connections and their age first, or `KILL` stragglers (it drops client and server connections immediately; new clients wait until `RESUME`).
- Clients with their own short statement timeouts (e.g. 5 s in the app) will error during
  the pause anyway; coordinate.
- `RECONNECT app;` closes each server connection after it is released, without pausing. Connections can
  then split between old and new destinations for a while; the docs recommend `PAUSE` when all
  connections must switch at the same time. After `RELOAD` or `RECONNECT`, `WAIT_CLOSE` waits until
  the change is fully active.
- With multiple PgBouncer instances (behind a load balancer or `so_reuseport`), you must
  PAUSE each one; script it.

## Verify
During the pause, `SHOW POOLS;` shows `cl_waiting` rising and `sv_active = 0`; after RESUME,
`cl_waiting` drains to 0 and application error logs show no connection failures.

## Checked
2026-10-31. Confirmed on pgbouncer.org usage.html (PAUSE, RESUME, RECONNECT, KILL, WAIT_CLOSE, RELOAD, SHOW POOLS columns) and config.html (query_wait_timeout default 120 s, so_reuseport). Removed: the patronictl command (not checked), the claim that PAUSE does not survive a restart, and WAIT_CLOSE as a straggler fix (it waits for close_needed to clear).
Method: documentation only; no commands were run.

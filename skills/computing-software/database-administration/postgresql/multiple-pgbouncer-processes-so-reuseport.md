---
id: computing-software.database-administration.postgresql.multiple-pgbouncer-processes-so-reuseport
name: multiple-pgbouncer-processes-so-reuseport
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, so-reuseport, pgbouncer, pgbouncer-scaling, online-restart, peering, connection-pooling]
level: practitioner
status: docs-checked
description: "Scale PgBouncer past one CPU core by running several processes on one port with so_reuseport, use peering for cancel requests, and restart without dropping clients."
sources:
  - https://www.pgbouncer.org/config.html#so_reuseport
  - https://www.pgbouncer.org/config.html#section-peers
  - https://www.pgbouncer.org/usage.html#online-restart
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running multiple PgBouncer processes and online restart

PgBouncer is single-threaded. When one core is saturated, latency rises and `SHOW POOLS` waits grow though PostgreSQL is idle.

## Several processes on one port (so_reuseport)
```ini
# /etc/pgbouncer/pgbouncer-1.ini  (and -2, -3 ... with their own pidfile, logfile, unix socket dir)
[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
so_reuseport = 1
peer_id = 1
unix_socket_dir = /var/run/pgbouncer-1
pidfile = /var/run/pgbouncer-1/pgbouncer.pid

[peers]
1 = host=/var/run/pgbouncer-1
2 = host=/var/run/pgbouncer-2
3 = host=/var/run/pgbouncer-3
```
- On operating systems that support SO_REUSEPORT, the kernel distributes new connections across processes listening on the same port (see `so_reuseport` on the config page).
- **Peering** (1.19+): a cancel request (Ctrl-C, `statement_timeout` from the client side) may land on a different process than the one holding the session; `[peers]` + `peer_id` let it be forwarded. Without peering, cancels randomly fail.
- Pool size is per process: total server connections = `default_pool_size x processes`. Divide the budget.
- systemd template unit `pgbouncer@.service` with `%i` selecting the ini makes N instances manageable.

## Online restart (upgrade binary or change non-reloadable settings)
- Modern method with so_reuseport: start a new process (new version) on the same port, then send `SHUTDOWN WAIT_FOR_CLIENTS;` to the old one in the admin console (SIGTERM does the same from 1.23.0; earlier versions shut down immediately); it stops accepting new connections and exits once its clients disconnect.
- Classic method: `pgbouncer -R` (takeover) was removed in a recent release together with `SHOW FDS` and `SUSPEND`; the changelog says to use rolling restarts with so_reuseport instead.
- `RELOAD` covers most settings without any restart.

## Verify
```bash
ss -ltnp 'sport = :6432'          # one LISTEN line per process
for i in 1 2 3; do psql -h /var/run/pgbouncer-$i -p 6432 -U pgbouncer pgbouncer -c 'SHOW POOLS;'; done
```
Check CPU per process with `top -p $(pgrep -d, pgbouncer)`: load should be spread.

## Gotchas
- Admin console commands (PAUSE, RELOAD) apply to one process; script them across all instances.
- Clients from one app instance can land on different processes; prepared statement tracking (`max_prepared_statements`) is per process, which is fine since each server link is tracked separately.

## Checked

2026-10-28. Confirmed against the PgBouncer config page (so_reuseport, peer_id, [peers]), usage page (SHUTDOWN WAIT_FOR_CLIENTS, SIGTERM behaviour from 1.23.0) and changelog (peering added in 1.19.0). Corrected: -R online restart is removed in recent releases, not merely deprecated. Removed: the 100% CPU figure and the Linux 3.9 kernel version.

Method: documentation only; no commands were run.

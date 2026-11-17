---
id: computing-software.database-administration.postgresql.shutdown-modes-and-pg-ctl
name: shutdown-modes-and-pg-ctl
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, pg-ctl, shutdown-modes, pg-ctl-stop, smart-shutdown, fast-shutdown, immediate-shutdown, postgres-server-setup, sigterm, sigint, sigquit]
level: practitioner
status: verified
description: "Stop, restart and reload PostgreSQL with the right pg_ctl shutdown mode (smart, fast, immediate) and know what each does to sessions, checkpoints and recovery time."
sources:
  - https://www.postgresql.org/docs/current/server-shutdown.html
  - https://www.postgresql.org/docs/current/app-pg-ctl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PostgreSQL shutdown modes

**Goal:** take the server down with predictable impact and predictable restart time.

## The three modes
| pg_ctl `-m` | Signal to postmaster | Behaviour | Next start |
|---|---|---|---|
| `smart` | SIGTERM | Refuses new connections, waits for every existing session to disconnect. Can wait forever behind a pooler. | Clean |
| `fast` (default since 9.5) | SIGINT | Rolls back open transactions, disconnects clients, runs a shutdown checkpoint. | Clean, fast |
| `immediate` | SIGQUIT | Kills all processes without a checkpoint. | Crash recovery (WAL replay since last checkpoint) |

```bash
pg_ctl -D <datadir> stop -m fast -t 120     # wait up to 120 s
pg_ctl -D <datadir> restart -m fast
pg_ctl -D <datadir> reload                   # SIGHUP: re-read postgresql.conf / pg_hba.conf
pg_ctl -D <datadir> promote                  # standby only
```
Service managers wrap `pg_ctl` or send these signals themselves; check which signal or `-m` mode
your unit uses (the docs map SIGINT to fast, SIGTERM to smart, SIGQUIT to immediate).

## Making fast shutdown actually fast
The shutdown checkpoint has to flush all dirty buffers. With a large
`shared_buffers` and a long `checkpoint_timeout`, it can take minutes, and a service manager's stop timeout
may then kill the server. Before planned restarts:
```sql
CHECKPOINT;   -- flush now while still serving traffic
```
then `pg_ctl stop -m fast`; the shutdown checkpoint has little left to do.

## Gotchas
- Never `kill -9` the postmaster: the docs say it prevents releasing shared memory and semaphores and
  leaves subprocesses to kill by hand; expect crash recovery. A crashed backend makes the postmaster reinitialise
  all sessions (`restart_after_crash = on` by default).
- `immediate` is safe for data (WAL guarantees it) but recovery time is
  proportional to WAL since the last checkpoint, potentially many GB.
- On a primary with replication, the server will not fully shut down until all outstanding WAL records are
  transferred to the connected standbys (docs, synchronous replication); a stuck standby connection can stall it.
- `pg_ctl reload` does not apply `postmaster`-context settings; check
  `pending_restart` in `pg_settings`.

## Verify
- `pg_ctl status -D <datadir>` reports no server running.
- Server log ends with `database system is shut down`; next start shows
  `database system was shut down at ...` (clean) rather than
  `database system was interrupted; last known up at ...` (crash recovery).

## Checked
- PostgreSQL 18.6 (Windows, pg_ctl): with a session running `pg_sleep(30)`, `pg_ctl stop -m smart -t 5` printed `waiting for server to shut down........ failed` and the HINT `The "-m fast" option immediately disconnects sessions rather than waiting for session-initiated disconnection`; a new connection meanwhile got `FATAL: the database system is shutting down`; `pg_ctl stop -m fast` then stopped it (`done`, `server stopped`; log `received fast shutdown request`, `checkpoint starting: shutdown immediate`, `database system is shut down`). After `stop -m immediate` the next start logged `database system was interrupted; last known up at ...`, then `database system was not properly shut down; automatic recovery in progress`, `redo starts at`, `redo done`. `pg_ctl status` reported `no server running` when stopped; `pg_ctl restart -m fast`, `pg_ctl reload` (`server signaled`) and `pg_ctl promote` (`server promoted`) ran. `pg_settings.pending_restart` showed a pending `max_connections` change after reload.
- Docs: app-pg-ctl (smart/fast/immediate, fast is the default), server-shutdown (signal mapping, SIGKILL warning), 9.5 release notes (default changed from smart to fast), runtime-config-error-handling (`restart_after_crash`), warm-standby (shutdown waits for outstanding WAL transfer).
- The systemd unit names and `TimeoutStopSec` remark were removed (Linux only, not run).

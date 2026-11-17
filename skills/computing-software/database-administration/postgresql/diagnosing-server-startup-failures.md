---
id: computing-software.database-administration.postgresql.diagnosing-server-startup-failures
name: diagnosing-server-startup-failures
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres-server-setup, postgres-startup-failure, postmaster-pid, pg-ctl, troubleshooting, shared-memory]
level: practitioner
status: verified
description: "Find why postgres will not start: read the right log, then fix port conflicts, stale postmaster.pid, permissions, shared memory and bad config values."
sources:
  - https://www.postgresql.org/docs/current/server-start.html
  - https://www.postgresql.org/docs/current/kernel-resources.html
  - https://www.postgresql.org/docs/current/app-pg-ctl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnosing PostgreSQL start-up failures

## 1. Find the actual error
`pg_ctl start` and `systemctl start` only tell you it failed. The reason is in:
```bash
pg_ctl -D $PGDATA -l startup.log start            # -l captures the server's stderr
tail -n 50 $PGDATA/log/*.log                      # if logging_collector=on and it got that far
postgres -D $PGDATA                               # foreground, as the unprivileged service user: errors go to the terminal
```
On a service-manager install read that manager's log for the unit (for example `journalctl -u <unit>` under systemd; unit names differ by distro).
Running `postgres -D` in the foreground is the fastest way to see config parse errors that happen
before the logger starts; stop it with Ctrl-C. It refuses to run as an administrator/root user (`Execution of PostgreSQL by a user with administrative permissions is not permitted`).

## 2. Match the message
| Message | Cause | Fix |
|---|---|---|
| `could not bind IPv4 address "<addr>": <OS error text>` with hint `Is another postmaster already running on port N?` | another postmaster or process on the port (OS text differs: `Address already in use` on Linux, `Only one usage of each socket address ...` on Windows); with several `listen_addresses` the server may still start on the others | find the process holding the port (`ss -ltnp`, `netstat -ano`); stop it or change `port` |
| `lock file "postmaster.pid" already exists` (hint `Is another postmaster (PID n) running in data directory ...?`) | the PID in the file belongs to a live process. A stale file whose PID is dead is normally ignored and startup proceeds (`pg_ctl` prints `another server might be running; trying to start server anyway`) | check the PID in the file is not a postgres process using that PGDATA; delete `postmaster.pid` only if the PID is reused by an unrelated process |
| `data directory "..." has invalid permissions` (detail: `Permissions should be u=rwx (0700) or u=rwx,g=rx (0750)`) | group/other access on PGDATA (check is skipped on Windows) | `chmod 700 $PGDATA`; owner must be the service user |
| `could not create shared memory segment` / `could not map anonymous shared memory` | `shared_buffers` or `huge_pages=on` beyond what the kernel allows (messages from the Unix shared-memory code) | lower `shared_buffers`, set `huge_pages=try`, or raise the kernel limits described in the server docs' kernel-resources page |
| `invalid value for parameter "..."` / `syntax error in file ... line N, near token "..."` followed by `configuration file ... contains errors` | bad postgresql.conf or postgresql.auto.conf edit | fix the line; `ALTER SYSTEM` mistakes live in `postgresql.auto.conf` |
| `could not open file "global/pg_control"` / `database files are incompatible with server` (detail names the data directory's version) | wrong PGDATA, or binaries of a different major version | check `PG_VERSION` in PGDATA against `postgres --version` |
| `could not create lock file "<socket dir>/.s.PGSQL.5432.lock"` | `unix_socket_directories` directory missing (for example a tmpfs cleared at boot) | create the directory before start, via your service manager |
| `FATAL: the database system is starting up` for a long time | crash recovery replaying WAL | wait; watch progress in the log (`redo in progress, elapsed time: ... s, current LSN: ...`) |

## 3. Verify config before restarting
```sql
SELECT name, setting, error FROM pg_file_settings WHERE error IS NOT NULL;
SELECT * FROM pg_hba_file_rules WHERE error IS NOT NULL;
```
Run these on the running server after editing files and before a restart, so a typo
does not turn a reload into an outage.

## Gotchas
- Never delete `postmaster.pid` while a postmaster is running: two postmasters on one
  data directory corrupt it. On containers, a reused PID can make a stale file look live;
  confirm the process is actually postgres.
- Never remove files from `pg_wal` to "free space" to get it to start; see the WAL disk-full
  procedure instead.
- `pg_ctl -w -t 300 start` waits for readiness; crash recovery after a large checkpoint
  interval can exceed the default 60 s timeout and look like a failure when it is not.

## Verify
`pg_isready -h <host or socket dir> -p <port>` prints `<host>:<port> - accepting connections` (`- rejecting connections` while a standby has `hot_standby = off`), and the log
shows `database system is ready to accept connections`.

## Checked
- PostgreSQL 18.6 (Windows), each reproduced with `pg_ctl start -l`: an unknown value `shared_buffers=notanumber` gave `invalid value for parameter "shared_buffers"` then `configuration file ... contains errors`; `foo bar baz` gave `syntax error in file ... line 896, near token "baz"`; `PG_VERSION` set to 15 gave `FATAL: database files are incompatible with server` with the version in the detail; a copied `postmaster.pid` holding a live postmaster's PID gave `lock file "postmaster.pid" already exists` with hint `Is another postmaster (PID 20764) running ...`; a pid file with a dead PID let the server start after `another server might be running; trying to start server anyway`; a second server on a used port logged `could not bind IPv4 address "127.0.0.1": Only one usage of each socket address ...` plus the hint, and still started on IPv6 `localhost`; running `postgres -D` directly as an administrator printed the refusal text.
- Source (postgres REL_18_STABLE on GitHub, miscinit.c, sysv_shmem.c, pqcomm.c, xlogrecovery.c, controldata_utils.c): exact message strings for invalid permissions (with the 0700/0750 detail and the non-Windows guard), lock file exists (CreateLockFile also checks whether the recorded PID still exists, so a dead PID is not an error), could not create lock file, shared memory messages, `redo in progress, elapsed time`, and the bind hint.
- Not run here (Linux only): systemd/journalctl, `ss`, hugepage tuning. They are stated as environment pointers; read your distro's docs for exact names.

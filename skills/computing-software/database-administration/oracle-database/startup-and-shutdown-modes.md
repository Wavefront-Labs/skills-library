---
id: computing-software.database-administration.oracle-database.startup-and-shutdown-modes
name: startup-and-shutdown-modes
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, oracle-instance, startup-nomount, startup-mount, shutdown-immediate, shutdown-abort, restricted-session, sqlplus, srvctl]
level: practitioner
status: docs-checked
description: "Start and stop an Oracle instance through NOMOUNT, MOUNT and OPEN, choose the right SHUTDOWN mode, and use restricted and read-only open."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/starting-up-and-shutting-down.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Startup and shutdown modes

## Startup stages
```
sqlplus / as sysdba
STARTUP NOMOUNT;          -- instance only: no database access
ALTER DATABASE MOUNT;     -- mounted but closed: certain DBA activities, no general access
ALTER DATABASE OPEN;      -- any user with CREATE SESSION can connect
```
`STARTUP` alone starts the instance, mounts and opens the database.
- **NOMOUNT**: usually only for database creation or re-creating control files.
- **MOUNT**: for administrative operations that need the database mounted but closed.
- **OPEN**: unrestricted (all users) or restricted (`STARTUP RESTRICT`; DBAs only).
- **FORCE** (`STARTUP FORCE`): force a start after a startup or shutdown problem. **OPEN RECOVER** starts and begins
  complete media recovery immediately.
- `ALTER DATABASE OPEN READ ONLY;` lets you query while guaranteeing data files and redo logs are not written to.
  It does not restrict recovery, nor operations that generate no redo (such as taking data files offline or online).
  Read/write is the default. A query that sorts to disk needs a locally managed default temporary tablespace.
- Restricted mode: only users with `RESTRICTED SESSION` (SYSDBA connections and the DBA role have it) can start new
  connections. Switch with `ALTER SYSTEM ENABLE RESTRICTED SESSION;` and `ALTER SYSTEM DISABLE RESTRICTED SESSION;`.
- `STARTUP PFILE = <path>` starts from a named initialization parameter file instead of the default one. Without a
  PFILE clause the instance reads an SPFILE from the default location, then falls back to a text parameter file.
- You cannot start an instance while connected through a shared server process.

If `CONTROL_FILES` entries cannot be opened, the database is not mounted; if data files or online redo logs cannot be
opened, it is not opened. Both return a warning message.

## Shutdown modes
Connect as SYSOPER, SYSDBA, SYSBACKUP or SYSDG. `NORMAL` is the default.

| Mode | New connections | Current sessions | Transactions | Next startup recovery |
|---|---|---|---|---|
| `NORMAL` | no | waits for all to disconnect | n/a | none needed |
| `TRANSACTIONAL` | no | disconnected after transactions complete | waits for them; no new ones | none needed |
| `IMMEDIATE` | no | disconnected, statements terminated | uncommitted work rolled back | none needed |
| `ABORT` | no | statements terminated at once, users disconnected | not rolled back | automatic instance recovery |

Oracle describes `IMMEDIATE` as for automated unattended backups, an imminent power shutdown, or a database or
application misbehaving when users cannot log off. Long uncommitted transactions can make it slow. Use `ABORT` only
if you must stop instantly, no other mode works, or the instance has startup problems. If a shutdown is blocked for an hour it aborts with ORA-01013; do not interrupt a
shutdown, and after ORA-01013 resubmit `SHUTDOWN`, and use `SHUTDOWN ABORT` only if repeated attempts fail.

## Managed by Oracle Restart
If Oracle Restart manages the database, Oracle recommends `srvctl start database -db <db_unique_name>` and
`srvctl stop database -db <db_unique_name> -stopoption immediate` (other options: normal, transactional, abort) rather
than SQL*Plus. If `-stopoption` is omitted, the stored Oracle Restart stop option applies (default immediate).
`-startoption` accepts nomount, mount, restrict, force and "open,recover".

## Verify
- [ ] `SELECT status FROM v$instance;` shows OPEN.
- [ ] The alert log shows the open completed without errors.

## Checked
Date: 2026-11-09. Confirmed against the Oracle 19c Database Administrator's Guide chapter "Starting Up and Shutting
Down a Database": startup modes, mount/open/read-only statements, restricted session, PFILE start, shutdown mode
behaviour and recovery, ORA-01013 handling, srvctl options. Removed (not on that page): ORA-00845/27102/00205/01157/
01113 diagnostics, specific uses of MOUNT such as ARCHIVELOG changes, `STARTUP UPGRADE`, `V$TRANSACTION.USED_UBLK`,
the ABORT-then-RESTRICT-then-IMMEDIATE sequence, the multitenant PDB `SAVE STATE` section, `dbstart`/`dbshut`/oratab.
Method: documentation only; no commands were run.

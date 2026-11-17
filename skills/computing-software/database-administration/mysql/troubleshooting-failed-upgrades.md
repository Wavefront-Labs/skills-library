---
id: computing-software.database-administration.mysql.troubleshooting-failed-upgrades
name: troubleshooting-failed-upgrades
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mysql-upgrade, mysql-downgrade, data-dictionary-upgrade, upgrade-failure, error-log, rollback]
level: advanced
status: docs-checked
description: "Recover when mysqld fails to start after an upgrade: the --upgrade modes, stale option files, table mismatches, and rolling back to the old server."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/upgrade-troubleshooting.html
  - https://dev.mysql.com/doc/refman/8.4/en/upgrading-what-is-upgraded.html
  - https://dev.mysql.com/doc/refman/8.4/en/server-options.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting failed MySQL upgrades

The **server itself** upgrades at startup in two steps: (1) the data dictionary, Performance Schema and
INFORMATION_SCHEMA; (2) everything else: system tables in the `mysql` schema, the `sys` schema and user schemas
(including `CHECK TABLE ... FOR UPGRADE` on every user table, which locks each table while it is processed and can be
slow). The data dictionary must be upgraded or the server exits; failures show in the error log.

## First checks
- Run `mysqld --print-defaults`. Anything beyond the program name means an active `my.cnf` that may carry options
  from the previous installation.
- A schema mismatch between a table's `.frm` file and the InnoDB data dictionary in an 8.3 instance can make the
  upgrade to 8.4 fail (for example from `.frm` corruption): dump and restore the affected tables, then retry.
- A loadable function (or stored function) that shares a name with a new built-in function becomes inaccessible:
  `DROP FUNCTION`, then `CREATE FUNCTION` under a different name.
- Compiled client programs that show `Commands out of sync` or core dumps after an upgrade were probably built
  against old header or library files: recompile against the new `mysql.h` and client library.
- A user-created schema named `sys` without a `sys.version` view makes step 2 fail: rename or remove it, then retry.

## The --upgrade option
Values: `AUTO` (default), `NONE`, `MINIMAL`, `FORCE`.
- `AUTO`: upgrades whatever is out of date (steps 1 and 2).
- `NONE`: no upgrade steps; the server exits with `Server shutting down because upgrade is required, yet prohibited
  by the command line option '--upgrade=NONE'` if the data dictionary is out of date.
- `MINIMAL`: step 1 only. Group Replication cannot be started afterwards because its system tables were not
  updated, so use it only for troubleshooting. Skips the `sys` check and table checking.
- `FORCE`: step 1 plus a forced step 2; startup takes longer because all objects in all schemas are checked, and
  missing system tables (help, time zone) are re-created.
Time zone tables are never loaded by the upgrade; load them yourself.

## Rolling back after a failed upgrade
If the upgrade fails because of issues covered in "Preparing Your Installation for Upgrade", the server reverts all
changes to the data directory. Then: remove all redo log files (`ib_logfile*`, in the data directory by default),
restart the old server on the existing data directory, fix the errors, do a slow shutdown with
`innodb_fast_shutdown=0`, and attempt the upgrade again.
If the data dictionary was already upgraded, the old server cannot use the datadir: restore the pre-upgrade backup
or fail back to a replica still on the old version (downgrades across series need logical dump/load).

## Prevention
- Run MySQL Shell's `util.checkForServerUpgrade()` before upgrading.
- Snapshot or back up the datadir right before starting new binaries.
- Upgrade a replica first.

## Checked
2026-11-01. Confirmed against the MySQL 8.4 manual: Upgrade Troubleshooting (3.13), What the MySQL Upgrade Process
Upgrades (3.4) and the `--upgrade` entry of Server Command Options. Removed as unconfirmed: the table of specific
log messages and removed options, the `mysql_upgrade` version note, the redo-log capacity advice, the exact
completion log line and the log-reading commands.
Method: documentation only; no commands were run.

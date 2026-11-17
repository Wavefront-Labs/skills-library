---
id: computing-software.database-administration.mysql.set-persist-and-mysqld-auto-cnf
name: set-persist-and-mysqld-auto-cnf
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mysql-8, set-persist, set-persist-only, mysqld-auto-cnf, reset-persist, persisted-variables, dynamic-configuration]
level: practitioner
status: verified
description: "Change MySQL 8 settings online and keep them across restarts with SET PERSIST / PERSIST_ONLY, inspect and undo them via mysqld-auto.cnf and RESET PERSIST."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/persisted-system-variables.html
  - https://dev.mysql.com/doc/refman/8.4/en/set-variable.html
  - https://dev.mysql.com/doc/refman/8.4/en/reset-persist.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SET PERSIST and mysqld-auto.cnf

**Goal:** tune a running server without a config-management drift surprise at the next restart.

## Forms
```sql
SET GLOBAL  max_connections = 800;          -- now, lost on restart
SET PERSIST max_connections = 800;          -- now AND written to mysqld-auto.cnf
SET PERSIST_ONLY innodb_log_buffer_size = 67108864;  -- read-only/static var: file only, effective after restart
RESET PERSIST max_connections;              -- remove from file (running value unchanged)
RESET PERSIST IF EXISTS max_connections;
RESET PERSIST;                              -- remove all
```
Privileges: `SYSTEM_VARIABLES_ADMIN` for `SET PERSIST`; `SYSTEM_VARIABLES_ADMIN` + `PERSIST_RO_VARIABLES_ADMIN` for `PERSIST_ONLY` (error 3630 without the second, confirmed on 9.7.4). `SET PERSIST max_connections = 800` followed by `SET GLOBAL max_connections = 777` leaves the file at 800 while the running value is 777 and `variables_info.VARIABLE_SOURCE` reads `DYNAMIC`; the 800 comes back on the next restart.

## Where it lives
`$datadir/mysqld-auto.cnf`, JSON, read **after** all my.cnf files, so it wins (checked: `max_connections=100` in my.ini, `SET PERSIST max_connections=800`, restart: the server came up with 800 and `VARIABLE_SOURCE = PERSISTED`, `VARIABLE_PATH` = the `mysqld-auto.cnf` path). Dynamic variables are stored under `mysql_dynamic_variables` and ones read early at startup (such as `max_connections` and `partial_revokes`) under `mysql_dynamic_parse_early_variables`. Inspect:
```sql
SELECT * FROM performance_schema.persisted_variables;
SELECT VARIABLE_NAME, VARIABLE_SOURCE, SET_TIME, SET_USER FROM performance_schema.variables_info WHERE VARIABLE_SOURCE = 'PERSISTED';
```
Disable reading it: `persisted_globals_load = OFF` in my.cnf.

## Gotchas
- Config management (Ansible/Puppet) writing my.cnf is silently overridden by a persisted value; standardise on one, or audit `persisted_variables` in CI.
- Some variables are non-persistible: `SET PERSIST version = 'x'`, `datadir` and `basedir` each failed with `ERROR 1238 Variable ... is a read only variable` (the manual's persisted-variables page lists the rules). `SET PERSIST` of an unknown name gives error 1193, and `RESET PERSIST nonexist` gives error 3615 (`RESET PERSIST IF EXISTS` suppresses that).
- Sensitive values: `persist_sensitive_variables_in_plaintext` defaults to ON on 9.7.4 (checked); the manual covers keyring-based protection for persisted credentials (not run here).
- Copying a datadir (clone, snapshot) copies `mysqld-auto.cnf` too, so persisted settings (including any `server_id`-like ones) follow it to a new server: check `performance_schema.persisted_variables` on every new replica.

## Verify
`SET PERSIST`, restart, `SELECT @@max_connections` keeps the value and `variables_info.VARIABLE_SOURCE = 'PERSISTED'`.

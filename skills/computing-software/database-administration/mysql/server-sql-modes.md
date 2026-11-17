---
id: computing-software.database-administration.mysql.server-sql-modes
name: server-sql-modes
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mariadb, sql-mode, strict-mode, strict-trans-tables, only-full-group-by, no-zero-date, error-for-division-by-zero, upgrade-compatibility]
level: practitioner
status: verified
description: "Set and audit MySQL sql_mode (STRICT_TRANS_TABLES, ONLY_FULL_GROUP_BY, NO_ZERO_DATE...) and fix apps that break when strict mode turns warnings into errors."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/sql-mode.html
  - https://mariadb.com/kb/en/sql-mode/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Server SQL modes

**Goal:** run with strict, standard-ish semantics without breaking legacy code by surprise.

## Defaults (MySQL 8.0/8.4/9.7)
`ONLY_FULL_GROUP_BY, STRICT_TRANS_TABLES, NO_ZERO_IN_DATE, NO_ZERO_DATE, ERROR_FOR_DIVISION_BY_ZERO, NO_ENGINE_SUBSTITUTION` (`@@global.sql_mode` on 9.7.4 returned exactly this list)

## What the important ones do
| Mode | Effect |
|---|---|
| `STRICT_TRANS_TABLES` / `STRICT_ALL_TABLES` | Invalid/out-of-range/truncated values error instead of being clipped with a warning |
| `ONLY_FULL_GROUP_BY` | Reject selecting non-aggregated columns not functionally dependent on GROUP BY |
| `NO_ZERO_DATE`, `NO_ZERO_IN_DATE` | Reject `0000-00-00` and `2026-00-10` (with strict) |
| `ERROR_FOR_DIVISION_BY_ZERO` | Division by zero errors on INSERT/UPDATE (with strict) |
| `NO_ENGINE_SUBSTITUTION` | Error if the requested engine is unavailable |
| `ANSI_QUOTES` | `"x"` is an identifier, not a string |
| `PIPES_AS_CONCAT` | `||` concatenates |
| `NO_BACKSLASH_ESCAPES` | Backslash is literal |

## Set it
```ini
[mysqld]
sql_mode = "ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION"
```
Session-level for a legacy app only: `SET SESSION sql_mode = REPLACE(@@sql_mode, 'ONLY_FULL_GROUP_BY', '');` (or via the connector's init command). On 9.7.4 that left `STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION`, and `SELECT v, t FROM sm GROUP BY v` then ran, while under the default it failed with `ERROR 1055 ... not functionally dependent on columns in GROUP BY clause`.

## Migrating a legacy app to strict
1. On staging, enable strict and run the test suite; also `SHOW WARNINGS` after writes in non-strict to find silent truncations.
2. Fix GROUP BY errors with proper aggregation or `ANY_VALUE(col)` (`SELECT v, ANY_VALUE(t) ... GROUP BY v` ran under the default mode).
3. Replace zero dates with NULL: `UPDATE t SET d = NULL WHERE d = '0000-00-00'` (needs a session without NO_ZERO_DATE: under the default mode that UPDATE failed with `ERROR 1292 Incorrect date value: '0000-00-00'`).
4. Turn on in production.

## Gotchas
- Stored routines, triggers and events capture `sql_mode` at creation time; recreate them after changing mode (`SHOW CREATE PROCEDURE` shows it).
- Replication: statement-format binlog events carry the session mode (`mysqlbinlog` showed `SET @@session.sql_mode=1168113696` as a number before the statement), and the manual recommends the same SQL mode on source and replica (it names partitioned tables as the problem case).
- Removed modes (`NO_AUTO_CREATE_USER`) in a config file prevent startup: on 9.7.4 `mysqld --sql-mode=NO_AUTO_CREATE_USER` aborted with `Error while setting value 'NO_AUTO_CREATE_USER' to 'sql_mode'`, and `SET sql_mode='NO_AUTO_CREATE_USER'` gives error 1231.

## Verify
`SELECT @@GLOBAL.sql_mode;` and `INSERT INTO t(tinyint_col) VALUES (999);` errors with 1264 Out of range. With `sql_mode=''` the same insert stored 127 with warning 1264; `INSERT ... VALUES ('abcdef')` into `VARCHAR(3)` gave error 1406 under strict and stored `abc` with warning 1265 otherwise; `INSERT ... VALUES (1/0)` gave error 1365 while `SELECT 1/0` returned NULL; `'0000-00-00'` and `'2026-00-10'` gave error 1292 (all run on 9.7.4). A routine created under `ANSI_QUOTES` showed `sql_mode = ANSI_QUOTES` in `SHOW CREATE PROCEDURE` and `information_schema.routines`, confirming the captured mode.

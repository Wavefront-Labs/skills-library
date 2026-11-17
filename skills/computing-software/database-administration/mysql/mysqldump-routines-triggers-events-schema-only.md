---
id: computing-software.database-administration.mysql.mysqldump-routines-triggers-events-schema-only
name: mysqldump-routines-triggers-events-schema-only
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mysqldump-routines, schema-only-dump, mysqldump, definer, stored-procedures, triggers, events, logical-backup]
level: practitioner
status: verified
description: "Dump MySQL stored routines, triggers, events and schema-only definitions with mysqldump, and fix DEFINER errors when restoring onto another server."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/mysqldump.html
  - https://dev.mysql.com/doc/refman/8.4/en/stored-objects-security.html
  - https://dev.mysql.com/doc/refman/8.4/en/mysqldump-definition-data-dumps.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dumping routines, triggers, events and schema-only dumps

## What mysqldump includes by default
| Object | Default | Flag |
|---|---|---|
| Tables + data | yes | `--no-data` / `-d` for schema only, `--no-create-info` / `-t` for data only |
| Triggers | yes | `--skip-triggers` |
| Stored procedures / functions | **no** | `--routines` / `-R` |
| Events | **no** | `--events` / `-E` |
| Views | yes (with the database) | — |

A "full" logical backup without `--routines --events` silently loses code. On 9.7.4 a dump of `shop` with only default options contained the trigger and the view but 0 `CREATE PROCEDURE`, `FUNCTION` or `EVENT` statements.

From a GTID-enabled server, mysqldump also prints `SET @@GLOBAL.GTID_PURGED=...` (even for a partial dump, with a warning on stderr); that line fails for an account without the needed privilege, so pass `--set-gtid-purged=OFF` when the target should not inherit GTIDs. Redirect stderr away from the dump file: a `2>&1` put the warnings into the SQL file in a test.

## Common dumps
```bash
# schema only, all code objects, no data
mysqldump --no-data --routines --events --triggers --databases shop > shop_schema.sql
# code objects only
mysqldump --no-data --no-create-info --no-create-db --skip-opt --routines --events --triggers shop > shop_code.sql
# data only, separately (e.g. for a schema-first restore)
mysqldump --no-create-info --skip-triggers --single-transaction shop > shop_data.sql
```
Schema dumps are what you diff in version control (`--skip-dump-date` and `--compact`-style options keep diffs clean; strip `AUTO_INCREMENT=` values with sed).

## DEFINER problems
Routines, views, triggers and events carry `DEFINER=` the account that created them. Restoring elsewhere fails or behaves oddly:
- `ERROR 1227: Access denied; you need (at least one of) the SUPER or SET_ANY_DEFINER privilege(s)` (9.7.4 wording; older 8.0 servers name `SET_USER_ID`) when the restoring account is not the definer. Grant `SET_ANY_DEFINER` (8.2+) or `SET_USER_ID` (older 8.0) to the restore account, or rewrite definers to the restore account itself. Rewriting to a third account (`shopowner`) still failed with 1227 until `SET_ANY_DEFINER` was granted.
- Creating a function as an account without `SUPER` while binary logging is on fails with `ERROR 1419 You do not have the SUPER privilege and binary logging is enabled` even if the function is declared DETERMINISTIC (set `log_bin_trust_function_creators=ON` or use a privileged restore account).
- Definer account missing on the target: objects are created but fail at runtime with `ERROR 1449 The user specified as a definer ('x'@'y') does not exist` (reproduced for a procedure).

Rewrite during restore:
```bash
sed -E 's/DEFINER=`[^`]+`@`[^`]+`/DEFINER=`app_owner`@`%`/g' shop_schema.sql | mysql shop
```
Find definers on the source first:
```sql
SELECT ROUTINE_SCHEMA, ROUTINE_NAME, DEFINER FROM information_schema.ROUTINES WHERE ROUTINE_SCHEMA = 'shop';
SELECT TRIGGER_NAME, DEFINER FROM information_schema.TRIGGERS WHERE TRIGGER_SCHEMA = 'shop';
SELECT TABLE_NAME, DEFINER, SECURITY_TYPE FROM information_schema.VIEWS WHERE TABLE_SCHEMA = 'shop';
```
MySQL Shell's `util.dumpSchemas` accepts `compatibility: ["strip_definers"]` for the same job (per the MySQL Shell dump-utilities page; Shell was not run here).

## Gotchas
- Events are dumped with the status they have on the source (a DISABLED event was recreated DISABLED); on a DR or test copy, disable the rest (`SET GLOBAL event_scheduler = OFF` before restore) so jobs don't run twice.
- Binary logging + creating a non-deterministic function needs `log_bin_trust_function_creators = ON` or a DETERMINISTIC/NO SQL/READS SQL DATA declaration, else `ERROR 1418` (reproduced with `RAND()`).
- `--routines` needs the `SHOW_ROUTINE` privilege or global SELECT on the dumping account: an account with only schema-level SELECT got a dump with 0 routines and no error, while adding `SHOW_ROUTINE` produced both. A restricted dump account on 9.7.4 also hit `SELECT command denied ... column_masking_policy` and (without `--no-tablespaces`) a missing `PROCESS` privilege; both are printed as errors.

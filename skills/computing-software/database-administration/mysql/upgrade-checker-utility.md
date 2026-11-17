---
id: computing-software.database-administration.mysql.upgrade-checker-utility
name: upgrade-checker-utility
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mysql-upgrade, upgrade-checker, util-check-for-server-upgrade, mysql-shell, mysql-8-4, deprecated-features, reserved-keywords]
level: practitioner
status: docs-checked
description: "Run MySQL Shell's util.checkForServerUpgrade before moving to 8.0/8.4, read its errors vs warnings, and fix the usual blockers (keywords, removed variables, auth plugins)."
sources:
  - https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-utilities-upgrade.html
  - https://dev.mysql.com/doc/refman/8.4/en/upgrade-prerequisites.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The upgrade checker

**Goal:** know every upgrade blocker before the maintenance window, not halfway
through it.

## Run it (use the Shell version equal to the target)
```bash
mysqlsh -- util checkForServerUpgrade admin@source-host:3306 \
  --target-version=8.4.0 --output-format=JSON --config-path=/etc/mysql/my.cnf > upgrade-check.json
```
Interactive: `util.checkForServerUpgrade('admin@source-host:3306', {targetVersion: '8.4.0'})`.
`targetVersion` accepts any release from 8.0.11 up to the release matching your
MySQL Shell version; if omitted, the Shell's own release is the target.
The account needs `PROCESS` and `SELECT`. `configPath` (`--config-path`) points at
the server's my.cnf; a check that needs the file fails without it.

## Read the result
The report ends with `Errors`, `Warnings` and `Notices` counts.
- **Errors**: must be corrected before upgrading.
- **Warnings**: the upgrade can succeed without clearing them, but clear them for
  better compatibility with the target release. Some manual checks are rated
  warning or notice.

## Usual findings (check names from the Shell docs)
| Check | Fix |
|---|---|
| `reservedKeywords`: object names that conflict with new reserved keywords | Quote with backticks in every query, or rename |
| `removedSysVars`: variables removed in the target version | Remove or replace in my.cnf before starting the new binary |
| `defaultAuthenticationPlugin`: older plugins such as `mysql_native_password` | Plan the move to `caching_sha2_password` |
| `nonNativePartitioning`: partitioned tables using non-native partitioning | Convert the tables |
| `utf8mb3`: utf8mb3 character set in use | Warning; utf8mb4 is recommended |
| `zeroDates`: zero date, datetime, timestamp values | Fix the data |
| `foreignKeyLength`: foreign key names longer than 64 characters | Rename in the source |

## Gotchas
- Run it against **every** server, including replicas with local-only config.
- It checks the server, not application SQL: test the app against the new version
  (CI with the new image, or replay captured traffic).
- The 8.4 prerequisites page also asks you to check views whose explicitly named
  columns exceed 64 characters (inspect with `SHOW CREATE VIEW`).
- Check the manual's Upgrade Paths page for which source versions may go straight
  to the target.

## Verify
Rerun until the report shows `Errors: 0`; keep the JSON report with the change
ticket.

## Checked
2026-11-01. Confirmed against the MySQL Shell 8.4 upgrade checker utility page and
the MySQL 8.4 "Preparing your installation for upgrade" page: command-line form and
options (`--target-version`, `--output-format=JSON`, `--config-path`), required
privileges, targetVersion range, error/warning/notice report, and the check names
in the table. Removed: RELOAD/EVENT/TRIGGER privilege claim, the specific example
keywords and removed variables, the 5.7-to-8.4 path and downgrade statements, the
orphaned .frm and SQL_CALC_FOUND_ROWS rows, the pt-upgrade suggestion.
Method: documentation only; no commands were run.

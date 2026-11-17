---
id: computing-software.web-development.ghost.ghost-mysql-troubleshooting-and-supported-databases
name: ghost-mysql-troubleshooting-and-supported-databases
category: computing-software
field: web-development
product: ghost
tags: [ghost, mysql, mariadb, sqlite, database, ansi-quotes, troubleshooting]
level: advanced
status: docs-checked
description: "Resolve common Ghost MySQL errors and choose the supported database: MySQL 8 in production, with MySQL 5 collation migration notes."
sources:
  - https://github.com/TryGhost/docs/blob/main/faq/troubleshooting-mysql-database.mdx
  - https://github.com/TryGhost/docs/blob/main/faq/supported-databases.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get Ghost talking to MySQL reliably.

Supported stack: Ubuntu, MySQL 8, NGINX and Node.js LTS. MySQL 8 stores JSON and has features that help performance. MariaDB is not the recommended path; migrate to MySQL 8.

Check what you run: `ghost ls`, then `ghost config database.client` prints `sqlite3` or `mysql`; for MySQL run `mysql --version`.

Errors and fixes:
- `ECONNREFUSED` on port 3306: MySQL is not running. `sudo service mysql start`, test with `mysql`, then if it followed `ghost install` re-run `ghost setup`.
- `ER_BAD_FIELD_ERROR`: may be caused by the `ANSI_QUOTES` SQL mode, or by combination modes such as `ANSI` that include it. Check `SELECT @@sql_mode` in mysql, then edit `my.cnf` to remove `ANSI_QUOTES` or `ANSI` from the `sql_mode` line.
- `ER_FK_COLUMN_CANNOT_CHANGE`: may be caused by a missing `STRICT_TRANS_TABLES` SQL mode; add it to the `sql_mode` line in `my.cnf`.
- `ER_TOO_BIG_ROWSIZE`: tables using the old `COMPACT` or `REDUNDANT` row format. Check with `show table status;`; take a backup, update MySQL, and run `ALTER TABLE <table> ROW_FORMAT=DYNAMIC;` per table (DYNAMIC is the supported format).
- `ER_CANT_CREATE_TABLE` ("Foreign key constraint is incorrectly formed") or `ER_FK_INCOMPATIBLE_COLUMNS`: foreign keys referencing tables with a different collation, usually after upgrading to MySQL 8. Make all tables use the default connection collation (`show variables like '%collation_connection%';`). The default utf8mb4 collation is `utf8mb4_general_ci` on 5.7 and `utf8mb4_0900_ai_ci` on 8.0.

Finding `my.cnf`: `mysql --help` lists the default option files in order; it may also be `.my.cnf`; if none exists, create one at the first listed location. The page gives the MySQL 8 default as `sql_mode=ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION`. These solutions are for the supported ghost-cli install.

Upgrading from MySQL 5 to 8: change Ghost table collations to the new default `utf8mb4_0900_ai_ci`. The FAQ gives a query that generates the required `ALTER TABLE` statements, then run them with `foreign_key_checks` set to 0 and back to 1; review them before running. SQLite3 in production: the FAQ strongly recommends a full reinstall of Ghost on MySQL 8.

## Checked

Date: 2026-11-07. Read in full (GitHub blob text, no imported snippets): faq/troubleshooting-mysql-database.mdx (76 lines) and faq/supported-databases.mdx (38 lines). Removed as unconfirmed: "restart MySQL" after editing `my.cnf` and the Verify step with `ghost doctor` and `ghost start`. Added the three other documented errors, my.cnf location and SQLite advice.
Method: documentation only; no commands were run.

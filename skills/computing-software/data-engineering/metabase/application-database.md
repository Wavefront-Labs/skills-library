---
id: computing-software.data-engineering.metabase.application-database
name: application-database
category: computing-software
field: data-engineering
product: metabase
tags: [application-database, mb-db-type, connection-uri, postgres, mysql, utf8mb4]
level: practitioner
status: docs-checked
description: "Configure Metabase's application database: supported Postgres, MySQL and MariaDB versions, MB_DB_* variables, connection URI, utf8mb4 needs, H2 files and SSL traps."
sources:
  - https://www.metabase.com/docs/latest/installation-and-operation/configuring-application-database
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Supported: PostgreSQL (recommended), MySQL 8.4.0+ or MariaDB 10.6.0+ (the `utf8mb4` character set is required). ApsaraDB MySQL is not supported. H2 is the default and is for local demos only.

Variables: `MB_DB_TYPE` (`postgres`, `mysql` or `h2`), `MB_DB_HOST`, `MB_DB_PORT`, `MB_DB_DBNAME`, `MB_DB_USER`, `MB_DB_PASS`. `MB_DB_CONNECTION_URI` takes a full JDBC string for extra parameters and can be combined with `MB_DB_USER` and `MB_DB_PASS`, which helps when a password has special characters. `MB_DB_FILE` points at the H2 file.

Setup: Metabase does not create the database.
- Postgres: `createdb --encoding=UTF8 <name>`.
- MySQL: `CREATE DATABASE ... CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci`.
Launch with `java --add-opens java.base/java.nio=ALL-UNNAMED -jar metabase.jar`. Configuration is read at startup, so the application database cannot change while running.

H2: created next to the JAR if nothing else is configured, as `metabase.db.mv.db` (or `.h2.db`) plus `metabase.db.trace.db`. Omit the extension in `MB_DB_FILE`.

SSL: since v0.38 Postgres no longer uses `NonValidatingFactory` by default. Prefer `MB_DB_CONNECTION_URI` with `sslmode=verify-ca` and `sslrootcert=<path>`. The `ssl=true&sslfactory=org.postgresql.ssl.NonValidatingFactory` fallback is for troubleshooting only.

Gotcha: the page's MySQL URI example uses port 5432, which looks like a typo; MySQL normally uses 3306.

## Checked
2026-11-03. Confirmed against the Metabase docs page Installation and operation, Configuring the Metabase application database: Postgres recommended, MySQL 8.4.0 / MariaDB 10.6.0 minimums and utf8mb4, ApsaraDB MySQL unsupported, MB_DB_* variables, connection URI with separate user and password, createdb and CREATE DATABASE examples, H2 files and MB_DB_FILE extension rule, pre-0.38 SSL change and NonValidatingFactory warning. The MySQL 5432 port in the page example is as written there. Nothing removed.
Method: documentation only; no commands were run.

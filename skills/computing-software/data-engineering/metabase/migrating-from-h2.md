---
id: computing-software.data-engineering.metabase.migrating-from-h2
name: migrating-from-h2
category: computing-software
field: data-engineering
product: metabase
tags: [h2-migration, load-from-h2, production-database, backup, same-version]
level: advanced
status: docs-checked
description: "Migrate Metabase from the H2 application database to Postgres or MySQL with load-from-h2: detection, version rule, JAR and Docker steps, and common failure modes."
sources:
  - https://www.metabase.com/docs/latest/installation-and-operation/migrating-from-h2
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Detect H2: as admin call `GET /api/bug-reporting/details`; if `application-database` is not `postgres` or `mysql`, you are on H2.

Targets: PostgreSQL 14 (preferred), MySQL 8.4.0 or MariaDB 10.6.0 with `utf8mb4`, `utf8mb4_unicode_ci` and `innodb_large_prefix=ON`.

Version rule: migrate with the same Metabase version that last used the H2 file; upgrade only afterwards.

JAR steps:
1. Check the machine can reach the target database, which must be empty.
2. Stop Metabase so no content is created mid-migration.
3. Back up the H2 file.
4. Run:
```
export MB_DB_TYPE=postgres
export MB_DB_CONNECTION_URI="jdbc:postgresql://<host>:5432/metabase?user=<username>&password=<password>"
java --add-opens java.base/java.nio=ALL-UNNAMED -jar metabase.jar load-from-h2 /path/to/metabase.db
```
5. Start Metabase with the same `MB_DB_*` settings and without `load-from-h2`.
6. Keep the old H2 file.

Docker: back up the H2 file from the container, stop it, download the same-version JAR beside the file, run `load-from-h2` (it migrates then exits), and start a new container with `MB_DB_TYPE`, `MB_DB_DBNAME`, `MB_DB_PORT`, `MB_DB_USER`, `MB_DB_PASS`, `MB_DB_HOST`.

Gotchas:
- The file is often `metabase.db.mv.db`, but the command takes `/path/to/metabase.db` without the extension.
- Leaving `load-from-h2` in the startup command is wrong.
- With `MB_DB_AUTOMIGRATE=false`, Metabase prints the SQL and will not start until you apply it.

## Checked
2026-11-03. Confirmed against the Metabase docs page Installation and operation, Migrating to a production application database: /api/bug-reporting/details detection, minimum versions (PostgreSQL 14, MySQL 8.4.0, MariaDB 10.6.0) and required MySQL settings, same-version rule, JAR and Docker steps, load-from-h2 command and path without extension, MB_DB_AUTOMIGRATE=false. Nothing removed.
Method: documentation only; no commands were run.

---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-databases
name: woodpecker-databases
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [database, sqlite, postgres, mysql]
level: practitioner
status: docs-checked
description: "Choose and configure the Woodpecker database: SQLite, MySQL/MariaDB or PostgreSQL."
sources: ["https://woodpecker-ci.org/docs/administration/configuration/server"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker database configuration

The default engine is embedded SQLite stored under `/var/lib/woodpecker/`. In containers mount a volume there to persist it. For others, set the driver and datasource.

MySQL/MariaDB:

```ini
WOODPECKER_DATABASE_DRIVER=mysql
WOODPECKER_DATABASE_DATASOURCE=root:password@tcp(1.2.3.4:3306)/woodpecker?parseTime=true
```

PostgreSQL (version 11 or higher):

```ini
WOODPECKER_DATABASE_DRIVER=postgres
WOODPECKER_DATABASE_DATASOURCE=postgres://root:password@1.2.3.4:5432/woodpecker?sslmode=disable
```

The driver defaults to `sqlite3`. `WOODPECKER_DATABASE_DATASOURCE_FILE` reads the connection string from a file.

Operational facts:

- Woodpecker does not create the database for MySQL or Postgres; run `CREATE DATABASE` yourself.
- It handles schema migration automatically, including initial tables, unless release notes say otherwise.
- It does no archival and no backups; use your database vendor's tools. Expect the stored logs to grow the database considerably.
- Pool tuning: `WOODPECKER_DATABASE_MAX_CONNECTIONS` (100), `WOODPECKER_DATABASE_IDLE_CONNECTIONS` (2), `WOODPECKER_DATABASE_CONNECTION_TIMEOUT` (3 seconds), `WOODPECKER_DATABASE_MAX_RETRIES` (10).
- `WOODPECKER_LOG_STORE` can move logs to JSON `file` storage or an `addon`.

Plan capacity for log growth, and use your database vendor's tools for backups and archival, because Woodpecker offers neither. Set the driver and datasource together, and prefer the file variant for passwords embedded in the connection string.

## Checked

2026-11-03. Read the Woodpecker server configuration page and confirmed database driver and datasource settings and the SQLite default. Nothing removed. 

Method: documentation only; no commands were run.

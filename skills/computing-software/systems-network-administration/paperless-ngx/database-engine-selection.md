---
id: computing-software.systems-network-administration.paperless-ngx.database-engine-selection
name: database-engine-selection
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, postgresql, mariadb, sqlite, paperless-dbengine, database]
level: practitioner
status: docs-checked
description: "Choose and configure the Paperless-ngx database: PAPERLESS_DBENGINE values, connection variables and defaults, and the explicit-engine rule in v3."
sources:
  - "https://docs.paperless-ngx.com/configuration/"
  - "https://docs.paperless-ngx.com/migration-v3/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Database engine

By default Paperless uses SQLite, stored at `data/db.sqlite3` (always `<PAPERLESS_DATA_DIR>/db.sqlite3`). PostgreSQL is recommended for multi-user or higher-throughput installs; MariaDB is also supported.

## Settings
- `PAPERLESS_DBENGINE`: `sqlite` (default), `postgresql` or `mariadb`.
- `PAPERLESS_DBHOST`: required for PostgreSQL and MariaDB.
- `PAPERLESS_DBPORT`: defaults to 5432 for PostgreSQL and 3306 for MariaDB.
- `PAPERLESS_DBNAME`, `PAPERLESS_DBUSER`, `PAPERLESS_DBPASS`: all default to `paperless`.

```yaml
PAPERLESS_DBENGINE: postgresql
PAPERLESS_DBHOST: postgres
```

## v3 change
In v2 the engine was inferred from `PAPERLESS_DBHOST`. In v3 PostgreSQL and MariaDB users must set `PAPERLESS_DBENGINE` explicitly. SQLite needs no change.

## Versions
Django-supported PostgreSQL and MariaDB versions work; the minimum PostgreSQL is 14 as of v2.18. Back up before any major database upgrade and follow the database vendor's instructions. An exporter and importer round trip with `--data-only` into a fresh database also works, provided settings and paths are unchanged.

The configuration docs warn that MariaDB comes with caveats; see the MySQL Caveats section of the advanced usage page.

## Checked
2026-11-04. Compared with the Database section of configuration, the v3 migration page and the Database Upgrades part of administration (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: SQLite default and file location, engine values, DBHOST requirement, port defaults, name/user/password defaults, explicit engine rule in v3, minimum PostgreSQL 14 from v2.18, exporter/importer --data-only route. Removed: the "change the password" advice and the pointer to a MariaDB caveats skill (replaced with the docs' own MySQL Caveats reference).

Method: documentation only; no commands were run.

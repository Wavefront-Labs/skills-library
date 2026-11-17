---
id: computing-software.web-development.directus.config-database-connection
name: config-database-connection
category: computing-software
field: web-development
product: directus
tags: [database-config, db-client, db-ssl-ca, db-exclude-tables]
level: practitioner
status: docs-checked
description: "Set Directus DB_* variables for pg, mysql, mssql, oracledb, sqlite3 or cockroachdb, including connection string, SSL CA, pool options and excluded tables."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/configuration/database.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`DB_CLIENT` is required: `pg` (or `postgres`), `mysql`, `oracledb`, `mssql`, `sqlite3`, `cockroachdb`.

- For `pg`, `mysql`, `oracledb`, `mssql`: set `DB_HOST`, `DB_PORT`, `DB_DATABASE`, `DB_USER`, `DB_PASSWORD`.
- For `sqlite3`: set `DB_FILENAME`.
- For `pg` you may use `DB_CONNECTION_STRING` instead; it makes Directus ignore the other connection settings.
- `DB_EXCLUDE_TABLES`: comma list of tables Directus ignores completely (default `spatial_ref_sys,sysdiagrams`).
- `DB_CHARSET` / `DB_CHARSET_NUMBER`: MySQL or MariaDB charset (default `UTF8_GENERAL_CI`).
- `DB_VERSION`: only for non-standard databases reached via the PostgreSQL adapter.
- `DB_HEALTHCHECK_THRESHOLD`: ms, default `150`.

All `DB_*` variables are passed to the Knex `connection` config, so you can add more. `DB_POOL__*` goes to tarn.js. `DB_SSL__*` goes to the driver, e.g. `DB_SSL__CA` for a custom CA that is not in Node's trust store; `DB_SSL__CA_FILE` loads it from a file.

```
DB_CLIENT="pg"
DB_CONNECTION_STRING="postgresql://user:pass@db-host/directus"
```

## Checked

2026-11-04: DB_CLIENT values, required connection variables, DB_CONNECTION_STRING, DB_EXCLUDE_TABLES, DB_CHARSET, DB_VERSION, DB_HEALTHCHECK_THRESHOLD, Knex, DB_POOL__ and DB_SSL__ notes confirmed against the Directus database configuration page. Removed an unsupported Verify line.

Method: documentation only; no commands were run.

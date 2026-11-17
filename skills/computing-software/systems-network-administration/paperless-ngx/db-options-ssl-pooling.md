---
id: computing-software.systems-network-administration.paperless-ngx.db-options-ssl-pooling
name: db-options-ssl-pooling
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, paperless-db-options, ssl, connection-pool, postgresql, mariadb]
level: advanced
status: docs-checked
description: "Use PAPERLESS_DB_OPTIONS for TLS, timeouts and pooling in v3, replacing the removed DBSSL and DB_POOLSIZE variables."
sources:
  - "https://docs.paperless-ngx.com/configuration/"
  - "https://docs.paperless-ngx.com/migration-v3/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PAPERLESS_DB_OPTIONS

One comma-separated `key=value` string passes driver options to the database. Dot notation makes nested options: `pool.max_size=20` sets `OPTIONS["pool"]["max_size"]`. Unknown keys go to the driver without validation, so a typo is silently ignored.

## Examples
```bash
# PostgreSQL
PAPERLESS_DB_OPTIONS="sslmode=require,sslrootcert=/certs/ca.pem,pool.max_size=5"
# MariaDB
PAPERLESS_DB_OPTIONS="ssl_mode=REQUIRED,ssl.ca=/certs/ca.pem"
# either
PAPERLESS_DB_OPTIONS="connect_timeout=10"
```

## Replacing removed variables
- `PAPERLESS_DBSSLMODE` becomes `sslmode` (PostgreSQL) or `ssl_mode` (MariaDB).
- `PAPERLESS_DBSSLROOTCERT` becomes `sslrootcert` or `ssl.ca`.
- `PAPERLESS_DB_POOLSIZE` becomes `pool.max_size` (PostgreSQL only).
- `PAPERLESS_DB_TIMEOUT` becomes `timeout` (SQLite) or `connect_timeout`.

## Sizing pools
Make PostgreSQL `max_connections` at least `(web_workers + celery_workers) * pool.max_size` plus a safety margin.

## Engine defaults
- SQLite starts with WAL journal mode and a 5 second busy timeout. Override PRAGMAs with `init_command=...`, separating PRAGMAs with `;` and options with `,`.
- MariaDB uses READ COMMITTED, which needs `binlog_format=ROW` when binary logging is on.

## Migration tips
- The v3 migration guide says the old variables continue to function for now and log a deprecation warning at startup, while the configuration reference marks them "Removed in v3". Move to `PAPERLESS_DB_OPTIONS` either way.
- Options differ by driver: see the libpq connection parameters (PostgreSQL), MariaDB Connector/Python (MariaDB) and SQLite PRAGMA statements for the keys each accepts.
- Several options combine in one value, for example `sslmode=require,sslrootcert=/certs/ca.pem,pool.max_size=10`.

## Checked
2026-11-04. Compared with PAPERLESS_DB_OPTIONS and the removed DB variables in configuration, and the Database Advanced Options table of the v3 migration page (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: string format, dot notation, pass-through of unknown keys, examples, every old-to-new mapping, pool sizing formula, SQLite WAL and 5 second busy timeout, init_command separators, MariaDB READ COMMITTED and binlog_format=ROW. Removed: "restart after any change" and "bad certificate path shows as a connection error" (not stated). Reworded the deprecation bullet to reflect that the migration guide and configuration reference differ on whether the old variables still work.

Method: documentation only; no commands were run.

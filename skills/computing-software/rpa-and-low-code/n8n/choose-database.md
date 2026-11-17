---
id: computing-software.rpa-and-low-code.n8n.choose-database
name: choose-database
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, database, postgresql, sqlite, db-type, tls]
level: practitioner
status: docs-checked
description: "Choose n8n's database: SQLite default, PostgreSQL 16 to 18 support policy, DB_POSTGRESDB variables with defaults, TLS modes and required privileges."
sources:
  - https://docs.n8n.io/deploy/host-n8n/configure-n8n/choose-n8ns-database
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: configure PostgreSQL (or keep SQLite) correctly.

SQLite is the default for self-hosting (`~/.n8n/database.sqlite`). On n8n Cloud, SQLite serves Starter, Pro and legacy Enterprise and PostgreSQL serves Enterprise Scaling. Shared variable: `DB_TABLE_PREFIX`.

## Supported PostgreSQL
The latest two actively maintained majors (17 and 18 as of July 2026) plus one older (16); run the latest minor. Amazon Aurora PostgreSQL is experimental and untested; AlloyDB, CockroachDB and YugabyteDB are not supported.

## Variables
`DB_TYPE=postgresdb`, `DB_POSTGRESDB_DATABASE` (default `n8n`), `_HOST` (`localhost`), `_PORT` (5432), `_USER` (`postgres`), `_PASSWORD` (empty), `_SCHEMA` (`public`), `DB_POSTGRESDB_SSL_CA`, `_SSL_CERT`, `_SSL_KEY`, `DB_POSTGRESDB_SSL_REJECT_UNAUTHORIZED` (default true).
```bash
export DB_TYPE=postgresdb
export DB_POSTGRESDB_DATABASE=n8n
export DB_POSTGRESDB_HOST=postgresdb
export DB_POSTGRESDB_PORT=5432
export DB_POSTGRESDB_USER=n8n
export DB_POSTGRESDB_PASSWORD=n8n
export DB_POSTGRESDB_SCHEMA=n8n
n8n start
```

## TLS
Nothing declared means `SSL=off`. CA plus the unauthorized flag gives SSL on with server verification (opportunistic encryption is not supported). Adding cert and key enables client TLS authentication.

## Privileges
n8n must create and modify table schemas: create the database and user and `GRANT ALL PRIVILEGES ON DATABASE n8n-db TO n8n-user;`.

## Checked

2026-11-03. Read against the official n8n documentation pages:
- https://docs.n8n.io/deploy/host-n8n/configure-n8n/choose-n8ns-database

Confirmed: parameter names, defaults, limits, commands and behaviour in this skill match those pages. Nothing removed; every concrete claim matched the page.

Method: documentation only; no commands were run.

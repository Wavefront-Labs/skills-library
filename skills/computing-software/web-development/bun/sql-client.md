---
id: computing-software.web-development.bun.sql-client
name: sql-client
category: computing-software
field: web-development
product: bun
tags: [bun-sql, postgres-client, mysql-client, database-url]
level: practitioner
status: docs-checked
description: "Use Bun.SQL for PostgreSQL, MySQL/MariaDB and SQLite: tagged templates, connection options, pooling, reserved connections, env vars and sharp edges."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/runtime/sql.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
import { sql, SQL } from "bun";
const users = await sql`SELECT * FROM users WHERE id = ${id}`; // bound parameter, escaped
const pg = new SQL("postgres://user:pass@localhost:5432/app");
const my = new SQL("mysql://user:pass@localhost:3306/app");
const lite = new SQL("sqlite://app.db");
const db = new SQL({ url: "postgres://app@db.internal/shop", max: 20, idleTimeout: 30, tls: { ca: Bun.file("./ca.pem") } });
{ using conn = await sql.reserve(); await conn`SELECT 1`; } // dedicated connection
```

Options: `adapter`, `hostname`, `port`, `username`, `password`, `database`, `tls` (false default), `max` (10), `idleTimeout`, `maxLifetime`, `connectionTimeout` (30 s), `prepare` (PostgreSQL), `transform` (for example `SQL.camel`).

Precedence: explicit option, URL, `DATABASE_URL`, field variables (`PGHOST`, `MYSQL_HOST`, `SQLITE_URL`...), defaults. `sql.close({ timeout: 0 })` closes immediately.

Gotchas:
- Queries are lazy; an unawaited query never runs. `.raw()` and `.values()` must be called before awaiting.
- With SQLite, a bare filename needs `{ adapter: "sqlite" }`.
- MySQL 8 `caching_sha2_password` over plain TCP needs TLS or `allowPublicKeyRetrieval: true` (a unix socket needs neither).
- Empty `IN` lists give `IN (NULL)` (matches nothing) on PostgreSQL and MySQL; SQLite `NOT IN ()` matches every row.
- Use `sql.json(value)` for non-object JSON values. `listen`/`notify` and `COPY` are PostgreSQL only.
- A rejection with no handler becomes an unhandled rejection.

## Checked

2026-11-04. Confirmed against the Bun docs page runtime/sql (read in sections): adapter selection, connection options and defaults (tls false, max 10, connectionTimeout 30), idleTimeout and maxLifetime, setting precedence, DATABASE_URL and PG*/MYSQL_*/SQLITE_URL variables, sqlite filename needing the adapter option, allowPublicKeyRetrieval, empty IN list behaviour, sql.json, listen/notify and COPY being PostgreSQL only, lazy queries, raw/values before await, unhandled rejection, sql.reserve and close timeout 0, transform presets. Qualified the caching_sha2_password gotcha to plain TCP as the page says.
Method: documentation only; no commands were run.

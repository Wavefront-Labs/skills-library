---
id: computing-software.software-engineering.v-lang.v-db-postgres-and-mysql
name: v-db-postgres-and-mysql
category: computing-software
field: software-engineering
product: v-lang
tags: [v-db-postgres-and-mysql, orm-and-databases, postgres, db.pg, pg.connect, postgresql, mysql, db.mysql, exec_param, connection, v-lang]
level: practitioner
status: draft
description: "Connect to PostgreSQL with pg.connect, run exec_param queries, handle result rows and pools, and note the MySQL module."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# db.pg and db.mysql

Goal: talk to server databases.

- `import db.pg`; `mut db := pg.connect(pg.Config{ host: 'localhost', port: 5432, user: os.getenv('PGUSER'), password: os.getenv('PGPASSWORD'), dbname: 'app' })!`; `defer { db.close() }`.
- Query: `rows := db.exec_param('SELECT id, name FROM users WHERE age > $1', '18')!`; each `row.vals[i]` is `?string`; `db.exec('...')!`; `db.exec_one(...)!`.
- ORM works the same with `sql db { ... }` using the pg handle.
- MySQL: `import db.mysql`; `mysql.connect(mysql.Config{ host, port, username, password, dbname })!` with similar `query`/`exec` methods.
- Requires libpq (`libpq-dev`) / libmysqlclient at build time and runtime.
- Credentials via env/secrets manager, never in source.

Gotchas:
- Each connection is not thread safe; use one per thread or a pool (`pool` modules; confirm).
- Values come back as strings; convert with `.int()` or `strconv`.

Verify: run against a local Docker postgres and select 1.

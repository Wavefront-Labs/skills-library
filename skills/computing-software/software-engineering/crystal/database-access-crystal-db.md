---
id: computing-software.software-engineering.crystal.database-access-crystal-db
name: database-access-crystal-db
category: computing-software
field: software-engineering
product: crystal
tags: [database-access-crystal-db, frameworks, crystal-db, postgres, sqlite3, mysql, database, query-one, query-all, transaction, connection-pool, prepared-statements, db-open, crystal]
level: practitioner
status: draft
description: "Connect to PostgreSQL, MySQL or SQLite via crystal-db drivers, run queries with query_one and query_all, params and transactions."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Database access with crystal-db

Goal: query a database.

```crystal
require "db"
require "pg"
DB.open(ENV["DATABASE_URL"]) do |db|   # URL from the environment, never in source
  db.exec "insert into users(name) values ($1)", "Ada"
  id, name = db.query_one "select id, name from users where id = $1", 1, as: {Int32, String}
  db.query_each("select name from users") { |rs| puts rs.read(String) }
  users = db.query_all "select id, name from users", as: {Int32, String}
  db.transaction { |tx| tx.connection.exec "update ..." }
end
```
- Placeholders: `$1` for Postgres, `?` for MySQL/SQLite; always parameterise, never interpolate.
- Pool options in the URL (`max_pool_size`, `initial_pool_size`, `checkout_timeout`).
- Map rows to objects with `DB::Serializable` (`include DB::Serializable`, `query_all ..., as: User`).

Gotchas:
- Nullable columns need `String?` types or reads raise.
- Keep `DB.open` global and reuse it; do not open per request.
- Close result sets; block forms do it for you.

Verify: run against a local SQLite file in a spec.

---
id: computing-software.software-engineering.scala.sc-database-access
name: sc-database-access
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-http-db, database-access]
level: practitioner
status: draft
description: "Access SQL from Scala with Doobie or Slick, bind parameters and manage transactions and pools."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Slick, Doobie and JDBC
- Doobie: ``sql"select name from users where id = $id".query[String].unique.transact(xa)``; interpolated values become bound parameters, not string concatenation.
- Slick: `table.filter(_.id === id).result`, run with `db.run(...)`; compose with `DBIO` for transactions (`.transactionally`).
- Use HikariCP for pooling (`HikariTransactor`); run migrations with Flyway.
- Never build SQL by string concatenation; use `Fragment` helpers for dynamic parts.
Verify: integration tests against a container database.

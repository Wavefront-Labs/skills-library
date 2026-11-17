---
id: computing-software.software-engineering.groovy.sql-queries-params
name: sql-queries-params
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, sql-queries-params, groovy-sql]
level: practitioner
status: docs-checked
description: "Use groovy.sql.Sql: newInstance and withInstance, execute with GString or ? placeholders, eachRow, firstRow, rows and paging, named parameters."
sources:
  - https://groovy-lang.org/databases.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sql queries with bound parameters
- Connect with `Sql.newInstance(url, user, password, driver)`; `Sql.withInstance(url, user, password, driver) { sql -> ... }` closes the connection for you.
- `sql.execute` has a variant taking a GString and another taking a list of parameters; `executeInsert` and `executeUpdate` have similar variants. `?` placeholders with a parameter list use a `PreparedStatement`, which avoids the risk of SQL injection. The guide recommends the GString and list-of-parameters variants for the same reason.
- `executeInsert` returns a list of all generated keys.
- Read with `query`, `eachRow`, `firstRow` or `rows`. `rows(sql)` returns a list of map-like rows (`GroovyRowResult`); the row abstraction has case-insensitive keys, and negative indices count column numbers from the right. `firstRow('SELECT COUNT(*) AS num FROM Author').num` returns a scalar.
- Paging: `sql.rows(query, 1, 3)` takes a starting position and a page size.
- `eachRow` also has a form with a metadata closure before the row closure.
- Named and named-ordinal parameters (colon form and question mark form) have their own section of the guide.

## Gotchas
- Do not build SQL by concatenating user input into a plain String.

## Checked

2026-11-03. Confirmed against the Working with a relational database chapter (connecting, execute, executeInsert, reading rows, paging, metadata closure, named parameters) and the `Sql` source (`GroovyRowResult`). Removed: the H2 dependency, version and driver details, the `Sql.expand` claim, the `rows(query)` shape description beyond what the guide states, and the code snippet and self-check.

Method: documentation only; no commands were run.

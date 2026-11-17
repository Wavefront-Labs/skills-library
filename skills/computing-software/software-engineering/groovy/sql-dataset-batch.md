---
id: computing-software.software-engineering.groovy.sql-dataset-batch
name: sql-dataset-batch
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, sql-dataset-batch]
level: advanced
status: docs-checked
description: "Sql withTransaction, withBatch with a size and a prepared statement, and groovy.sql.DataSet for closure-based queries."
sources:
  - https://groovy-lang.org/databases.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transactions, batches and DataSet
- `sql.withTransaction { ... }` runs the closure in a transaction: operations inside it are never seen half-done outside, and if something goes wrong, earlier operations in the block are rolled back.
- `sql.withBatch(3) { stmt -> ... }` groups statements into batches of the given size. A prepared form takes the SQL as well: `sql.withBatch(3, qry) { ps -> ... }`; prepared statements can be combined with batches.
- `executeInsert` returns a list of the generated keys.
- `groovy.sql.DataSet` is a small ORM-like layer: `sql.dataSet('Author')` gives a DataSet whose `findAll { ... }` closures (chainable) and `sort { ... }` build the query, and `rows()` runs it.

## Checked

2026-11-03. Confirmed against the databases chapter (Working with transactions, batches and prepared statements, Using DataSets). Removed: the thread-safety claim, the `eachRow` metadata-signature gotcha, the claim about generated keys being a list of lists, the DataSet predicate limitation, and the self-check.

Method: documentation only; no commands were run.

---
id: computing-software.software-engineering.clojure.next-jdbc-execute-plan-transactions-pooling
name: next-jdbc-execute-plan-transactions-pooling
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, next.jdbc, jdbc, sql, execute, plan, with-transaction, hikaricp, result-set-builder, postgresql, next-jdbc-queries, clojure-database]
level: practitioner
status: docs-checked
description: "Query SQL databases with next.jdbc (get-datasource, execute!, execute-one!, plan, with-transaction), use a pooled DataSource, and control result shapes with builders."
sources: ["https://github.com/seancorfield/next-jdbc", "https://cljdoc.org/d/com.github.seancorfield/next.jdbc/CURRENT"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# next.jdbc

**Goal:** talk to SQL databases with a thin, fast layer over JDBC.

```clojure
(require '[next.jdbc :as jdbc] '[next.jdbc.result-set :as rs])
(def ds (jdbc/get-datasource {:dbtype "postgresql" :dbname "app" :host "localhost" :user "u" :password pw}))
(jdbc/execute! ds ["select * from users where id = ?" 42])          ; vector of qualified-key maps
(jdbc/execute-one! ds ["select * from users where id = ?" 42])
(jdbc/execute! ds ["select * from t"] {:builder-fn rs/as-unqualified-maps})
(jdbc/with-transaction [tx ds] (jdbc/execute! tx ["update ..."]) (jdbc/execute! tx ["update ..."]))
(reduce (fn [n row] (inc n)) 0 (jdbc/plan ds ["select id from big_table"]))   ; reduce rows without realising maps
```
- Everything starts from a `javax.sql.DataSource`: `get-datasource` builds one from a db-spec map or JDBC URL, or
  create a pooled one with your preferred library (the README names c3p0 and hikari-cp). Add the JDBC driver
  dependency for your database.
- `execute!` returns a vector of realised maps with qualified keys of the form `:<table>/<column>` (unqualified
  when a value has no source table); `rs/as-maps` is the default builder, with `rs/as-unqualified-maps`,
  `rs/as-arrays`, `rs/as-unqualified-arrays` and lower-case variants as alternatives via `:builder-fn`.
- `execute-one!` returns a single realised map (the first row, first generated-keys result, or
  `{:next.jdbc/update-count N}`) and suits most non-query statements.
- `plan` returns an `IReduceInit` that executes the statement when reduced and cleans up even if the reduction
  short-circuits with `reduced`; the README says to consider it first for queries.
- Use `get-connection` inside `with-open` to reuse one connection for several calls.
- Always parameterise with `?` placeholders; never concatenate user input into SQL.

## Failure modes
- Connection leaks when using `get-connection` without `with-open`.
- Expecting `execute!` to stream: it realises the whole result in memory; use `plan` for large result sets.

## Self-check
Run a query with `execute!` and again with `plan` and confirm the key shapes you rely on.

## Checked
2026-11-08. Confirmed on the next.jdbc README and the cljdoc home page (the same README): DataSource-first model, `get-datasource`, pooling libraries, `execute!`, `execute-one!`, `plan`, `transact`/`with-transaction`, builder functions, qualified keys, `with-open` with `get-connection`. Removed: `:return-keys`, `next.jdbc.connection/->pool`, HikariCP coordinates, the `rs/as-unqualified-lower-maps` name, rollback and nested-transaction behaviour, and the ds-versus-tx pitfall, none of which the README states.
Method: documentation only; no commands were run.

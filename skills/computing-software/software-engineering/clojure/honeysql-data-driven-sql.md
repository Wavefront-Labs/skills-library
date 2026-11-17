---
id: computing-software.software-engineering.clojure.honeysql-data-driven-sql
name: honeysql-data-driven-sql
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, honeysql, sql, query-builder, format, helpers, where, join, parameters, dsl, honeysql-sql-dsl]
level: practitioner
status: draft
description: "Build parameterised SQL from Clojure data with HoneySQL (sql/format, :select/:from/:where, helpers, joins, upsert) and execute it with next.jdbc."
sources: ["https://github.com/seancorfield/honeysql"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HoneySQL

**Goal:** compose queries as data and avoid string concatenation.

```clojure
(require '[honey.sql :as sql] '[honey.sql.helpers :as h])
(sql/format {:select [:u.id :u.name] :from [[:users :u]]
             :where [:and [:= :u.active true] [:> :u.age 18]]
             :order-by [[:u.name :asc]] :limit 10})
;=> ["SELECT u.id, u.name FROM users AS u WHERE (u.active = ?) AND (u.age > ?) ORDER BY u.name ASC LIMIT ?" true 18 10]

(-> (h/select :*) (h/from :t) (h/where [:in :id [1 2 3]]) sql/format)
(sql/format {:insert-into :t :values [{:a 1 :b 2}] :on-conflict :a :do-update-set [:b]}
            {:dialect :ansi})
(jdbc/execute! ds (sql/format q))
```
- `format` returns a vector `[sql & params]` ready for next.jdbc; values become `?` parameters automatically.
- Identifiers come from keywords; never put user input into keywords or `[:raw ...]` (injection).
- Use `[:raw "..."]` and `:inline` options sparingly; they bypass parameterisation.
- Namespaced keywords (`:users/id`) become `users.id`; use `{:quoted true}` option for reserved words.
- Dialect and quoting are options of `format` (`{:dialect :mysql}`, `{:quoted true}`).
- Group by, joins (`:join`, `:left-join`), CTEs (`:with`), and window functions are supported (check version docs).
- Use raw SQL files via libraries like HugSQL if you prefer SQL-first.

## Failure modes
- Unknown clause keys silently ignored in older versions; read the docs for your version.
- Mixing version 1.x and 2.x syntax (`honeysql.core` vs `honey.sql`).

## Self-check
Print the `format` output for a query with a user-supplied value and verify it is a `?` parameter.

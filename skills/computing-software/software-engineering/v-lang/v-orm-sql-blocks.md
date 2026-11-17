---
id: computing-software.software-engineering.v-lang.v-orm-sql-blocks
name: v-orm-sql-blocks
category: computing-software
field: software-engineering
product: v-lang
tags: [v-orm-sql-blocks, orm-and-databases, orm, sql block, sql db, create table, insert into, select from, where, update, delete, struct mapping, v-lang]
level: practitioner
status: draft
description: "Use the built-in ORM with sql db { } blocks to create tables, insert, select with where, order, limit, update and delete structs."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# V ORM: sql blocks, create, insert, select

Goal: query a database with type-checked V syntax.

```v
struct User {
    id   int    @[primary; sql: serial]
    name string
    age  int
}
sql db { create table User }!
u := User{name: 'Ann', age: 30}
sql db { insert u into User }!
adults := sql db { select from User where age >= 18 order by name limit 10 }!
sql db { update User set age = 31 where name == 'Ann' }!
sql db { delete from User where id == 1 }!
n := sql db { select count from User }!
```
- Field attributes: `@[primary]`, `@[sql: serial]`, `@[unique]`, `@[sql: 'col_name']`, `@[sql_type: 'TEXT']`, `@[skip]`/`@[sql: '-']`, `@[default: 'x']`, `@[fkey: 'user']` (confirm).
- Interpolate variables directly: `where name == who` (parameterised under the hood, not string concatenation).
- `db` is a `sqlite.DB`, `pg.DB` or `mysql.DB` value.

Gotchas:
- Schema changes are not migrated automatically; run `drop table`/alter manually.
- Every sql block returns a result; handle with `!`.

Verify: insert and select a row in an in-memory sqlite db.

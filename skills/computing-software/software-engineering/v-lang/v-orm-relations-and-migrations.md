---
id: computing-software.software-engineering.v-lang.v-orm-relations-and-migrations
name: v-orm-relations-and-migrations
category: computing-software
field: software-engineering
product: v-lang
tags: [v-orm-relations-and-migrations, orm-and-databases, orm relations, foreign key, fkey, one to many, transaction, migration, schema, joins, orm limits, v-lang]
level: advanced
status: draft
description: "Model one-to-many with @[fkey], use transactions, handle schema evolution manually and know current ORM limitations."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ORM relations, transactions and schema management

Goal: scale beyond single tables.

- One-to-many: `struct Post { id int @[primary; sql: serial]  user_id int  title string }` and child arrays in the parent: `posts []Post @[fkey: 'user_id']`; inserting a parent with children saves them (confirm behaviour for your version).
- Query children: `posts := sql db { select from Post where user_id == uid }!`.
- Transactions: run `db.exec('BEGIN')!` ... `COMMIT`/`ROLLBACK` around sql blocks on the same connection (or ORM `begin/commit` helpers if present; confirm).
- Migrations: keep numbered `.sql` files and a `schema_version` table; apply with `db.exec` in order; V's `create table` only creates when missing.
- Limits: complex joins, group by and aggregations often need raw SQL (`exec`); check release notes since ORM capabilities grow.

Gotchas:
- Struct changes do not alter the DB.
- Unique and foreign key support varies by backend.

Verify: insert parent with children and select back counts.

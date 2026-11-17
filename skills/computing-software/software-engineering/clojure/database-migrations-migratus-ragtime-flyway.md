---
id: computing-software.software-engineering.clojure.database-migrations-migratus-ragtime-flyway
name: database-migrations-migratus-ragtime-flyway
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, migrations, migratus, ragtime, flyway, schema-versioning, sql-migrations, rollback, db-migrations]
level: practitioner
status: draft
description: "Manage schema changes with versioned SQL migrations using Migratus or Ragtime (or Flyway), run them at startup or in CI, and keep them reversible and idempotent."
sources: ["https://github.com/yogthos/migratus", "https://github.com/weavejester/ragtime"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Database migrations

**Goal:** version the schema alongside the code.

```clojure
;; Migratus config
(def config {:store :database
             :migration-dir "migrations"          ; resources/migrations
             :db {:dbtype "postgresql" :dbname "app" ...}})
(require '[migratus.core :as migratus])
(migratus/create config "add-users-table")        ; creates ...-add-users-table.up.sql and .down.sql
(migratus/migrate config)
(migratus/rollback config)
(migratus/pending-list config)
```
- Files named `<timestamp>-<name>.up.sql` and `.down.sql` run in order; applied versions are recorded in a table.
- Ragtime uses a similar model (`ragtime.jdbc/load-resources "migrations"`, `ragtime.repl/migrate`).
- Flyway (Java) also works with `V1__name.sql` files and the Flyway API.
- Do not edit applied migrations; add a new one.
- Run migrations in a separate deploy step or at startup behind a lock; make them backward compatible so old and new
  app versions can run during rollout (expand, then contract).
- Wrap DDL in transactions where the database supports it (PostgreSQL does; MySQL DDL auto-commits).
- Test: run all migrations on an empty database in CI and compare against production schema if possible.

## Failure modes
- Down migrations that lose data; document or omit.
- Two developers creating the same timestamp ordering conflicts.

## Self-check
Create a database, run `migrate`, `rollback`, then `migrate` again to prove both directions work.

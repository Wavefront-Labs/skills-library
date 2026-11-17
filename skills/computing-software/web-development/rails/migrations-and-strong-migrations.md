---
id: computing-software.web-development.rails.migrations-and-strong-migrations
name: migrations-and-strong-migrations
category: computing-software
field: web-development
product: rails
tags: [rails, rails-migrations, strong-migrations, zero-downtime, active-record, schema-rb, ruby, web-development]
level: practitioner
status: docs-checked
description: "Writing safe Rails migrations: reversible change/up/down, strong_migrations checks, concurrent indexes, column removal with ignored_columns, and data backfills."
sources:
  - https://guides.rubyonrails.org/active_record_migrations.html
  - https://github.com/ankane/strong_migrations
  - https://api.rubyonrails.org/classes/ActiveRecord/Migration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrations and strong_migrations safety

**Goal:** schema changes that deploy without downtime or locked tables, and roll back cleanly.

## 1. Reversible by default
```ruby
class AddStatusToOrders < ActiveRecord::Migration[8.1]
  def change
    add_column :orders, :status, :string, default: "pending", null: false
  end
end
```
`change` auto-reverses known operations; `change_column` is irreversible, so wrap it in `reversible` (or use `up`/`down`). Use `reversible do |dir| dir.up {...}; dir.down {...} end` for custom SQL; `raise ActiveRecord::IrreversibleMigration` when you truly can't reverse. Prove it: `bin/rails db:migrate && bin/rails db:rollback && bin/rails db:migrate`.

## 2. strong_migrations
```ruby
# Gemfile
gem "strong_migrations"
```
`bin/rails generate strong_migrations:install`. It stops dangerous migrations with an explanation and the safe alternative: removing or renaming columns and tables, adding indexes non-concurrently (Postgres), and adding foreign keys, check constraints or `NOT NULL` in one step. For migrations that predate the gem set `StrongMigrations.start_after = <version of your latest migration>` in an initializer; `StrongMigrations.lock_timeout = 10.seconds` and `StrongMigrations.statement_timeout = 1.hour` are the README's examples.

## 3. Safe patterns (PostgreSQL)
**Index:**
```ruby
class AddIndexOnOrdersEmail < ActiveRecord::Migration[8.1]
  disable_ddl_transaction!
  def change
    add_index :orders, :email, algorithm: :concurrently
  end
end
```
**Remove a column:** first deploy `self.ignored_columns += ["legacy_flag"]` in the model, then, after that code is deployed, a migration with `safety_assured { remove_column :orders, :legacy_flag }`.
**Rename:** create the new column, write to both, backfill, move reads, stop writing to the old column, drop it.
**NOT NULL on a big table (Postgres):** `add_check_constraint :orders, "status IS NOT NULL", name: "orders_status_null", validate: false`, then `validate_check_constraint`, `change_column_null` and `remove_check_constraint` in a later migration.
**Foreign key (Postgres):** `add_foreign_key ..., validate: false` then `validate_foreign_key` in a separate migration.

## 4. Data backfills
Backfill safely by batching, throttling and running outside a transaction: the README suggests the Rails console or a separate migration with `disable_ddl_transaction!`:
```ruby
class BackfillOrderStatus < ActiveRecord::Migration[8.1]
  disable_ddl_transaction!
  def up
    Order.unscoped.in_batches(of: 10_000) do |relation|
      relation.where(status: nil).update_all(status: "pending")
      sleep(0.01) # throttle
    end
  end
end
```
If you backfill with something other than `update_all`, call `Order.reset_column_information` first.

## 5. Schema files
Commit `db/schema.rb`, or `db/structure.sql` when `config.active_record.schema_format` is `:sql` (needed for database-specific features the Ruby schema cannot express; on PostgreSQL it is dumped with `pg_dump`). `bin/rails db:prepare` sets up the database; load a structure file with `bin/rails db:schema:load`.

## Verify
- [ ] strong_migrations installed; no unexplained `safety_assured` blocks.
- [ ] Every migration migrates, rolls back and re-migrates in CI.
- [ ] Big-table migrations rehearsed on a production-sized copy with timeouts set.

## Checked
Checked 2026-10-24 against the Rails 8.1.4 migrations guide and the strong_migrations README (default branch). Confirmed: `Migration[8.1]`, irreversible `change_column`, `reversible`, `IrreversibleMigration`, `disable_ddl_transaction!`, `strong_migrations:install`, `start_after`, `lock_timeout`/`statement_timeout`, `safety_assured`, `ignored_columns` before `remove_column`, the six-step rename procedure, `algorithm: :concurrently` needing `disable_ddl_transaction!`, `validate: false` foreign keys and check constraints with `validate_*`, the batched backfill pattern, `schema_format :sql` and `db:prepare`. Fixed: the opening example combined `index: { algorithm: :concurrently }` with a transactional `change` (the README says that fails) and used a stale `Migration[8.0]`; removed the `git diff --exit-code` drift check and the "write a minimal class inside the migration" advice, which the checked pages do not state.

Method: documentation only; no commands were run.

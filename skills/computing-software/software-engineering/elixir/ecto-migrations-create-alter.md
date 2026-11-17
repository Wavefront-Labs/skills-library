---
id: computing-software.software-engineering.elixir.ecto-migrations-create-alter
name: ecto-migrations-create-alter
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, ecto-migration, mix-ecto-migrate, create-table, alter-table, index, rollback, concurrently, mix-ecto-gen-migration, ecto-migrations]
level: practitioner
status: docs-checked
description: "Generate and run migrations, add indexes safely (concurrently), make reversible changes and roll back."
sources: ["https://hexdocs.pm/ecto_sql/Ecto.Migration.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrations and schema changes

**Goal:** evolve the schema without downtime or data loss.

```bash
mix ecto.gen.migration add_users ; mix ecto.migrate ; mix ecto.rollback --step 1 ; mix ecto.migrations
```
```elixir
defmodule MyApp.Repo.Migrations.AddUsers do
  use Ecto.Migration
  @disable_ddl_transaction true       # required for concurrently
  @disable_migration_lock true
  def change do
    create table(:users) do
      add :email, :string, null: false
      add :org_id, references(:orgs, on_delete: :delete_all)
      timestamps(type: :utc_datetime)
    end
    create unique_index(:users, [:email])
    create index(:posts, [:user_id], concurrently: true)
  end
end
```

## Rules
- `change/0` is auto-reversible for create/add/rename; use `up/0` and `down/0` for irreversible steps (`execute/2` gives both directions).
- Never edit a migration that has run in shared environments; add a new one.
- On big tables, add indexes concurrently (PostgreSQL), add columns without volatile defaults, and backfill in separate batched steps.
- Release deploys run migrations through an eval'd release module (no Mix).
- Keep schema modules and migrations separate: do not import app schemas into migrations (they change later).

## Self-check
Migrate up, roll back, migrate again on an empty dev DB.

## Checked
2026-11-08: confirmed against Ecto.Migration (create table, add, references, timestamps, index, unique_index, concurrently, @disable_ddl_transaction, @disable_migration_lock, change/up/down, execute). Removed: the mix ecto.setup and mix ecto.reset aliases (Phoenix-generated, not on the cited page).
Method: documentation only; no commands were run.

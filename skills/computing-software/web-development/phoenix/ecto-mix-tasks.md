---
id: computing-software.web-development.phoenix.ecto-mix-tasks
name: ecto-mix-tasks
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, ecto, ectocreate, ectomigrate, ectorollback, migrations, mix, postgresql]
level: practitioner
status: docs-checked
description: "Use mix ecto.create, drop, gen.migration, migrate and rollback, with step/to options and fixes for common ecto.create Postgres role errors."
sources:
  - https://hexdocs.pm/phoenix/ecto.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: manage the database and migrations from the command line.

## ecto.create / ecto.drop

`mix ecto.create` creates the repo's database; `mix ecto.create -r OurCustom.Repo` targets another repo. `mix ecto.drop` drops it **without prompting**.

Postgres errors the page lists for `ecto.create`, and the fix (run in `psql`):

| Error text | Fix |
|---|---|
| role "postgres" does not exist | `CREATE ROLE postgres LOGIN CREATEDB;` |
| role "postgres" is not permitted to log in | `ALTER ROLE postgres LOGIN;` |
| permission denied to create database | `ALTER ROLE postgres CREATEDB;` |
| password authentication failed for user "postgres" | change the password in the env config (dev: bottom of `config/dev.exs`) |

## ecto.gen.migration

```console
$ mix ecto.gen.migration add_comments_table
```

Use a snake_case, descriptive name. The file `priv/repo/migrations/<timestamp>_add_comments_table.exs` has an empty `change/0`, which handles both forward and rollback:

```elixir
def change do
  create table(:comments) do
    add :body, :string
    add :word_count, :integer

    timestamps(type: :utc_datetime)
  end
end
```

The migration DSL (including `alter/2`) is documented in Ecto.Migration.

## ecto.migrate / ecto.rollback

- `mix ecto.migrate` runs all pending migrations; versions are recorded in the `schema_migrations` table (the timestamp from the filename).
- `-n 2` or `--step 2` runs that many pending migrations; `--to 20150317170448` runs up to and including that version.
- `mix ecto.rollback` reverses the last migration and removes its `schema_migrations` row. It accepts `-n`, `--step`, `-v` and `--to` like migrate.

Related: computing-software.web-development.phoenix.ecto-schema-gen

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Nothing needed removal; every claim matched the page text.

Method: documentation only; no commands were run.

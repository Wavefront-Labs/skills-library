---
id: computing-software.web-development.phoenix.ecto-schema-gen
name: ecto-schema-gen
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, ecto, phxgenschema, schema, migration, postgresql, elixir]
level: practitioner
status: docs-checked
description: "Generate an Ecto schema and migration with mix phx.gen.schema, run it, and read the generated schema, migration and Repo config."
sources:
  - https://hexdocs.pm/phoenix/ecto.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: create a database-backed Ecto schema and table with `phx.gen.schema`, then understand the generated files and Repo configuration.

## Generate

```console
$ mix phx.gen.schema User users name:string email:string \
bio:string number_of_pets:integer
```

Arguments: schema name, table name, then `field:type` pairs. It creates `lib/hello/user.ex` (the schema) and `priv/repo/migrations/<timestamp>_create_users.exs`. Then run `mix ecto.migrate`. Mix assumes the dev environment unless told otherwise, e.g. `MIX_ENV=prod mix ecto.migrate`.

## What you get

- Migration: `create table(:users)` with an `add` per field plus `timestamps(type: :utc_datetime)` (adds `inserted_at` and `updated_at`).
- No `id` is listed in the migration, but Ecto adds an integer `id` primary key by default.
- Schema: `schema "users" do ... field :name, :string ... timestamps(type: :utc_datetime) end`, plus a default `changeset/2` using `cast/3` and `validate_required/3` over all fields. A schema is a plain Elixir struct mapping to and from the table.

## Repo and config

`lib/hello/repo.ex`:

```elixir
defmodule Hello.Repo do
  use Ecto.Repo,
    otp_app: :hello,
    adapter: Ecto.Adapters.Postgres
end
```

The Repo brings in the `Ecto.Repo` query functions, sets `otp_app`, and sets the adapter. `phx.new` also writes DB settings in `config/dev.exs` (`config :hello, Hello.Repo, username:, password:, hostname:, database: "hello_dev", pool_size: 10 ...`); `config/test.exs` and `config/runtime.exs` hold similar config. Edit these to match your real credentials.

## Databases

Phoenix supports PostgreSQL (default), MySQL, MSSQL, ETS and SQLite3 through Ecto. Use `phx.new --database` to change the adapter or `--no-ecto` to leave Ecto out.

Related: computing-software.web-development.phoenix.ecto-changesets, computing-software.web-development.phoenix.ecto-mix-tasks

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Nothing needed removal; every claim matched the page text.

Method: documentation only; no commands were run.

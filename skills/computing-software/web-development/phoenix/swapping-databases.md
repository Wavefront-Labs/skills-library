---
id: computing-software.web-development.phoenix.swapping-databases
name: swapping-databases
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, mysql, sqlite, ecto, postgrex, myxql, database, adapter]
level: practitioner
status: docs-checked
description: "Switch a Phoenix app from PostgreSQL to MySQL: phx.new --database flag, or swap Postgrex for MyXQL and the Repo adapter."
sources:
  - https://hexdocs.pm/phoenix/swapping_databases.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: use a database other than the default PostgreSQL (the guide's example is MySQL).

## New app
```console
$ mix phx.new hello_phoenix --database mysql
```
This configures dependencies and config; then run `mix deps.get`.

## Existing app
1. In `mix.exs` `deps`, remove Postgrex and add MyXQL:
```elixir
{:phoenix_ecto, "~> 4.4"},
{:ecto_sql, "~> 3.13"},
{:myxql, ">= 0.0.0"},
```
2. In `config/dev.exs` set default MySQL credentials (change the existing Repo block's values if present):
```elixir
config :hello_phoenix, HelloPhoenix.Repo,
  username: "root",
  password: "",
  database: "hello_phoenix_dev"
```
Also set correct values in `config/test.exs` and `config/runtime.exs`.
3. In `lib/hello_phoenix/repo.ex` set `:adapter` to `Ecto.Adapters.MyXQL`.
4. Fetch and create:
```console
$ mix deps.get
$ mix ecto.create
$ mix ecto.migrate
```

## Other data stores
ETS (in Ecto via `etso`) and DETS are built into Erlang/OTP; many libraries exist for other stores. The guide does not cover them.

## Checked

2026-11-08. Read the Phoenix guide Swapping Databases in full. Confirmed the --database mysql flag, the mix.exs dependency swap to myxql, the dev/test/runtime config note, the Ecto.Adapters.MyXQL adapter, and the ETS/DETS note. Nothing removed.

Method: documentation only; no commands were run.

---
id: computing-software.web-development.phoenix.ecto-repo-persistence
name: ecto-repo-persistence
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, ecto, repo, insert, update, query, persistence, elixir]
level: practitioner
status: docs-checked
description: "Persist and query data with Ecto Repo in IEx: insert, all, one, from queries, update, delete and the bulk *_all functions."
sources:
  - https://hexdocs.pm/phoenix/ecto.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: use the `Repo` module to store and fetch schema data.

The Repo handles adapter communication, connection pooling, and translating database constraint errors. Try it in `iex -S mix`:

```elixir
iex> alias Hello.{Repo, User}
iex> Repo.insert(%User{email: "user1@example.com"})
{:ok, %Hello.User{...}}
```

`Repo.insert/2` takes a struct or a changeset and returns `{:ok, struct}`; for an invalid changeset it returns `{:error, changeset}`. In dev the SQL is logged at debug level.

## Fetch

```elixir
iex> Repo.all(User)
iex> import Ecto.Query
iex> Repo.all(from u in User, select: u.email)
iex> Repo.one(from u in User, where: ilike(u.email, "%1%"), select: count(u.id))
iex> Repo.all(from u in User, select: %{u.id => u.email})
```

`Repo.all(User)` turns the schema into a SQL query and maps rows back to `%User{}` structs. `Ecto.Query` gives a query DSL with SQL injection protection and compile-time query optimisation. The page uses `Repo.one/2` to fetch a count.

## Change and delete

- Single record: `Repo.update/2`, `Repo.delete/2`
- Bulk: `Repo.insert_all/3`, `Repo.update_all/3`, `Repo.delete_all/2`

Related: computing-software.web-development.phoenix.ecto-changesets, computing-software.web-development.phoenix.first-context

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Replaced an unsupported claim about `Repo.one` with what the page shows (a count fetched with `Repo.one/2`).

Method: documentation only; no commands were run.

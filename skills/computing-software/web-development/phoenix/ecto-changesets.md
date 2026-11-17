---
id: computing-software.web-development.phoenix.ecto-changesets
name: ecto-changesets
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, ecto, changeset, validate, cast, validations, elixir]
level: practitioner
status: docs-checked
description: "Build Ecto changesets with cast, validate_required, validate_length and validate_format, and inspect valid?, errors and changes in IEx."
sources:
  - https://hexdocs.pm/phoenix/ecto.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: validate and filter external params before they reach the database.

A changeset is a pipeline of transformations (type-casting, validation, dropping extra params). Repos are changeset-aware: invalid data is refused and updates only touch changed fields.

## Default generated changeset

```elixir
def changeset(user, attrs) do
  user
  |> cast(attrs, [:name, :email, :bio, :number_of_pets])
  |> validate_required([:name, :email, :bio, :number_of_pets])
end
```

- `cast/3`: struct, params, list of permitted fields. It only takes fields that exist in the schema, so unknown keys (e.g. `random_key`) are stripped.
- `validate_required/3`: the listed fields must be present. To make one optional, remove it from this list.

## Add validations

```elixir
|> validate_length(:bio, min: 2)
|> validate_length(:bio, max: 140)
|> validate_format(:email, ~r/@/)
```

Many more are in the Ecto.Changeset docs.

## Inspect in IEx

Start with `iex -S mix`, `alias Hello.User`, then:

```elixir
iex> changeset = User.changeset(%User{}, %{})
iex> changeset.valid?
false
iex> changeset.errors
[name: {"can't be blank", [validation: :required]}, ...]
iex> changeset.changes
```

After editing the module, call `recompile()` in IEx and rebuild the changeset. Examples from the page: `User.changeset(%User{}, %{bio: "A"})` gives `changeset.errors[:bio]` = `{"should be at least %{count} character(s)", [count: 2, validation: :length, kind: :min, type: :string]}`; `%{email: "example.com"}` gives `{"has invalid format", [validation: :format]}`.

Passing a changeset to `Repo.insert/2`: valid returns `{:ok, struct}`, invalid returns `{:error, changeset}`.

Related: computing-software.web-development.phoenix.ecto-repo-persistence

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Nothing needed removal; every claim matched the page text.

Method: documentation only; no commands were run.

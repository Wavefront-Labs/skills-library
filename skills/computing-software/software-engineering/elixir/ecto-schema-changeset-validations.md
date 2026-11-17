---
id: computing-software.software-engineering.elixir.ecto-schema-changeset-validations
name: ecto-schema-changeset-validations
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, ecto, schema, changeset, cast, validate-required, validate-format, unique-constraint, embedded-schema, ecto-schema-changeset, elixir-ecto]
level: practitioner
status: docs-checked
description: "Define Ecto schemas and build changesets with cast, validate_* and constraint functions; separate create and update changesets."
sources: ["https://hexdocs.pm/ecto/Ecto.Schema.html", "https://hexdocs.pm/ecto/Ecto.Changeset.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Schemas and changesets

**Goal:** validate and persist user input safely.

```elixir
defmodule MyApp.User do
  use Ecto.Schema
  import Ecto.Changeset
  schema "users" do
    field :email, :string
    field :age, :integer
    field :password, :string, virtual: true, redact: true
    has_many :posts, MyApp.Post
    timestamps(type: :utc_datetime)
  end
  def changeset(user, attrs) do
    user
    |> cast(attrs, [:email, :age, :password])          # whitelist: only these keys are accepted
    |> validate_required([:email])
    |> validate_format(:email, ~r/@/)
    |> validate_number(:age, greater_than_or_equal_to: 0)
    |> validate_length(:password, min: 12)
    |> unique_constraint(:email)                        # needs a unique index in the DB
  end
end
Repo.insert(User.changeset(%User{}, params))   # {:ok, user} | {:error, changeset}
```

## Rules
- `cast/4` (opts default to `[]`, so `cast/3` calls work) is the mass-assignment guard: never cast fields such as `:is_admin` from user input.
- `unique_constraint` converts the database error into a changeset error; it does not itself check uniqueness. `unsafe_validate_unique` is only a best-effort pre-check.
- Errors: `changeset.errors`, `traverse_errors/2` for rendering; `changeset.valid?`.
- Use `embedded_schema` for forms and API params not backed by a table.
- `Repo.insert!` raises `Ecto.InvalidChangesetError` on an invalid changeset.

## Self-check
Insert two users with the same email and confirm the second returns an error from the constraint, not an exception.

## Checked
2026-11-08: confirmed against Ecto.Schema (schema, field, virtual, redact, embedded_schema, has_many, timestamps) and Ecto.Changeset (cast, validate_*, unique_constraint, unsafe_validate_unique, traverse_errors) and Ecto.Repo insert!. Removed: the cast/3 arity wording and the insert!/2 arity.
Method: documentation only; no commands were run.

---
id: computing-software.web-development.phoenix.testing-contexts
name: testing-contexts
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, datacase, context, schema, sandbox, errors-on, exunit, changeset]
level: practitioner
status: docs-checked
description: "Test Phoenix contexts and schemas with DataCase: describe blocks, fixtures, the SQL Sandbox, async tests, and errors_on for changeset validations."
sources:
  - https://hexdocs.pm/phoenix/testing_contexts.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: write and understand context and schema tests in a generated Phoenix app (example: `mix phx.gen.html Blog Post posts title body:text`).

## Context tests

`test/hello/blog_test.exs` uses `Hello.DataCase` (the counterpart of `ConnCase` for contexts and schemas), aliases `Hello.Blog`, and groups tests in `describe "posts"` (one describe per schema, since a context can hold several; generating `Blog Comment comments ...` adds a `describe "comments"`). Fixtures come from `import Hello.BlogFixtures`:

```elixir
test "list_posts/0 returns all posts" do
  post = post_fixture()
  assert Blog.list_posts() == [post]
end

test "create_post/1 with valid data creates a post" do
  valid_attrs = %{body: "some body", title: "some title"}
  assert {:ok, %Post{} = post} = Blog.create_post(valid_attrs)
  assert post.body == "some body"
end
```

## DataCase and the SQL Sandbox

`DataCase` is an `ExUnit.CaseTemplate`: its `using` block aliases `Hello.Repo` and imports `Ecto`, `Ecto.Changeset`, `Ecto.Query`, `Hello.DataCase`. Its setup calls:

```elixir
def setup_sandbox(tags) do
  pid = Ecto.Adapters.SQL.Sandbox.start_owner!(Hello.Repo, shared: not tags[:async])
  on_exit(fn -> Ecto.Adapters.SQL.Sandbox.stop_owner(pid) end)
end
```

Each test runs in a transaction that is rolled back at the end, so data never leaks between tests. The sandbox also lets DB-touching tests run concurrently on PostgreSQL: `use Hello.DataCase, async: true`. See the `Ecto.Adapters.SQL.Sandbox` docs for async considerations.

## Schema tests and errors_on

Guideline: keep side-effect-free code (data structures, schemas, changesets) in the schema; the context creates/updates schemas and writes to a database or API. Test them accordingly. Add a validation:

```elixir
def changeset(post, attrs) do
  post
  |> cast(attrs, [:title, :body])
  |> validate_required([:title, :body])
  |> validate_length(:title, min: 2)
end
```

Test it in `test/hello/blog/post_test.exs`:

```elixir
defmodule Hello.Blog.PostTest do
  use Hello.DataCase, async: true
  alias Hello.Blog.Post

  test "title must be at least two characters long" do
    changeset = Post.changeset(%Post{}, %{title: "I"})
    assert %{title: ["should be at least 2 character(s)"]} = errors_on(changeset)
  end
end
```

`errors_on/1` is defined at the bottom of `DataCase` for exactly this.

## Checked

2026-11-08. Read the Phoenix guide Testing Contexts in full. Confirmed the BlogTest layout, DataCase contents, SQL Sandbox start_owner! code, async: true note for PostgreSQL, the schema-versus-context guideline, and the errors_on example. Nothing removed.

Method: documentation only; no commands were run.

---
id: computing-software.software-engineering.elixir.phoenix-controller-context-heex
name: phoenix-controller-context-heex
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, phoenix-controller, context, heex, function-components, action-fallback, render, phx-gen, phoenix-controllers-contexts]
level: practitioner
status: docs-checked
description: "Keep controllers thin, put business logic in context modules, render with HEEx function components and use action_fallback for errors."
sources: ["https://hexdocs.pm/phoenix/controllers.html", "https://hexdocs.pm/phoenix/contexts.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controllers, contexts and templates

**Goal:** a maintainable layering for web apps.

```elixir
defmodule MyAppWeb.PostController do
  use MyAppWeb, :controller
  action_fallback MyAppWeb.FallbackController
  def show(conn, %{"id" => id}) do
    with {:ok, post} <- Blog.fetch_post(id) do
      render(conn, :show, post: post)
    end
  end
  def create(conn, %{"post" => params}) do
    with {:ok, post} <- Blog.create_post(params) do
      conn |> put_status(:created) |> render(:show, post: post)
    end
  end
end
defmodule MyAppWeb.FallbackController do
  use MyAppWeb, :controller
  def call(conn, {:error, :not_found}), do: conn |> put_status(:not_found) |> put_view(json: MyAppWeb.ErrorJSON) |> render(:"404")
  def call(conn, {:error, %Ecto.Changeset{} = cs}), do: conn |> render(:error, changeset: cs)
end
# generators: mix phx.gen.context / phx.gen.html / phx.gen.json / phx.gen.auth
```

## Rules
- Contexts (`Blog`, `Accounts`) own schemas and Repo calls; controllers and LiveViews call context functions only.
- Parameters arrive as string-keyed maps; cast with changesets rather than trusting shapes.
- Templates use HEEx (`~H`).
- `mix phx.gen.auth` is the supported starting point for authentication.

## Self-check
Add an error return in a context and confirm the fallback controller renders the error response.

## Checked
2026-11-08: confirmed against the Phoenix controllers and contexts guides, Phoenix.Controller (action_fallback, put_status, put_view, render) and the phx.gen.context, phx.gen.html, phx.gen.json and phx.gen.auth generators. Removed: the unprocessable_entity status and the attr and slot component remark.
Method: documentation only; no commands were run.

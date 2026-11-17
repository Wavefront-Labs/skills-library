---
id: computing-software.software-engineering.elixir.phoenix-router-pipeline-plug
name: phoenix-router-pipeline-plug
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, phoenix-router, pipeline, plug, scope, pipe-through, verified-routes, mix-phx-routes, phoenix-router-plugs, elixir-phoenix]
level: practitioner
status: docs-checked
description: "Declare routes in scopes with pipelines, write function and module plugs and use verified routes (~p)."
sources: ["https://hexdocs.pm/phoenix/routing.html", "https://hexdocs.pm/plug/Plug.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Router, pipelines and plugs

**Goal:** map requests to handlers with the right pipeline.

```elixir
defmodule MyAppWeb.Router do
  use MyAppWeb, :router
  pipeline :browser do
    plug :accepts, ["html"]; plug :fetch_session; plug :fetch_live_flash
    plug :protect_from_forgery; plug :put_secure_browser_headers
    plug :require_user
  end
  pipeline :api, do: plug(:accepts, ["json"])
  scope "/", MyAppWeb do
    pipe_through :browser
    get "/", PageController, :home
    resources "/posts", PostController
    live "/dash", DashLive
  end
  scope "/api", MyAppWeb do pipe_through :api; get "/ping", PingController, :show end

  def require_user(conn, _opts) do          # function plug
    if conn.assigns[:current_user], do: conn, else: conn |> redirect(to: ~p"/login") |> halt()
  end
end
# in templates: ~p"/posts/#{post}"       mix phx.routes
```

## Rules
- A plug takes and returns a `%Plug.Conn{}`; after sending a response or redirect call `halt/1`.
- Module plugs implement `init/1` (compile time) and `call/2` (per request).
- Verified routes `~p` are checked at compile time against the router.
- Put authentication/authorisation in pipelines or `on_mount` hooks, not scattered in actions.

## Self-check
Run `mix phx.routes` and confirm each scope's pipeline is applied.

## Checked
2026-11-08: confirmed against the Phoenix routing guide, Phoenix.Router (pipeline, pipe_through, scope, resources, live), verified routes, the default browser pipeline plugs, mix phx.routes and the Plug behaviour (init/1, call/2, halt). Removed: nothing.
Method: documentation only; no commands were run.

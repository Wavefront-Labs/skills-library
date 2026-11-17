---
id: computing-software.software-engineering.elixir.plug-bandit-cowboy-server
name: plug-bandit-cowboy-server
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, plug, bandit, cowboy, plug-router, plug-conn, webserver, plug-test, plug-bandit-cowboy]
level: practitioner
status: draft
description: "Build small HTTP services with Plug.Router and run them under Bandit (the default Phoenix server in recent versions) or Cowboy."
sources: ["https://hexdocs.pm/plug", "https://hexdocs.pm/bandit"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Plug, Bandit and Cowboy servers

**Goal:** a minimal web service without Phoenix.

```elixir
defmodule MyApp.Router do
  use Plug.Router
  plug :match
  plug Plug.Parsers, parsers: [:urlencoded, :json], json_decoder: Jason
  plug :dispatch
  get "/health", do: send_resp(conn, 200, "ok")
  post "/items" do
    send_resp(conn, 201, Jason.encode!(%{id: 1, name: conn.body_params["name"]}))
  end
  match _, do: send_resp(conn, 404, "not found")
end
# children = [{Bandit, plug: MyApp.Router, scheme: :http, port: 4000}]
# test: import Plug.Test; conn = conn(:get, "/health") |> MyApp.Router.call([])
```

## Rules
- A Plug is a function `(conn, opts) -> conn` or a module with `init/1` and `call/2`.
- Order matters: `:match`, parsers, `:dispatch`.
- Set body size limits in `Plug.Parsers` (`length:`) to bound memory.
- Phoenix uses Bandit by default in new apps since Phoenix 1.7.11 (unconfirmed exact version); older apps use Cowboy via `Phoenix.Endpoint.Cowboy2Adapter`.

## Self-check
Test the router with `Plug.Test.conn/3` and assert `conn.status == 200`.

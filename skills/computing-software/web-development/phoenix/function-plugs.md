---
id: computing-software.web-development.phoenix.function-plugs
name: function-plugs
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, plug, conn, function-plug, endpoint, elixir]
level: practitioner
status: docs-checked
description: "Write a Phoenix function plug that takes a Plug.Conn and options, returns the conn, and plug it into the endpoint, router pipeline or controller."
sources:
  - https://hexdocs.pm/phoenix/plug.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: add a connection transformation as a plain function plug.

A function plug accepts a `%Plug.Conn{}` as first argument and options as second, and returns a `%Plug.Conn{}`. Any function meeting both rules works.

```elixir
def introspect(conn, _opts) do
  IO.puts """
  Verb: #{inspect(conn.method)}
  Host: #{inspect(conn.host)}
  Headers: #{inspect(conn.req_headers)}
  """

  conn
end
```

Plug it by passing the function name as an atom. In `lib/hello_web/endpoint.ex`, put `plug :introspect` right before `plug HelloWeb.Router` and define the function in the endpoint module. Fetching `http://localhost:4000` then prints the verb, host and headers in the shell. See `Plug.Conn` docs for all conn fields.

## Where plugs can go

- Endpoint: plugs common to every request, applied before the router.
- Router: inside `pipeline` blocks, e.g. `plug :accepts, ["html"]`; once a route matches, every plug in its pipelines runs.
- Controller: `plug :name` at the top of the controller; limit to actions with `plug HelloWeb.Plugs.Locale, "en" when action in [:index]`.

## Compose instead of nesting

Replace nested `case`/`if` chains with flat plugs (`plug :authenticate`, `plug :fetch_message`, `plug :authorize_message`). On a failure path, redirect and then call `halt()`:

```elixir
conn |> put_flash(:info, "You must be logged in") |> redirect(to: ~p"/") |> halt()
```

`halt(conn)` tells Plug the next plug must not be invoked. Pass data downstream with `assign(conn, :user, user)` and read it from `conn.assigns[:user]`.

Related: computing-software.web-development.phoenix.module-plugs

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Nothing needed removal; every claim matched the page text.

Method: documentation only; no commands were run.

---
id: computing-software.web-development.phoenix.verified-routes
name: verified-routes
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, verifiedroutes, sigilp, routing, compile-time, url, query-string]
level: practitioner
status: docs-checked
description: "Use the ~p sigil for compile-time verified paths in templates, controllers and tests, with query strings and full URLs via url/1."
sources:
  - https://hexdocs.pm/phoenix/routing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: replace hard-coded paths with `~p` so the compiler flags paths that no longer match the router.

## How it works
`Phoenix.VerifiedRoutes` checks `~p` paths against your router at compile time. Try it in `iex -S mix`:
```elixir
defmodule RouteExample do
  use HelloWeb, :verified_routes

  def example do
    ~p"/comments"
    ~p"/unknown/123"
  end
end
```
The unknown path gives: `warning: no route path for HelloWeb.Router matches "/unknown/123"`; the existing route gives none.

Generated projects already enable verified routes across the web layer, including tests.

## Usage
Template:
```heex
<a href={~p"/"}>Welcome Page!</a>
<a href={~p"/comments"}>View Comments</a>
```
Controller redirect:
```elixir
redirect(conn, to: ~p"/comments/#{comment}")
```

## Query strings
```elixir
~p"/users/17?admin=true&active=false"   # "/users/17?admin=true&active=false"
~p"/users/17?#{[admin: true]}"          # "/users/17?admin=true"
~p"/users/17?#{%{admin: true}}"         # "/users/17?admin=true"
```

## Full URLs
Wrap with `url/1` (imported wherever `~p` is available):
```elixir
url(~p"/users")   # "http://localhost:4000/users"
```
Host, port, proxy port and SSL come from each environment's config (see `config/dev.exs`).

## Related
computing-software.web-development.phoenix.nested-resources

## Checked

2026-11-08. Checked against the Phoenix Routing guide page on hexdocs (read the verified routes and scopes sections; the rest of the page was matched with a phrase checker). Removed anything the page did not state.

Method: documentation only; no commands were run.

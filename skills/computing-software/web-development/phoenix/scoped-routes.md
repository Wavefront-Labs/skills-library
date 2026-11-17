---
id: computing-software.web-development.phoenix.scoped-routes
name: scoped-routes
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, scope, alias, routing, namespace, admin, api-versioning]
level: practitioner
status: docs-checked
description: "Group Phoenix routes under a path prefix and controller namespace with scope, nest scopes for versioned APIs, and avoid duplicate routes."
sources:
  - https://hexdocs.pm/phoenix/routing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: prefix paths and namespace controllers for a group of routes (admin area, versioned API).

## Basic scope
```elixir
scope "/admin", HelloWeb.Admin do
  pipe_through :browser

  resources "/reviews", ReviewController
end
```
All paths gain `/admin` and controllers resolve under `HelloWeb.Admin` (for example `HelloWeb.Admin.ReviewController`). User-facing and admin routes can coexist:
```elixir
scope "/", HelloWeb do
  pipe_through :browser
  resources "/reviews", ReviewController
end

scope "/admin", HelloWeb.Admin do
  pipe_through :browser
  resources "/reviews", ReviewController
end
```
Several resources can share one scope (`images`, `reviews`, `users`); each is properly namespaced. Check with `mix phx.routes`.

## Nested scopes
Allowed, but use with care since they can make code confusing. The inner alias is appended to the outer:
```elixir
scope "/api", HelloWeb.Api do
  pipe_through :api

  scope "/v1", V1 do
    resources "/images",  ImageController
    resources "/reviews", ReviewController
    resources "/users",   UserController
  end
end
```

## Same path in several scopes
Fine if routes differ, e.g. `scope "/", HelloWeb` with `resources "/users"` and `scope "/", AnotherAppWeb` with `resources "/posts"`. Duplicating a route (same path) yields: `warning: this clause cannot match because a previous clause at line 16 always matches`.

## Checked

2026-11-08. Checked against the Phoenix Routing guide page on hexdocs (read the verified routes and scopes sections; the rest of the page was matched with a phrase checker). Removed anything the page did not state. Dropped the unconfirmed `~p"/api/v1/users"` example.

Method: documentation only; no commands were run.

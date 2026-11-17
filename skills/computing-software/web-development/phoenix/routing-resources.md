---
id: computing-software.web-development.phoenix.routing-resources
name: routing-resources
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, resources, phxroutes, router, only, except, routing]
level: practitioner
status: docs-checked
description: "Declare Phoenix routes with verb macros and resources, filter actions with only and except, and inspect them with mix phx.routes."
sources:
  - https://hexdocs.pm/phoenix/routing.html
  - https://hexdocs.pm/phoenix/cheatsheets/router.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: define routes in `lib/hello_web/router.ex` and confirm what they expand to.

## Single routes
Verb macros exist for GET, POST, PUT, PATCH, DELETE, OPTIONS, CONNECT, TRACE and HEAD:
```elixir
get "/users", UserController, :index
patch "/users/:id", UserController, :update
```

## Inspect routes
Run `mix phx.routes` at the project root. Example line: `GET  /  HelloWeb.PageController :home`.

## resources
```elixir
resources "/users", UserController
```
expands to eight routes: GET `/users` :index, GET `/users/:id/edit` :edit, GET `/users/new` :new, GET `/users/:id` :show, POST `/users` :create, PATCH `/users/:id` :update, PUT `/users/:id` :update, DELETE `/users/:id` :delete. The controller need not exist yet for `mix phx.routes` to list them.

Filter with options:
```elixir
resources "/posts", PostController, only: [:index, :show]
resources "/comments", CommentController, except: [:delete]
```
More options are described under `Phoenix.Router.resources/4`.

## Why macros
Routes compile into one large pattern-matching case, and each route also records metadata used by `Phoenix.VerifiedRoutes`.

## Summary points from the guide
A verb macro expands to one match clause, `resources` to 8; `only:`/`except:` shrink that; routes can be nested and scoped.

## Related
computing-software.web-development.phoenix.nested-resources, computing-software.web-development.phoenix.scoped-routes, computing-software.web-development.phoenix.verified-routes

## Checked

2026-11-08. Confirmed against the Phoenix guide source (phoenixframework/phoenix, guides/routing.md and guides/cheatsheets/router.cheatmd, main branch, read in full), the published form of the cited hexdocs page: verb macros, the eight resources routes, only/except, mix phx.routes output and the macro rationale. Removed: nothing.

Method: documentation only; no commands were run.

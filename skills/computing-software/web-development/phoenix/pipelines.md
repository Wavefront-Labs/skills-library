---
id: computing-software.web-development.phoenix.pipelines
name: pipelines
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, pipeline, browser, api, plug, pipe-through, routing, authentication]
level: practitioner
status: docs-checked
description: "Use Phoenix router pipelines: default browser and api pipelines, custom pipelines, pipe_through on scopes, composing pipelines, and forward."
sources:
  - https://hexdocs.pm/phoenix/routing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: attach groups of plugs to sets of routes.

## Defaults
Generated routers define two pipelines:
```elixir
pipeline :browser do
  plug :accepts, ["html"]
  plug :fetch_session
  plug :fetch_live_flash
  plug :put_root_layout, html: {HelloWeb.Layouts, :root}
  plug :protect_from_forgery
  plug :put_secure_browser_headers
end

pipeline :api do
  plug :accepts, ["json"]
end
```
`:fetch_live_flash` merges LiveView flash with controller flash; `:protect_from_forgery` and `:put_secure_browser_headers` guard form posts.

## Rules
- A scope uses a pipeline via `pipe_through`; routes outside any scope have no pipelines.
- Once a route matches, all plugs of its pipelines run. Requests first pass the endpoint plugs, then route matching.
- No route match: no pipeline runs and a 404 is raised.
- In nested scopes, parent `pipe_through`s run first, then the nested one.

## Custom pipelines
```elixir
pipeline :auth do
  plug HelloWeb.Authentication
end

scope "/reviews", HelloWeb do
  pipe_through [:browser, :auth]
  resources "/", ReviewController
end
```
Pipelines are plugs, so one can plug another:
```elixir
pipeline :auth do
  plug :browser
  plug :ensure_authenticated_user
  plug :ensure_user_owns_review
end

scope "/reviews", HelloWeb do
  pipe_through :auth
  resources "/", ReviewController
end
```

## Organising routes
Split routes across scopes by pipeline (public reads under `[:browser]`, creates under `[:browser, :auth]`) so you can easily audit which routes require authentication.

## Forward
`forward "/jobs", BackgroundJob.Plug` sends every path starting with `/jobs` to that plug, which can match subroutes. Put it in a scope with `pipe_through [:authenticate_user, :ensure_admin]` to run those plugs first. Do not forward to another Phoenix endpoint: plugs would be invoked twice, which may error.

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Nothing needed removal; every claim matched the page text.

Method: documentation only; no commands were run.

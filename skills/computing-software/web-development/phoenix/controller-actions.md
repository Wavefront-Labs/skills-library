---
id: computing-software.web-development.phoenix.controller-actions
name: controller-actions
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, controller, actions, params, conn, json, request-data, elixir]
level: practitioner
status: docs-checked
description: "Write Phoenix controller actions: naming conventions, conn and params arguments, pattern matching, and how path, body and query params merge."
sources:
  - https://hexdocs.pm/phoenix/controllers.html
  - https://hexdocs.pm/phoenix/json_and_apis.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: write correct controller actions and read request data.

Controllers are plugs; `use HelloWeb, :controller` imports helpful modules. An action is a plain function whose name must match a route in the router (for `get "/", PageController, :index` define `def index`).

Conventional names: `index` (list), `show` (one item by ID), `new` (form), `create` (save new), `edit` (form for existing), `update` (save edit), `delete` (remove).

Every action takes `conn` (request info such as host, path, port, query string) and `params` (a map of request parameters). Pattern match params in the signature; prefix with an underscore when unused:

```elixir
def show(conn, %{"messenger" => messenger}) do
  render(conn, :show, messenger: messenger)
end

def index(conn, _params), do: render(conn, :home)
```

## Params are merged

Plug parses path parameters, query parameters and the body into `params`. Same-named fields override each other with priority `Path Parameters > Body (any kind) > Query Parameters`. With routes `post "/:name"` and `post "/"` and an action `render(conn, :greet, params)`, `POST /api/name1?name=name3` with JSON `{"name": "name2"}` yields name1; without the path part, name2; with only the query, name3.

Individually: `conn.path_params`, `conn.body_params`, `conn.query_params`.

Related: computing-software.web-development.phoenix.rendering

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Nothing needed removal; every claim matched the page text.

Method: documentation only; no commands were run.

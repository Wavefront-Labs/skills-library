---
id: computing-software.web-development.phoenix.json-api
name: json-api
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, json, phxgenjson, api, curl, params, json-view, noapp]
level: practitioner
status: docs-checked
description: "Build a Phoenix JSON API with mix phx.gen.json, render with a JSON view, know how params merge, and generate an API-only app with phx.new flags."
sources:
  - https://hexdocs.pm/phoenix/json_and_apis.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: scaffold and understand a CRUD JSON API in Phoenix.

## Scaffold

```console
mix phx.gen.json Urls Url urls link:string title:string
```

It creates a controller, `url_json.ex`, `changeset_json.ex`, `fallback_controller.ex`, the schema, migration, context and tests. Add the route it asks for to the `:api` scope, then migrate:

```elixir
scope "/api", HelloWeb do
  pipe_through :api
  resources "/urls", UrlController, except: [:new, :edit]
end
```

```console
mix ecto.migrate
mix phx.server
```

The `:api` pipeline ensures the client can handle JSON.

## Try it with curl

- `curl -i http://localhost:4000/api/urls` returns 200 with `{"data":[]}` when empty.
- Create: `curl -iX POST http://localhost:4000/api/urls -H 'Content-Type: application/json' -d '{"url": {"link":"https://elixir-lang.org", "title":"Elixir"}}'`
- Show: `GET /api/urls/1`. Update: `PUT /api/urls/2` with `{"url": {"title": "..."}}` returns 200 with the updated link. Delete: `DELETE /api/urls/2` returns 204.

## Rendering JSON

Controllers call `render(conn, :index, urls: urls)` exactly as for HTML. One view per format: HTML uses `UrlHTML`, JSON uses `UrlJSON`, whose functions return plain maps:

```elixir
def index(%{urls: urls}), do: %{data: for(url <- urls, do: data(url))}
def show(%{url: url}), do: %{data: data(url)}
defp data(%Url{} = url), do: %{id: url.id, link: url.link, title: url.title}
```

Phoenix encodes the returned map with the built-in JSON module. `create`, `update` and `delete` rely on action fallback.

## Request data

`params` merges path params, query params and body into one map. On a name clash the priority is Path > Body (any kind) > Query. Read them separately via `conn.path_params`, `conn.body_params`, `conn.query_params`. Example: `POST /api/name1?name=name3` with body `{"name": "name2"}` yields `name1`.

## API-only app

`mix help phx.new` lists the flags `--no-assets`, `--no-dashboard`, `--no-ecto`, `--no-esbuild`, `--no-gettext`, `--no-html`, `--no-live`, `--no-mailer`, `--no-tailwind`. `--no-html` is the obvious one for APIs.

```console
mix phx.new hello --no-assets --no-dashboard --no-ecto --no-gettext --no-html --no-mailer
```

Telemetry, PubSub and DNS Cluster modules are still included; remove them manually if needed. An app can serve both a REST API and a web app.

Related: computing-software.web-development.phoenix.action-fallback

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Nothing needed removal; every claim matched the page text.

Method: documentation only; no commands were run.

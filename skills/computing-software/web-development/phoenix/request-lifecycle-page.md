---
id: computing-software.web-development.phoenix.request-lifecycle-page
name: request-lifecycle-page
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, route, controller, template, heex, embed-templates, request-lifecycle, elixir]
level: intro
status: docs-checked
description: "Add a new Phoenix page by wiring a route, controller action, HTML view module and HEEx template, including a dynamic /hello/:messenger page."
sources:
  - https://hexdocs.pm/phoenix/request_lifecycle.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: serve `/hello` and `/hello/:messenger` in an app named `hello`.

## 1. Route (`lib/hello_web/router.ex`)
Inside the `scope "/", HelloWeb do ... pipe_through :browser` block:
```elixir
get "/", PageController, :home
get "/hello", HelloController, :index
get "/hello/:messenger", HelloController, :show
```
The router maps verb/path pairs to controller/action pairs. `:messenger` becomes a param (`/hello/Frank` gives `"messenger" => "Frank"`).

## 2. Controller (`lib/hello_web/controllers/hello_controller.ex`)
```elixir
defmodule HelloWeb.HelloController do
  use HelloWeb, :controller

  def index(conn, _params) do
    render(conn, :index)
  end

  def show(conn, %{"messenger" => messenger}) do
    render(conn, :show, messenger: messenger)
  end
end
```
Actions take `conn` and `params`; prefix an unused `params` with `_`. Param keys are always strings, and `=` in the pattern is a pattern match, not assignment (use `%{"messenger" => m} = params` to keep the full map). `render(conn, :index)` expects a view named after the controller and format: `HelloWeb.HelloHTML` defining `index/1`.

## 3. View (`lib/hello_web/controllers/hello_html.ex`)
```elixir
defmodule HelloWeb.HelloHTML do
  use HelloWeb, :html

  embed_templates "hello_html/*"
end
```
`embed_templates` compiles every template in the sibling `hello_html` directory into function components. The alternative is defining `def index(assigns)` returning a `~H` sigil; there is no runtime or performance difference.

## 4. Templates (`lib/hello_web/controllers/hello_html/`)
File names follow `NAME.FORMAT.TEMPLATING_LANGUAGE`.

`index.html.heex`:
```heex
<section>
  <h2>Hello World, from Phoenix!</h2>
</section>
```
`show.html.heex`:
```heex
<Layouts.app flash={@flash}>
  <section>
    <h2>Hello World, from {@messenger}!</h2>
  </section>
</Layouts.app>
```
- `@messenger` / `@flash` are assigns passed from the controller; `{...}` interpolates Elixir; `<Layouts.app>` is a function component (`HelloWeb.Layouts.app`).
- HEEx escapes values automatically, protecting against cross-site scripting.

## Gotchas
- Keep controller, view and directory names matched (`hello_controller.ex`, `hello_html.ex`, `hello_html/`); a different directory name works only if `embed_templates` is updated.
- The page is wrapped by the root layout `lib/hello_web/components/layouts/root.html.heex`, which injects the template with `{@inner_content}`.
- Restart with `mix phx.server` if stopped; otherwise hot code reloading updates on the fly.

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Nothing needed removal; every claim matched the page text.

Method: documentation only; no commands were run.

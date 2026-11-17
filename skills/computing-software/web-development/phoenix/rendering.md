---
id: computing-software.web-development.phoenix.rendering
name: rendering
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, render, formats, text, json, html, view, controller]
level: practitioner
status: docs-checked
description: "Render in Phoenix controllers with text/2, json/2 and render/3, pass assigns, and add a JSON view for a second format."
sources:
  - https://hexdocs.pm/phoenix/controllers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: choose the right rendering call and wire views per format.

- `text(conn, "From messenger #{messenger}")` sends plain text.
- `json(conn, %{id: messenger})` sends JSON from any encodable term; `html/2` also exists, but most HTML goes through views.
- `render(conn, :show, messenger: messenger)` calls the view layer (preferred for HTML for performance and security benefits).

For `render/3` the controller and view share a root name: `HelloController` needs `HelloHTML`, which must `embed_templates` from `lib/hello_web/controllers/hello_html/` containing `show.html.heex`.

Assigns: pass a keyword (`render(conn, :show, messenger: m, receiver: "Dweezil")`) or chain `assign(conn, :messenger, m) |> assign(:receiver, "Dweezil") |> render(:show)`.

## Another format (JSON)

`lib/hello_web.ex` declares supported formats: `use Phoenix.Controller, formats: [:html, :json]`. Phoenix then looks for `HTML` and `JSON` view modules by controller name; set explicitly with `plug :put_view, html: HelloWeb.PageHTML, json: HelloWeb.PageJSON`.

```elixir
defmodule HelloWeb.PageJSON do
  def home(_assigns) do
    %{message: "this is some JSON"}
  end
end
```

The view is just a function receiving assigns and returning a map. The router pipeline must accept the format: `plug :accepts, ["html", "json"]` in `:browser`. Then `http://localhost:4000/?_format=json` returns JSON. The guide notes real apps usually use a separate `:api` pipeline for JSON.

Related: computing-software.web-development.phoenix.direct-responses

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Nothing needed removal; every claim matched the page text.

Method: documentation only; no commands were run.
